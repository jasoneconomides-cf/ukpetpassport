# UK Pet Passport SEO Daily Ops SOP

This SOP keeps search, AI answer, and agent-discovery work organised across:

- `https://ukpetpassport.com/`
- `https://blog.ukpetpassport.com/`

The goal is steady, factual visibility growth without creating thin content or overwriting another agent's work.

## Default Workflow

Use this workflow unless Jason explicitly says to push directly to `main`.

1. Pull or read the latest `main`.
2. Check current branch and working tree status.
3. Check recent commits and open branches/PRs for overlapping work.
4. Create a feature branch:
   - Codex: `codex/<task-name>`
   - Chief of Staff: `chief/<task-name>`
5. Make focused changes only.
6. Run relevant checks.
7. Commit and push the branch.
8. Open or prepare a PR into `main`.
9. Wait for Jason's approval before merging.

Direct commits to `main` are only allowed for urgent factual/legal corrections, tiny typo fixes, status/SOP updates Jason explicitly approves, or when Jason says "push directly to main".

Never force push, reset hard, overwrite unknown changes, or merge a PR without Jason's explicit approval.

## Daily Checklist

Complete these checks once per working day when actively improving visibility.

### 1. Search Health

- Check Google Search Console if available.
- Check Bing Webmaster Tools if available.
- Look for indexing errors, sitemap errors, crawl issues, manual actions, or sudden drops.
- Record notable queries with rising impressions or low click-through rate.

### 2. Technical Discovery

- Confirm the homepage responds with expected security headers and agent-discovery `Link` headers.
- Confirm these resources are live:
  - `/robots.txt`
  - `/sitemap.xml`
  - `/llms.txt`
  - `/auth.md`
  - `/.well-known/api-catalog`
  - `/.well-known/agent-card.json`
  - `/.well-known/agent-skills/index.json`
  - `/.well-known/mcp/server-card.json`
- Run `isitagentready.com` after any discovery-related change.

### 3. Content Freshness

Review one existing page or post and improve it only if there is a genuine user benefit.

Good updates include:

- Correcting rules against GOV.UK, DEFRA, or APHA sources.
- Adding a clearer answer to the main search intent.
- Adding a missing date, last-updated note, or source reference.
- Improving internal links.
- Improving image alt text.
- Removing alarmist, inflated, or vague copy.

Do not change dates just to make a page look fresh.

### 4. Internal Links

For each reviewed or new article, check links to:

- Homepage checklist signup.
- Animal Health Certificate guide.
- Relevant country guide.
- Related blog posts.
- Official GOV.UK source pages.

Use descriptive link text. Avoid vague text like "click here".

### 5. Content Ideas

Capture at least one useful article or FAQ idea from:

- Search Console queries.
- People Also Ask results.
- GOV.UK rule changes.
- Common pet owner questions.
- Competitor gaps.

Prioritise specific long-tail questions, for example:

- Can one Animal Health Certificate cover two pets?
- Can my normal vet issue an Animal Health Certificate?
- How long does an Animal Health Certificate last after entering the EU?
- Do cats need tapeworm treatment to return to the UK?
- Taking a dog from the UK to Spain: what paperwork is needed?

## Weekly Checklist

Once per week, complete a deeper review.

- Publish or prepare 2-3 properly sourced articles.
- Refresh high-impression pages with low click-through rate.
- Check all recently published posts have:
  - Title.
  - Description.
  - Published date.
  - Last updated date where appropriate.
  - Author or reviewer information where available.
  - GOV.UK or other official source references.
  - Internal links.
  - Image and alt text.
  - Structured data if supported by the template.
- Check sitemap and RSS output after blog changes.
- Check for broken internal links.
- Review homepage claims against current rules.

## Content Standards

All pet travel guidance must be factual, calm, and source-led.

Required standards:

- Use GOV.UK, DEFRA, APHA, or official EU/member-state sources for rules.
- Clearly distinguish the 10-day EU entry window from later AHC validity.
- State that one AHC can cover up to five pets where relevant.
- State that an ordinary vet can issue an AHC only if they are an authorised Official Veterinarian.
- Avoid exaggerated cost claims unless supported by current evidence.
- Avoid implying automatic refusal or quarantine for every paperwork error.
- Avoid describing UK Pet Passport as a veterinary service unless the site genuinely offers that service.

## Repo-Specific Notes

### Root Site Repo

Repository: `jasoneconomides-cf/ukpetpassport`

Local path:

```bash
/Users/jasoneconomides/Documents/Connecting Pieces/ukpetpassport
```

Primary live site:

```text
https://ukpetpassport.com/
```

Use for:

- Homepage updates.
- Privacy/disclaimer/checklist copy.
- Agent discovery files.
- `robots.txt`, `llms.txt`, `auth.md`, well-known files.
- Cloudflare Worker routing and headers.

Recommended checks:

```bash
npm run check
curl -I https://ukpetpassport.com/
```

### Blog Repo

Repository: `jasoneconomides-cf/blog`

Local path:

```bash
/Users/jasoneconomides/Documents/UK Petpassport Coding
```

Primary live site:

```text
https://blog.ukpetpassport.com/
```

Use for:

- Blog homepage.
- Blog posts.
- RSS.
- Blog sitemap.
- Article images and metadata.

Recommended checks:

```bash
npm run build
```

## Daily Report Format

Use this format when reporting back to Jason.

```text
SEO Daily Ops Report - YYYY-MM-DD

Checked:
- ...

Findings:
- ...

Changed:
- ...

Recommended next actions:
- ...

Branch/PR:
- ...
```

If no code or content changes were made, say so clearly.

## Coordination Rules

- Codex and Chief of Staff must use separate branch prefixes.
- Before editing, check latest `main`.
- Before pushing, check whether another branch or recent commit touches the same files.
- If there is overlap, pause and ask Jason.
- Keep PRs small enough to review.
- Prefer one topic per branch.

## Source References

Use these official references as defaults:

- Google SEO Starter Guide: `https://developers.google.com/search/docs/fundamentals/seo-starter-guide`
- Google Search Essentials: `https://developers.google.com/search/docs/essentials`
- Google helpful content guidance: `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`
- Google sitemap guidance: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap`
- Google structured data policies: `https://developers.google.com/search/docs/appearance/structured-data/sd-policies`
- Bing Webmaster Guidelines: `https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a`
- GOV.UK pet travel guidance: `https://www.gov.uk/taking-your-pet-abroad`
