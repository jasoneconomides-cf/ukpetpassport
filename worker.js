import TurndownService from "turndown";
import { parseHTML } from "linkedom";

const MARKDOWN_ACCEPT = /(?:^|,)\s*text\/markdown(?:\s*;[^,]*)?(?:,|$)/i;

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
    const response = await env.ASSETS.fetch(request);
    const acceptsMarkdown = MARKDOWN_ACCEPT.test(
      request.headers.get("Accept") || "",
    );
    const isHtml = (
      response.headers.get("Content-Type") || ""
    ).toLowerCase().includes("text/html");

    if (!acceptsMarkdown || !isHtml || !response.ok) {
      return response;
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
    appendVary(headers, "Accept");

    return new Response(request.method === "HEAD" ? null : markdown, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
