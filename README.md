# ukpetpassport.com — Landing Page

Lead capture landing page for [ukpetpassport.com](https://ukpetpassport.com).

## Stack
- Pure HTML + CSS (no frameworks, no build step)
- Hosted on Cloudflare Pages
- Form: ClickFunnels embed (replace placeholder in `index.html`)

## To deploy
1. Connect this repo to Cloudflare Pages (Settings > Pages > Connect to Git)
2. Build command: *(none — static site)*
3. Output directory: `/` (root)
4. Add custom domain: `ukpetpassport.com`

## To update the opt-in form
In `index.html`, find the comment block:
```
<!-- CLICKFUNNELS FORM EMBED -->
```
Replace the placeholder `<form>` with your ClickFunnels embed code.

## Files
- `index.html` — full landing page
- `style.css` — all styles
