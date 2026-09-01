# Flowmatic Corporate Identity Contract

**Status:** APPROVED / LOCKED  
**Effective:** 2026-09-01  
**Authority:** This file and `brand-policy.json` are the single source of truth for every new Flowmatic document and visual deliverable.

## 1. Canonical CI assets

Use only the files under `assets/branding/canonical/`.

| Context | Required asset |
| --- | --- |
| Korean-language material on a light background | `flowmatic-ci-ko-horizontal.png` |
| English/global material on a light background | `flowmatic-ci-global-horizontal.svg` (preferred) or `.png` |
| English/global material on a dark background | `flowmatic-ci-global-reverse.svg` (preferred) or `.png` |
| Specification and visual QA | `flowmatic-ci-global-guide.svg` or `.pdf` |

The Korean horizontal raster is the supplied official Korean CI reference. The global lockup is the approved Revision 1.1 derivative. Revision 1.1 preserves the symbol width, reduces its vertical scale by 10.3%, and aligns the symbol's optical center to the complete `FLOWMATIC + MANUFACTURING INTELLIGENCE OS` block.

The files directly under `assets/branding/` that depict a flat 2×2 square are legacy website compatibility assets. They are **not** the corporate CI and are forbidden in every new deck, PDF, proposal, report, application, company profile, business card, social graphic, or generated visual.

## 2. Mandatory selection rule

- Korean-first deliverable: use the Korean horizontal CI.
- English/global deliverable: use the global horizontal CI.
- Dark background: use the approved reverse global asset. Do not create an improvised reverse Korean logo; place the Korean CI on a white holding field when the Korean lockup is required.
- Mixed-language external deliverable: use the global CI unless the Korean entity name is the primary identity of that specific submission.
- The tagline and the four intelligence axes are supporting copy, not part of the master logo.

## 3. Fixed presentation and PDF placement

This placement contract applies to presentations, investor decks, proposals, company profiles, reports, and their PDF exports.

- Cover / page 1: place one large corporate CI at the upper-left. Target width is 24% of the page or slide; permitted range is 22–30%. Use 4% top and left margins.
- Every page after page 1: place one small corporate CI at the lower-right. Target width is 8.5%; permitted range is 7–10%. Use 3% right and bottom margins.
- Keep the asset, size, and anchor consistent across all non-cover pages.
- If content collides with the CI, move or reflow the content. Do not move, crop, distort, or hide the CI.
- A Mondrian-style composition may support the layout, but it never replaces or recolors the corporate CI.

## 4. Non-negotiable integrity rules

- Never redraw, trace, regenerate, recolor, rotate, skew, crop, condense, stretch, add shadows, or substitute the symbol.
- Never recreate the logo with a generative-image model or a text font.
- Preserve aspect ratio and embedded color values.
- Use the SVG master whenever the output pipeline supports SVG; otherwise use the supplied high-resolution PNG.
- Do not add Korean, Arabic, or other text inside the global master lockup.
- Minimum global full-lockup width: 220 px digital / 42 mm print.
- Minimum standalone symbol size: 32 px digital.
- If a canonical file is unavailable or fails validation, stop the export. Do not approximate it.

## 5. Approved palette

| Role | Hex |
| --- | --- |
| Charcoal | `#101820` |
| Flow Cyan | `#00A8D2` |
| Amber | `#FFB000` |
| Blue | `#1264D8` |
| Red | `#F0442B` |

Gradients embedded in the approved vector master are part of that master and must not be edited.

## 6. Enforcement

`brand-policy.json` records the approved file hashes. Run:

```bash
python3 tools/validate_brand_contract.py
```

The repository workflow runs the same fail-closed check. Changing a canonical asset requires an explicit CI revision, an updated guide, new checksums, and documented approval.

