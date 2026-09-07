# Interactive NC viewer

The updated NC page opens on a working 3D viewer. Its scope is local file
loading, orbit/zoom/pan, tool parsing and selection, previous/next tool, rapid
visibility, and a diameter-sized tool circle. Tool diameter can be read from an
NC comment or entered per tool. The value changes the world-space diameter of
the circle, not a fixed pixel size. An unknown diameter has no invented circle.
The existing theoretical-time analysis is retained in a disclosure below it.

## Source reuse

`nc-viewer-core.js` is a **browser port of selected native Viewer functions**,
not the Python/Qt application running in the browser and not the full native
parser. Its source baseline is:

- Repository: `leekj321-cell/flowmatic-nc`
- Commit: `2efd5cbc9df42de084dc928d4464df612d7640a1`
- File: `flowmatic_mi/engines/nc_analysis.py`
- Git blob: `35209a37825269c9d3366010a47ab54d90e0a30e`
- Ported behavior: `normalize_tool_name`, `extract_tool_info`,
  `make_arc_ij_points`, `make_arc_r_points`, and the separation of cycle
  positioning, cutting and rapid return.

`tests/fixtures/nc-native-viewer.json` was produced by executing that retrieved
Python module. It contains synthetic tool-comment examples and native point
coordinates for IJ, helical, full-circle, positive-R and negative-R arcs.
Parity tests compare the browser output with those results. The public input
adapter additionally handles inch/incremental coordinates, T preselection and
unknown starting coordinates explicitly. It is not claimed to have full native
controller/profile parity.

Rendering uses the locally vendored Three.js 0.180.0 and OrbitControls. The only
upstream edit is the OrbitControls import path to the local Three module.
When WebGL is unavailable, a Canvas line renderer projects the same scene
through the same 3D camera. Tool selection, picking, rotation, zoom and physical
diameter sizing share the same controls and world coordinates in both renderers.
The upstream license is in `vendor/three/LICENSE`. No external CDN or server
parser is required. No generator, recipe inference, measurement, compensation,
customer source file or private native engine bundle is included.

## Input and display boundary

- Text `.nc`, `.cnc`, `.tap`, `.txt`, `.min`, and extensionless `O` numbers.
  UTF-8 and Korean encodings are decoded locally. Binary/encoded `.tc` machine
  containers require export as text NC; ZIP archives require extraction.
- G0/G1, IJ and signed-R G2/G3 in G17/G18/G19; G20/G21 and G90/G91.
- G10 register writes do not generate toolpath. Machine work-offset registers
  are not applied; views use program coordinates and break links at WCS changes.
- G100 tool positioning, basic drill/tap cycles, and G98/G99 return are handled.
  G73/G83 display the depth envelope; intermediate pecks are explicitly omitted.
- Known arithmetic, assigned constants, G52 shifts and constant absolute XY G68
  rotations are supported. Unknown variables/transform states create exclusions.
- G28/G30/G53 moves invalidate affected coordinates. Unexpanded subprogram calls
  create gaps; motion resumes only after all coordinates are re-established.
  Unresolved control flow stops parsing. Multiple standalone programs are not
  concatenated into a fabricated continuous path.
- Auxiliary M functions are reported and not simulated. Indexing breaks the
  path connection; fixtures and rotary frames are not registered to one model.
  Simultaneous rotary machining and unsupported G commands are excluded.
- Compensation commands show programmed centerline coordinates, with a review
  message. This is not machine collision, compensated-cutting or PLC validation.
- Limits: 5 MiB / 100,000 lines / 250,000 displayed segments. Exclusions are
  summarized with source lines and repeated-condition counts.

The UI follows the native Viewer reference: black viewport, G-code List,
Current Tool / Motion, rapid toggle, Prev Tool / Next Tool and Tool Console.
The mobile layout puts file buttons, viewport and tool navigation first.
The code list is virtualized; clicking a path or code row links the selection.
A missing diameter produces no invented circle. Unrecognized tool descriptions
may be preserved literally rather than assigned a guessed tool type.

## Structure and maintenance

- `nc-viewer-core.js`: public parsing, geometry and marker-circle calculations.
- `nc-viewer-3d.js`: Three scene, camera, picking, tool and diameter controls.
- `nc-viewer-canvas.js`: line-only 3D rendering when WebGL is unavailable.
- `nc-viewer-3d.css`: responsive desktop/touch workspace.
- `nc_viewer_section.py`: Korean, English and Arabic viewer markup.
- `nc-demo-lite-worker.js`: existing local analysis plus the new scene result.
- `nc-demo-lite.js`: file input and result events; outdated requests cannot
  restore a previous file after reset or a newer selection.
- `build_site.py`: all four NC routes are generated from these shared sources.

Refresh the NC routes with the existing generator. A change to renderer,
worker or core should also advance their cache-version query parameters.

## Validation in this change

`node --test tests/nc-viewer.test.cjs`: **19 passing tests**, including the
executed native function parity fixtures, physical diameter scale, tool
preselection, units, arc planes, cycles, setup registers, safe arithmetic,
coordinate shifts, known rotation, unexpanded-call gaps and file boundaries.
All fixtures committed to this repository are synthetic.

JavaScript and Python syntax checks pass. The brand contract validates all
nine canonical assets. Four NC routes use versioned local asset references.

Private attachment batch: 240 NC-type files parsed without thrown errors;
219 produced geometry and 21 produced no displayable path, including reference
and utility routines or subprograms without full starting coordinates. This is
an ingestion/geometry test, not a claim that all machining moves were verified.
214 machine-container files and four drawings are outside that parser count.
Customer data and the private standalone sample are not committed here.

Browser QA used 360×740 and 393×852 iframe viewports in desktop Chromium,
with WebGL unavailable and the Canvas renderer active. Checks covered initial
loading of a supplied program, file input with a second supplied program,
previous/next tool, rapid visibility, diameter editing, code selection,
rotation, top view, zoom buttons and reset/sample restoration. Page widths
fit the mobile viewport without horizontal overflow.

This is responsive-layout QA, not an Android/iOS device test. Native phone
file opening, content/file URL handling, real multi-touch gestures and GPU
rendering remain unverified. A prior automated wheel gesture timed out.

The private review HTML is self-contained, with inline renderer, core, NC
sample and canonical CI. It schedules local parsing on the main thread,
removing the previous Blob Worker requirement. Its CSP blocks network and
worker creation. It was exercised through the internal HTTP preview, not a
phone's file manager or an attachment preview. The multilingual release is deployed through the existing GitHub Pages site after approval.

## Public release data policy

The public site opens with no NC file loaded. The sample button loads only
`demo-data/flowmatic-nc-sample.nc`, an independently authored three-tool example
with a synthetic-data marker. Shop programs, uploaded drawings and private
standalone review HTML are excluded from this repository and release.

`python3 tools/validate_nc_public_release.py` checks the allowed NC asset and its
pinned checksum, excludes private review filenames, and checks the English and
Arabic viewer markup for untranslated Korean. The existing validation workflow
also runs this check and the NC regression suite. A separate pre-release scan
compares outgoing Git objects with the supplied attachment fingerprints.

The Viewer controls, motion labels and review messages are localized in Korean,
English and Arabic. Arabic NC code retains left-to-right direction within the
right-to-left interface. Public-page browser checks exercised the synthetic
example through the site's local worker and local module assets.
