import TurndownService from "turndown";
import { parseHTML } from "linkedom";

const MARKDOWN_ACCEPT = /(?:^|,)\s*text\/markdown(?:\s*;[^,]*)?(?:,|$)/i;
const HOMEPAGE_LINK_HEADER = [
  '</.well-known/ai-catalog.json>; rel="ai-catalog"; type="application/json"',
  '</.well-known/api-catalog>; rel="api-catalog"',
  '</.well-known/mcp/server-card.json>; rel="service-desc"; type="application/json"',
  '</auth.md>; rel="service-doc"; type="text/markdown"',
  '</.well-known/agent-card.json>; rel="describedby"; type="application/json"',
  '</.well-known/agent-skills/index.json>; rel="describedby"; type="application/json"',
  '</llms.txt>; rel="describedby"; type="text/plain"',
].join(", ");

function appendVary(headers, value) {
  const values = new Set(
    (headers.get("Vary") || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean),
  );
  values.add(value);
  headers.set("Vary", [...values].join(", "));
}

function estimateTokens(text) {
  return Math.max(1, Math.ceil(text.length / 4));
}

function isHomepage(url) {
  return url.pathname === "/" || url.pathname === "/index.html";
}

function isNoindexAsset(url) {
  return [
    "/checklist-download",
    "/checklist-download.html",
    "/checklist.pdf",
  ].includes(url.pathname);
}

function addHomepageHeaders(headers, url) {
  if (!isHomepage(url)) return;

  headers.set("Link", HOMEPAGE_LINK_HEADER);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "DENY");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  appendVary(headers, "Accept");
}

function addNoindexHeaders(headers, url) {
  if (!isNoindexAsset(url)) return;

  headers.set("X-Robots-Tag", "noindex, nofollow");
}

function htmlToMarkdown(html) {
  const { document } = parseHTML(html);
  const turndown = new TurndownService({
    bulletListMarker: "-",
    codeBlockStyle: "fenced",
    emDelimiter: "_",
    headingStyle: "atx",
  });

  turndown.remove(["script", "style", "noscript", "svg"]);
  return `${turndown.turndown(document.body).trim()}\n`;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const acceptsMarkdown = MARKDOWN_ACCEPT.test(
      request.headers.get("Accept") || "",
    );
    const assetUrl =
      url.pathname === "/"
        ? new URL(`/index.html${url.search}`, url)
        : url.pathname === "/checklist-download"
          ? new URL(`/checklist-download.html${url.search}`, url)
        : url;
    const assetRequest =
      acceptsMarkdown && request.method === "HEAD"
        ? new Request(assetUrl, {
            headers: request.headers,
            method: "GET",
          })
        : new Request(assetUrl, request);
    const response = await env.ASSETS.fetch(assetRequest);
    const isHtml = (
      response.headers.get("Content-Type") || ""
    ).toLowerCase().includes("text/html");

    if (!acceptsMarkdown || !isHtml || !response.ok) {
      const headers = new Headers(response.headers);
      addHomepageHeaders(headers, url);
      addNoindexHeaders(headers, url);

      return new Response(request.method === "HEAD" ? null : response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });
    }

    const html = await response.text();
    const markdown = htmlToMarkdown(html);
    const headers = new Headers(response.headers);

    headers.set("Content-Type", "text/markdown; charset=utf-8");
    headers.set("Content-Length", String(new TextEncoder().encode(markdown).length));
    headers.set("Content-Signal", "search=yes, ai-input=yes, ai-train=no");
    headers.set("x-markdown-tokens", String(estimateTokens(markdown)));
    headers.set("x-original-tokens", String(estimateTokens(html)));
    headers.delete("Content-Encoding");
    headers.delete("Content-Range");
    headers.delete("ETag");
    headers.delete("Last-Modified");
    headers.delete("Transfer-Encoding");
    addHomepageHeaders(headers, url);
    addNoindexHeaders(headers, url);
    appendVary(headers, "Accept");

    return new Response(request.method === "HEAD" ? null : markdown, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
