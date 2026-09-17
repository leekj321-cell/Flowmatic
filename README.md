# Flowmatic Website

Static Flowmatic website for GitHub Pages and `flowmatic-os.com`.

## Current public homepage

The public homepage is **STC-lite R5** (`2026.09.17-r5-stc`). It presents Flowmatic as a manufacturing operating system that starts from a product drawing, creates manufacturing decisions across process/equipment/tooling/jig/layout/execution/quality/logistics, and can begin from the existing factory before progressive L1/L2 automation is added.

Canonical homepage surfaces:

- `/` and `/ko/`: Korean STC-lite R5 homepage.
- `/en/`: English STC-lite R5 homepage.
- `/ar/`: Arabic STC-lite R5 homepage.
- `stc-lite-home-v1.css`: homepage-specific R5 styling.
- `release.json`: public homepage release authority.

Existing product, platform and compatibility routes remain in place, including `/ko/{product}/`, `/en/{product}/`, `/ar/{product}/`, `/nc.html`, `/ct.html`, `/quality.html`, `/work-standard.html`, `/tms.html`, and `/amr.html`.

## Canonical build

Do **not** use `python build_site.py` as the public release command. `build_site.py` is the legacy/detail-page generator and still contains the superseded R4 homepage narrative.

Use:

```bash
python tools/build_stc_r5_site.py
```

The wrapper rebuilds legacy/detail pages and then restores the tracked STC-lite R5 home surfaces and R5 release metadata. It fails closed if the canonical homepage is not already marked as R5.

Canonical QA:

```bash
python tools/stc_r5_qa.py
python tools/stc_r5_qa.py --browser
```

`tools/web_declaration_qa.py` and `tools/web_release_qa.py` are compatibility entry points that route to the R5 QA.

## Working demos

The current working demo assets include:

- `flowmatic_nc_demo.mp4`
- `flowmatic_ct_demo.mp4`
- Public NC 3D browser demo
- Existing Machining, Quality, Operations and Logistics detail routes

The R5 homepage explicitly separates working/current proof from STC-lite Full target capabilities.

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
- `.github/workflows/web-release-20260910.yml`: R5 build, QA and official-domain verification pipeline.

To refresh only the QR contact signature from the locked CI:

```bash
python tools/generate_brand_assets.py --qr-only
```
