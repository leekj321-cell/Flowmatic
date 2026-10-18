# Website release 2026.10.18-r7-product-scroll

The owner approved the 18 October investor HTML preview and authorized PC/mobile and Korean, English and Arabic deployment, including automatic 01–04 transitions linked to native scrolling.

## Source and build

`content/investor_home.py` contains the Korean source copy and equivalent English/Arabic versions. `tools/build_investor_home.py` generates the three locale homes, root redirect and release marker. The canonical command remains `python tools/build_stc_r5_site.py`: it rebuilds legacy detail pages, generates the current homes, and preserves these notes. Do not run the legacy builder as a release command.

## Presentation and interaction

The approved actual-product hero replaces the former target-loop illustration. Four unmodified product captures in `media/product-20261018/` illustrate process review, logistics planning, layout approval and production operations. Native page scrolling updates the visible capture and selected step in both directions. Numbered anchors and keyboard controls remain available. Focus never changes merely because the page scrolls. Mobile uses a compact sticky preview; short viewports and no-JavaScript browsers show inline images for all steps.

## Evidence and retained concepts

Captures are internal demonstrations, not customer results. Logistics is a separate simulation; the throughput values and utilization shown in the screenshots are qualified in the adjacent text. Supported geometry, human approval and field validation limits are localized. The global Factory OS loop and L1–L6 adoption comparison remain explicitly TARGET. CURRENT / PILOT / TARGET, Design → Build → Run → Improve, user/budget-owner roles, one-product/one-line 4–8 week pilot, baseline/KPI/ROI, and proposed subscription/expansion model remain visible.

Canonical KO/global brand bytes, existing NC/CT detail routes, CT video and contact endpoint are preserved. Product screenshots retain their original Korean UI in every locale, with a translated note explaining this.

## Verification

`python tools/stc_r5_qa.py --browser` checks static structure, original image hashes, forward/reverse scrolling, manual and keyboard selection, original-image zoom, reduced motion, mobile menus, RTL, direct links, no-JavaScript content, contact behavior via interception, and viewport overflow. GitHub Actions runs local and official-domain Chromium checks. Physical-device/Safari certification and native Arabic proofreading are outside this check. No real inquiry is submitted during QA.

The source of the previous live release is commit 9071f9f4323ee71b69806e16cdfae45abb1a9700, available for rollback.
