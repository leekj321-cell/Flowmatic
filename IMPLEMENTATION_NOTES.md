# Website release 2026.09.19-r6-investor

Investor-first R6 supersedes the R5 copy hierarchy while preserving existing product/detail routes, working NC/CT proof assets, corporate CI, the L1–L6 comparison, and shared runtime.

## Public-home product narrative

The homepage now leads with **One Drawing → Running Factory** rather than a module list. The primary journey is:

`Product Drawing → Process → Equipment → Tooling/Jig → Layout → Execution → Quality/Logistics → Actual Result → Blueprint Revision`

The homepage also carries the mandatory Flowmatic Factory Stack comparison:

- L6 Factory Orchestration
- L5 Optimization
- L4 Factory Engineering
- L3 Execution / G-code / SCADA
- L2 Connectivity / Adapter / Gateway
- L1 Physical / Control / PLC / Sensor / CNC I/O / Robot / AMR

Traditional full-stack deployment is presented as requiring L1 through L6. Flowmatic presents L3 through L6 as the core software/decision layer and L1/L2 as progressive/optional automation. When lower automation is absent, existing people and manual interfaces continue to provide the input/execution path. The page explicitly notes that this is a Flowmatic product communication model and not a claim that its L1–L6 labels are identical to ISA-95 levels.

## Evidence boundary

The homepage uses explicit CURRENT / PILOT / TARGET boundaries. Public NC 3D review and the existing cycle-time analysis recording remain concrete evidence. Full drawing-to-factory generation, automatic equipment sizing, full jig generation, AMR/robot sourcing, and fully closed-loop execution remain target capabilities unless separately validated.

## Canonical build and QA

`build_site.py` remains the legacy/detail-page generator and still contains R4 home generation logic. It must not be used directly for a public release.

Canonical build:

```bash
python tools/build_stc_r5_site.py
```

The wrapper captures the tracked R5 home surfaces, runs the legacy generator for detail pages, and restores the R5 homes plus `release.json`. It fails closed if the tracked home is not marked `2026.09.19-r6-investor`.

Canonical QA:

```bash
python tools/stc_r5_qa.py --browser
```

Legacy QA entry points now delegate to the R5 QA. GitHub Actions builds through the R5 wrapper, validates corporate identity and the NC public release, runs local Chromium regression, waits for the official GitHub Pages release marker, then re-runs R5 QA against `https://flowmatic-os.com`.

## R4 compatibility

`homepage-declaration.json` is retained only because historical generator/rollback code still references it. The three-line `Elegant Engineering. / Intelligent Operations. / Flowmatic.` declaration is no longer the public homepage authority. `release.json`, the tracked locale home pages, and the R5 build wrapper are authoritative.

## Visual direction

The owner-selected B direction remains: strong Mondrian structural frames with selectively rounded content cards/controls, while the locked corporate CI itself is never redrawn or recolored.
