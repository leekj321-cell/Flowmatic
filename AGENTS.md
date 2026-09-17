# Flowmatic Repository Instructions

## Mandatory corporate identity rule

Before creating or editing any presentation, PDF, proposal, report, application, company profile, business card, social graphic, marketing image, website visual, or other Flowmatic-branded material:

1. Read `BRANDING.md` and `brand-policy.json`.
2. Select the locale-appropriate asset only from `assets/branding/canonical/`.
3. Apply the relevant placement/integrity rules in `BRANDING.md`.
4. Run `python tools/validate_brand_contract.py` before delivery.

Use of the legacy 2×2 square assets directly under `assets/branding/` is prohibited for new material. Do not redraw, regenerate, approximate, recolor, or substitute the corporate CI. If the canonical asset cannot be used exactly, stop and report the blocker instead of exporting a branded deliverable.

This rule is fail-closed and takes precedence over local visual styling, templates, generated layouts, and convenience fallbacks.

## Mandatory website release rule

The public homepage authority is **STC-lite R5** (`2026.09.17-r5-stc`).

- Canonical build command: `python tools/build_stc_r5_site.py`
- Canonical QA: `python tools/stc_r5_qa.py --browser`
- Canonical release metadata: `release.json`
- Canonical home surfaces: `index.html`, `ko/index.html`, `en/index.html`, `ar/index.html`
- Homepage stylesheet: `stc-lite-home-v1.css`

Do **not** use `python build_site.py` as the public website release command. That file remains the legacy/detail-page generator and still contains the superseded R4 homepage narrative. The R5 wrapper intentionally rebuilds detail pages and restores the tracked R5 home surfaces afterward.

`homepage-declaration.json` is legacy-generator compatibility data only. Its historical `Elegant Engineering. / Intelligent Operations. / Flowmatic.` declaration must not be restored as the public homepage H1 unless the owner explicitly reverses the R5 product direction.

Any homepage change must preserve these R5 concepts unless explicitly instructed otherwise:

- One Drawing → Running Factory.
- Design → Build → Run → Improve.
- Flowmatic Factory Stack comparison: L3–L6 core; L1–L2 optional/progressive.
- Human/manual fallback where lower automation layers are absent.
- Explicit separation of current working proof from STC-lite Full target capabilities.
- Existing NC/CT proof routes and locked corporate identity.
