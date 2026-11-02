# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Current public homepage

The public homepage follows the **Owner-approved Investor Product Scroll** (`2026.10.18-r7-product-scroll`). The current release is recorded in `release.json`. It preserves the Manufacturing Value Loop, actual product evidence and investor-first information hierarchy across Korean, English and Arabic.

Canonical homepage surfaces:

- `/` and `/ko/`: Korean investor-first homepage.
- `/en/`: English investor-first homepage.
- `/ar/`: Arabic investor-first homepage.
- `flowmatic-home.css`: homepage styling, including the investor-first type scale and hierarchy.
- `release.json`: public homepage release authority.

Existing product, platform and compatibility routes remain in place, including `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`, `/nc.html`, `/ct.html`, `/quality.html`, `/work-standard.html`, `/tms.html`, and `/amr.html`.

## Canonical build

Do **not** use `python build_site.py` as the public release command. `build_site.py` is the legacy/detail-page generator and still contains the superseded R4 homepage narrative.

Use:

```bash
python tools/build_stc_r5_site.py
```

The wrapper rebuilds detail pages and then generates the approved home surfaces from `content/investor_home.py`, including current release metadata.

Canonical QA:

```bash
python tools/validate_strategic_copy.py --profile public-web ko/index.html en/index.html ar/index.html
python tools/validate_public_terms.py --self-test
python tools/validate_public_terms.py
python tools/stc_r5_qa.py
python tools/stc_r5_qa.py --browser
```

`tools/web_declaration_qa.py` and `tools/web_release_qa.py` are compatibility entry points for the canonical homepage QA. The public-terminology check requires Poppler and Tesseract; it covers HTML, public evidence metadata, full PDF text and English OCR of product captures. Korean image text also requires visual review.

## Working demos

The current working demo assets include:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`
- Public NC 3D browser demo
- Existing Machining, Quality, Operations and Logistics detail routes

The homepage separates CURRENT working proof, PILOT validation, and TARGET Factory OS capabilities.

## Branding

All new Flowmatic presentations, PDFs, proposals, reports, applications, company profiles, business cards, generated visuals and website revisions must follow `BRANDING.md` and `brand-policy.json` and use the locked assets in `/assets/branding/canonical/`.

Validate the corporate identity contract with:

```bash
python tools/validate_brand_contract.py
```

## Contact

The site displays `contact@flowmatic-os.com`. The inquiry form uses the existing Formspree endpoint.

## Architecture notes

- `script.js`: shared navigation, interaction and demo behavior.
- `style-v5.20.css` / `web-refresh.css`: shared site styling.
- `build_site.py`: legacy/detail-page generator; not the canonical public-home build command.
- `tools/build_stc_r5_site.py`: canonical build entry point.
- `tools/stc_r5_qa.py`: canonical homepage static/browser regression.
- `homepage-declaration.json`: historical R4 generator compatibility only; it is no longer public-homepage authority.
- `.github/workflows/web-release-20260910.yml`: canonical build, QA and official-domain verification pipeline, including hashes of served evidence files.

To refresh only the QR contact signature from the locked CI:

```bash
python tools/generate_brand_assets.py --qr-only
```
