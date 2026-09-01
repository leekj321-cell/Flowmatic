# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Structure

- `/`, `/nc.html`, `/ct.html`, `/quality.html`, `/work-standard.html`, `/tms.html`, `/amr.html`: Korean compatibility URLs for existing links.
- `/ko/`, `/en/`, `/ar/`: language-specific canonical pages.
- `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`: language-specific product pages.
- `build_site.py`: static page generator for the multilingual HTML output.
- `style-v5.20.css`: current stylesheet.
- `script.js`: navigation, reveal, product CTA, text fitting, demo-video loader, and AJAX inquiry submission.
- Home composition journey: horizontal desktop assembly and a reversible mobile scroll scene from radial field scatter to four connected Intelligence axes.
- `/assets/branding/canonical/`: locked Korean and global corporate CI masters for all new materials.
- `/assets/branding/`: existing website compatibility assets, icons, social previews, and QR signature.
- `BRANDING.md`: binding corporate CI and document-placement contract.
- `brand-policy.json`: machine-readable asset paths, hashes, locale rules, and placement rules.
- `AGENTS.md`: fail-closed instructions for future automated material creation.
- `ROLLBACK.md`: pre-branding recovery tag and backup archive reference.
- `tools/validate_brand_contract.py`: deterministic integrity check for the locked corporate CI.
- `tools/generate_brand_assets.py`: existing website compatibility asset generator.

## Demo Videos

The current working demo videos are:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`

Quality Intelligence shows the working defect-to-loss-to-improvement workflow without inventing a current product screenshot. Machining Intelligence separates source-level validated Recipe and Safety Contract evidence from V.Next development and PoC scope. Work Standard, TMS, and AMR compatibility pages remain subordinate component routes.

## Contact

The site displays `contact@flowmatic-os.com`. The contact form submits to a Formspree endpoint that delivers inquiries to this verified recipient address.

## Branding

All new Flowmatic presentations, PDFs, proposals, reports, applications, company profiles, business cards, and generated visuals must use the locked assets in `/assets/branding/canonical/` and follow `BRANDING.md`.

The QR contact signature embeds the locked global CI master inside its standalone SVG so browsers render the complete lockup when the card is loaded as an image. Any remaining flat 2×2 files directly under `/assets/branding/` are legacy compatibility assets, are not the corporate CI, and must not be used in new materials.

Validate the canonical asset hashes with:

```bash
python3 tools/validate_brand_contract.py
```

## Build

Run:

```bash
python3 build_site.py
```

The site is pure static HTML/CSS/JS and does not require a package install.

To refresh only the QR contact signature from the locked CI without touching other compatibility assets, run:

```bash
python3 tools/generate_brand_assets.py --qr-only
```
