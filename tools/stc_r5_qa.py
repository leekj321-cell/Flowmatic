"""Static and browser QA for the Flowmatic STC-lite R5 public homepage.

This replaces the R4-specific first-screen declaration contract as the canonical
homepage regression check. Product/detail pages retain their existing validators.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "2026.09.17-r5-stc"
LANGS = ("ko", "en", "ar")
OUT = ROOT / "qa-artifacts"
OUT.mkdir(exist_ok=True)
REPORT = {
    "release": RELEASE,
    "checks": [],
    "limits": [
        "Author/product review and technical regression, not independent strategy-office approval.",
        "Chromium viewport regression, not physical-device or Safari certification.",
        "Arabic page is technically checked but not native-speaker proofread by this test.",
        "Contact transport is not used to send a real inquiry during QA.",
    ],
}


def check(name: str, ok: bool, detail=None) -> None:
    REPORT["checks"].append({"name": name, "pass": bool(ok), "detail": detail})
    if not ok:
        print("FAIL", name, detail, flush=True)


def soup(text: str) -> BeautifulSoup:
    return BeautifulSoup(text, "html.parser")


def canonical_path(lang: str) -> Path:
    return ROOT / lang / "index.html"


def static_checks() -> None:
    release = json.loads((ROOT / "release.json").read_text(encoding="utf-8"))
    check("release.json identifies STC-lite R5", release.get("release") == RELEASE, release)
    check("release.json declares homepage scope", release.get("scope") == "stc-lite-home", release)

    css = ROOT / "stc-lite-home-v1.css"
    check("STC-lite R5 stylesheet exists", css.exists() and css.stat().st_size > 1000)
    check("canonical build wrapper exists", (ROOT / "tools/build_stc_r5_site.py").exists())

    required_ids = (
        "hero", "journey", "stack", "progressive", "outputs", "loop",
        "proof", "capabilities", "pilot", "company", "contact",
    )
    for lang in LANGS:
        path = canonical_path(lang)
        doc = soup(path.read_text(encoding="utf-8"))
        tag = doc.select_one('meta[name="flowmatic-release"]')
        check(f"{lang}: R5 release marker", bool(tag and tag.get("content") == RELEASE))
        check(f"{lang}: correct document language", doc.html.get("lang") == lang)
        check(f"{lang}: single product H1", len(doc.select("h1")) == 1)
        check(f"{lang}: STC stylesheet linked", bool(doc.select_one('link[href*="stc-lite-home-v1.css"]')))
        check(f"{lang}: six-item customer navigation", len(doc.select(".site-nav a")) == 6)
        missing = [section_id for section_id in required_ids if not doc.find(id=section_id)]
        check(f"{lang}: complete STC-lite homepage sequence", not missing, missing)

        check(f"{lang}: one-drawing compiler has eight output nodes", len(doc.select("#hero .stc-flow-node")) == 8)
        check(f"{lang}: one-drawing journey has eight steps", len(doc.select("#journey .stc-step")) == 8)
        check(f"{lang}: comparison has two six-layer stacks", len(doc.select("#stack .stc-stack-card")) == 2 and len(doc.select("#stack .stc-layer")) == 12)
        flow = doc.select_one("#stack .stc-stack-card.flow")
        check(
            f"{lang}: Flowmatic stack marks L3-L6 core and L1-L2 optional",
            bool(flow and len(flow.select(".stc-layer.core")) == 4 and len(flow.select(".stc-layer.optional")) == 2),
        )
        check(f"{lang}: human-to-automation bridge has ten entries", len(doc.select("#progressive .stc-fallback-item")) == 10)
        check(f"{lang}: customer outputs are eight deliverables", len(doc.select("#outputs .stc-output")) == 8)
        check(f"{lang}: closed loop has four stages", len(doc.select("#loop .stc-loop article")) == 4)
        check(f"{lang}: current proof contains two concrete demonstrations", len(doc.select("#proof .stc-proof")) == 2)
        check(f"{lang}: public NC proof stays linked", bool(doc.select_one(f'#proof a[href="/{lang}/nc/"]')))
        check(f"{lang}: CT proof keeps real video source", bool(doc.select_one('#proof video source[src="/flowmatic_ct_demo.mp4"]')))

        body_text = doc.body.get_text(" ", strip=True)
        check(f"{lang}: target/working boundary is explicit", "STC-lite Full target" in body_text and "WORKING" in body_text)
        check(f"{lang}: L1-L6 model disclaimer exists", "ISA-95" in body_text)
        check(f"{lang}: old R4 declaration is no longer the H1", "Elegant Engineering." not in doc.h1.get_text(" "))

        primary = doc.select_one("#hero .stc-actions a.primary")
        secondary = doc.select_one("#hero .stc-actions a:not(.primary)")
        check(f"{lang}: hero primary CTA requests factory review", bool(primary and primary.get("href") == "#contact"))
        check(f"{lang}: hero secondary CTA leads to proof", bool(secondary and secondary.get("href") == "#proof"))

        if lang == "ar":
            check("ar: RTL document", doc.html.get("dir") == "rtl")
        else:
            check(f"{lang}: LTR document", doc.html.get("dir") == "ltr")

    root_doc = soup((ROOT / "index.html").read_text(encoding="utf-8"))
    ko_doc = soup((ROOT / "ko/index.html").read_text(encoding="utf-8"))
    check("root is Korean canonical STC-lite home", root_doc.h1.get_text(" ", strip=True) == ko_doc.h1.get_text(" ", strip=True))

    for relative in ("ko/nc/index.html", "ko/ct/index.html", "ko/platform/index.html"):
        check(f"legacy/detail route preserved: {relative}", (ROOT / relative).exists())


def _serve_local() -> tuple[ThreadingHTTPServer, str]:
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(ROOT), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def browser_checks(base: str) -> None:
    from playwright.sync_api import sync_playwright

    viewports = ((360, 800), (390, 844), (768, 1024), (1440, 900))
    errors: list[str] = []
    http_errors: list[tuple[int, str]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH"))
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
        page = ctx.new_page()
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("response", lambda response: http_errors.append((response.status, response.url)) if response.status >= 400 else None)

        for lang in LANGS:
            url = base.rstrip("/") + f"/{lang}/"
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(350)
            check(f"{lang}: served official R5 marker", page.locator('meta[name="flowmatic-release"]').get_attribute("content") == RELEASE)
            for width, height in viewports:
                page.set_viewport_size({"width": width, "height": height})
                page.evaluate("scrollTo({top:0,behavior:'instant'})")
                page.wait_for_timeout(120)
                metrics = page.evaluate("({scroll:document.documentElement.scrollWidth,width:innerWidth})")
                check(f"{lang}: no horizontal overflow {width}", metrics["scroll"] <= width + 1, metrics)
                h1 = page.locator("#hero h1")
                check(f"{lang}: hero H1 visible {width}", h1.is_visible())
                check(f"{lang}: two stack cards render {width}", page.locator("#stack .stc-stack-card").count() == 2)
                if width in (390, 1440):
                    page.screenshot(path=str(OUT / f"{lang}-stc-r5-{width}.png"), full_page=True)

            page.locator('#hero a[href="#contact"]').click()
            check(f"{lang}: primary CTA reaches contact", urlsplit(page.url).fragment == "contact")
            page.locator('#hero a[href="#proof"]').click()
            check(f"{lang}: secondary CTA reaches proof", urlsplit(page.url).fragment == "proof")

        browser.close()

    check("browser runtime has no page errors", not errors, errors)
    relevant_http = [(status, url) for status, url in http_errors if not any(x in url for x in ("formspree", "favicon"))]
    check("browser runtime has no relevant HTTP errors", not relevant_http, relevant_http)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", action="store_true")
    parser.add_argument("--base", default="")
    args = parser.parse_args()

    static_checks()
    server = None
    try:
        if args.browser:
            if args.base:
                base = args.base
            else:
                server, base = _serve_local()
            browser_checks(base)
    finally:
        if server is not None:
            server.shutdown()

    (OUT / "stc-r5-qa.json").write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding="utf-8")
    failures = [item for item in REPORT["checks"] if not item["pass"]]
    print(f"STC-lite R5 QA: {len(REPORT['checks']) - len(failures)}/{len(REPORT['checks'])} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
