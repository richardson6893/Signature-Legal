# Signature Legal — website

A static, multi-page website (HTML, CSS, vanilla JavaScript). No frameworks, no build tools required to host it.

## Structure
```
index.html, about.html, practice-areas.html, team.html, insights.html,
careers.html, contact.html, disclaimer.html, privacy.html, terms.html, 404.html
practice-areas/   11 practice area pages
insights/         3 placeholder articles
assets/css/style.css   all styles
assets/js/script.js    menu, disclaimer modal, form validation, scroll reveal
assets/img/            placeholder images + favicon
build.py          generates every page (content + shared header/footer)
sitemap.xml, robots.txt
```

## Editing content
All text, people, practice areas and articles live in `build.py`.
Edit it, then run `python3 build.py` to regenerate every page, so the
header, footer and disclaimer stay identical across the site.
(You can also edit the .html files directly, but changes will be
overwritten the next time you run build.py.)

## Before going live — replace placeholders
Search the project for `[` to find them:
- Photos for Chandana Gururaj and the associates: add JPGs to `assets/img/team/` and set `"photo"` / `"photo_size"` for each person in build.py (see Freud and Tahura for the pattern; crop to 4:5)
- Placeholder SVGs in `assets/img/` (books, architecture, courthouse) → real, licensed photos
- `[LINKEDIN URL]`, `[X / TWITTER URL]` → real profile links (FIRM and team in build.py)
- `[editable]` bios and the "Our story" text → reviewed wording
- `[Publication date]` on articles; `[DATE]`, `[NAME]` (grievance contact), `[12 months]` in legal pages
- `[ASSIGN ADVOCATE(S)]` for practice areas with no listed advocate
- `BASE_URL` in build.py if your domain is not signaturelegal.in
- Confirm working days in the JSON-LD `openingHours` (currently every day)

## Brand assets
`assets/img/brand/` holds web versions of the supplied logos: the pen-nib mark (navy and white), the full logo, and the background watermark. Favicons and the link-preview image (`og-image.jpg`) are generated from the same files. Freud Richardson’s and Tahura Anzar’s portraits are in `assets/img/team/`.

## Making the forms deliver email
GitHub Pages can't run server code. Until a form service is connected,
the forms validate input and then open the visitor's email app with the
message addressed to contact@signaturelegal.in.

To receive submissions directly (free tiers available):
1. Create a form at formspree.io (supports file uploads for CVs on paid plans) or web3forms.com.
2. Copy the endpoint URL, e.g. `https://formspree.io/f/abcd1234`.
3. In build.py set `FORM_ENDPOINT = "https://formspree.io/f/abcd1234"` and run `python3 build.py`.

## Preview locally
Double-click index.html, or for exact behaviour run:
```
python3 -m http.server 8000
```
and open http://localhost:8000

## Deploy free on GitHub Pages
1. Create a public repository on github.com.
2. Upload everything in this folder (Add file → Upload files), keeping the folder structure.
3. Settings → Pages → Source: Deploy from a branch → main / (root) → Save.
4. After 1–2 minutes the site is live at https://<username>.github.io/<repo>/
5. Custom domain: Settings → Pages → Custom domain → signaturelegal.in, then add the DNS records GitHub shows you at your domain registrar. Tick "Enforce HTTPS".

Note: 404.html uses root-relative links, which work on a custom domain.
