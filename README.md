# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Structure

- `/`, `/nc.html`, `/ct.html`, `/quality.html`, `/work-standard.html`, `/tms.html`, `/amr.html`: Korean compatibility URLs for existing links.
- `/ko/`, `/en/`, `/ar/`: language-specific canonical pages.
- `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`: language-specific product pages.
- `build_site.py`: static page generator for the multilingual HTML output.
- `style-v5.20.css`: current stylesheet.
- `script.js`: navigation, reveal, product CTA, text fitting, demo-video loader, and AJAX inquiry submission.
- `/assets/branding/`: official logo, app-icon, social-preview, and QR contact-signature assets.
- `BRANDING.md`: official color, logo-layout, and QR usage rules.
- `ROLLBACK.md`: pre-branding recovery tag and backup archive reference.
- `tools/generate_brand_assets.py`: deterministic source for SVG, PNG, ICO, OG, and QR assets.

## Demo Videos

The current working demo videos are:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`

Quality Intelligence shows the working defect-to-loss-to-improvement workflow without inventing a current product screenshot. Machining Intelligence separates source-level validated Recipe and Safety Contract evidence from V.Next development and PoC scope. Work Standard, TMS, and AMR compatibility pages remain subordinate component routes.

## Contact

The site displays `contact@flowmatic-os.com`. The contact form submits to a Formspree endpoint that delivers inquiries to this verified recipient address.

## Branding

All pages use one 2×2 Flowmatic mark: blue top-left, red bottom-left, and yellow in both right cells. Header, footer, favicon, manifest icons, structured data, and social previews reference the same `/assets/branding/` source set. The Contact section includes the official scan-tested QR signature for `https://flowmatic-os.com/`.

## Build

Run:

```bash
python3 build_site.py
```

The site is pure static HTML/CSS/JS and does not require a package install.
