# Flowmatic Dot / Web Demo Integration Handoff — 2026-11-17

## Current verified website status
- Public entry: https://flowmatic-os.com/demo/
- Public repo: leekj321-cell/Flowmatic; GitHub Pages.
- Current browser demo: separate limited heuristic STEP parser and planner, SVG 2D layout and queue-driven moving workpieces. It is **not** the desktop Flowmatic CAM/3D engine.
- Server: Supabase Edge Function flowmatic-demo-planner (private code).
- Actual desktop footage already hosted: /flowmatic_nc_demo.mp4 and /flowmatic_ct_demo.mp4, now linked in the demo page.

## Coordination boundaries
- Web-side changes belong in /demo/ and website canonical source, NOT the desktop release tree.
- Desktop development owns the real STEP → feature recognition → operation split → toolpath → cell/robot simulation engine.
- Do not overwrite demo/index.html or demo/demo.js without reviewing current live changes.
- Public evidence must distinguish current browser evaluation from real desktop footage; no simulated screenshots labeled as actual engine.
- Never publish proprietary desktop source, confidential CAD, NC posts, credentials or customer files.

## Request for latest desktop development / video producer
1. Confirm newest runnable build and verification status (do not infer release approval from folder names).
2. Capture verified screen footage in independent scenes: (A) stock/product STEP import, (B) auto process and NC/path, (C) cell layout, (D) robot material flow with red workpieces.
3. For each scene, supply exact local file path, duration, screenshot, build ID, and whether it shows real runtime rather than edited animation.
4. Supply a sanitized JSON result contract for browser display: workpiece geometry mesh, operations, toolpaths, machine and robot transforms, material transfer events. Keep engine source server-side.
5. Avoid conflicts with other Flowmatic dot's work on homepage, sales material and demo video. Update this note with actual evidence.

## Acceptance
- Browser video plays on the deployed URL.
- Browser UI clearly shows the same operation labels and moving workpieces as the recorded desktop footage.
- Live STEP upload either returns an engine-derived result or explicitly states the narrower heuristic scope.
- No external pilot/customer claims without evidence.
