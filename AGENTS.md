# Flowmatic Repository Instructions

## Mandatory strategic communications rule

Before creating or editing any Flowmatic investor pitch, IR deck, business plan, proposal, application narrative, executive report, market/competition analysis, company profile, or strategic website copy:

1. Read `STRATEGIC_COMMUNICATIONS_CONTRACT.md`.
2. Select the required profile: `strategic-report` for pitch/IR/report materials, `public-web` for website copy.
3. Apply the formal report-style heading, competition-analysis, target-account, claim-state and evidence rules in that contract.
4. When the output is text/HTML available in the repository or runtime, run `python tools/validate_strategic_copy.py --profile <profile> <files...>` before delivery.
5. Do not patch individual phrases while leaving the underlying narrative style unchanged. If a style violation appears, normalize the entire artifact/section against the contract.

This rule is fail-closed for external strategic communication. Conversational presentation narration, rhetorical headings, first-person promotional framing, subjective competitor praise/attack, and internal battle slang are prohibited unless the owner explicitly requests an internal-only working note.

## Mandatory corporate identity rule

Before creating or editing any presentation, PDF, proposal, report, application, company profile, business card, social graphic, marketing image, website visual, or other Flowmatic-branded material:

1. Read `BRANDING.md` and `brand-policy.json`.
2. Select the locale-appropriate asset only from `assets/branding/canonical/`.
3. Apply the relevant placement/integrity rules in `BRANDING.md`.
4. Run `python tools/validate_brand_contract.py` before delivery.

Use of the legacy 2×2 square assets directly under `assets/branding/` is prohibited for new material. Do not redraw, regenerate, approximate, recolor, or substitute the corporate CI. If the canonical asset cannot be used exactly, stop and report the blocker instead of exporting a branded deliverable.

This rule is fail-closed and takes precedence over local visual styling, templates, generated layouts, and convenience fallbacks.

## Mandatory website release rule

The public homepage authority is **Investor-first R6** (`2026.09.19-r6-investor`).

- Canonical build command: `python tools/build_stc_r5_site.py`
- Canonical QA: `python tools/stc_r5_qa.py --browser`
- Canonical release metadata: `release.json`
- Canonical home surfaces: `index.html`, `ko/index.html`, `en/index.html`, `ar/index.html`
- Homepage stylesheet: `stc-lite-home-v1.css`

Do **not** use `python build_site.py` as the public website release command. That file remains the legacy/detail-page generator and still contains the superseded R4 homepage narrative. The R5 wrapper intentionally rebuilds detail pages and restores the tracked R5 home surfaces afterward.

`homepage-declaration.json` is legacy-generator compatibility data only. Its historical `Elegant Engineering. / Intelligent Operations. / Flowmatic.` declaration must not be restored as the public homepage H1 unless the owner explicitly reverses the R5 product direction.

Any homepage change must preserve these product concepts unless explicitly instructed otherwise:

- One Drawing → Running Factory.
- Design → Build → Run → Improve.
- Flowmatic Factory Stack comparison with manufacturing-decision layers first and L1–L2 connected progressively after ROI is proven.
- Current working proof must appear before architecture or long-range vision.
- Explicit CURRENT / PILOT / TARGET claim boundaries.
- One-product / one-line 4–8 week pilot with baseline, KPI comparison, ROI decision, and expansion path.
- Primary users and budget owners must be visible in the public narrative.
- Existing NC/CT proof routes and locked corporate identity.
- Public copy must not expose internal labels such as STC-lite, Blueprint R2, L3–L6 CORE, CORE/OPTIONAL, INFERRED, manifest, hash, or Safety Contract outside an explicitly technical-detail context.
