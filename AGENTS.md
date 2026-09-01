# Flowmatic Repository Instructions

## Mandatory corporate identity rule

Before creating or editing any presentation, PDF, proposal, report, application, company profile, business card, social graphic, marketing image, or other Flowmatic-branded material:

1. Read `BRANDING.md` and `brand-policy.json`.
2. Select the locale-appropriate asset only from `assets/branding/canonical/`.
3. Apply the fixed cover and non-cover placement contract in `BRANDING.md`.
4. Run `python3 tools/validate_brand_contract.py` before delivery.

Use of the legacy 2×2 square assets directly under `assets/branding/` is prohibited for new material. Do not redraw, regenerate, approximate, or substitute the corporate CI. If the canonical asset cannot be used exactly, stop and report the blocker instead of exporting a branded deliverable.

This rule is fail-closed and takes precedence over local visual styling, templates, generated layouts, and convenience fallbacks.

