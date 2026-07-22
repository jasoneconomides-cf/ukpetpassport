# AGENTS.md — Guidance for AI agents working on this repo

## About This Repo

This is the UK Pet Passport main site (ukpetpassport.com), a free guidance website for UK pet owners navigating post-Brexit pet travel requirements.

## Tech Stack

- **Hosting:** Cloudflare Worker
- **Domain:** ukpetpassport.com
- **Form integration:** GetResponse
- **Tracking:** Google Tag Manager, Microsoft Clarity, GetResponse Analytics
- **SDK:** ClickFunnels SDK (cf-page-token)
- **DNS:** Cloudflare (scoped API token, DNS Edit permission)

## Key Files

- `index.html` — Main landing page (lead capture)
- `llms.txt` — AI agent hint file (site structure, content)
- `robots.txt` — Crawler rules (includes AI bot allow-list)
- `sitemap.xml` — XML sitemap
- `_headers` — Security headers + Link headers for content negotiation
- `STATUS.md` — Project state (shared with Chief of Staff AI)

## Agent-Readiness

This site is configured per Cloudflare's official agent-readiness checklist:
- Markdown content negotiation via Link headers
- Explicit AI bot rules in robots.txt
- llms.txt hint file
- Sitemap references
- Schema markup on all pages

## Related Repos

- **Blog:** https://github.com/jasoneconomides-cf/blog (Astro, deployed at blog.ukpetpassport.com)
- **Project brain:** /home/personal-f96fdafc/docs/uk-pet-passport-project-brain-ai-source-of-truth-mrs90rhq

## Working with Chief of Staff

Chief of Staff (MarketingSecrets.ai) coordinates work across this repo, the blog repo, and Cloudflare DNS.
All non-STATUS.md changes go through feature branches → PRs → main.
See STATUS.md and project brain doc for current state and workflow rules.