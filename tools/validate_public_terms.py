#!/usr/bin/env python3
"""Check published surfaces for retired internal names and PDF terminology.

Usage (the scan is anchored to this script's repository):
    python tools/validate_public_terms.py
    python tools/validate_public_terms.py --self-test

The default audit is read-only and fails on missing inputs or dependencies.
It checks HTML source, decoded text and attributes; public release/provenance
JSON; all PDF text pages and metadata; and English OCR of product PNGs.
OCR is a heuristic, not Korean OCR or a visual-completeness check. In
particular, Korean text in image pixels and missing PDF previews still need
visual review. Source code and internal QA output are outside this scan.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
# ASCII alphanumeric boundaries avoid ASTC/STC2 false positives while treating
# Korean particles, hyphens and underscores as delimiters in public labels.
FORBIDDEN = (
    ("internal product name", re.compile(r"(?<![A-Za-z0-9])stc(?:[-_\s]*lite)?(?![A-Za-z0-9])", re.I)),
    ("retired shape label", re.compile(r"가시\s*외형")),
)
EXCLUDED_DIRS = frozenset({
    "preview-dist", "qa-artifacts", "git", "__pycache__", "node_modules",
    "tools", "tests", "content", "flowmatic_core", "solution-compiler",
    "vendor", "venv", "env",
})
REQUIRED_HTML = (
    "index.html", "ko/index.html", "en/index.html", "ar/index.html",
    "amr.html", "ct.html", "nc.html", "quality.html", "tms.html",
    "work-standard.html",
)
REQUIRED_HTML_DIRS = ("ko", "en", "ar", "html-vnext")
PRODUCT_DIRS = (
    "media/product-20261018", "media/product-20261020", "media/product-20261102",
)
PDF_FILES = (
    "media/product-20261020/synthetic-work-standard.pdf",
    "media/product-20261102/synthetic-work-standard.pdf",
)
BLOCK_TAGS = frozenset({
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
    "dt", "fieldset", "figcaption", "figure", "footer", "form", "h1",
    "h2", "h3", "h4", "h5", "h6", "header", "hr", "li", "main", "nav",
    "ol", "p", "pre", "section", "table", "td", "th", "tr", "ul",
    "head", "title", "body", "script", "style", "noscript", "template",
})


class PublicHTML(HTMLParser):
    """Keep hidden text/attributes too; they are still delivered publicly."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.attributes: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in BLOCK_TAGS:
            self.text.append("\n")
        for name, value in attrs:
            if value is not None:
                self.attributes.append((f"attribute {tag}@{name}", value))

    def handle_endtag(self, tag: str) -> None:
        if tag in BLOCK_TAGS:
            self.text.append("\n")

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def html_parts(raw: str) -> list[tuple[str, str]]:
    parser = PublicHTML()
    parser.feed(raw)
    parser.close()
    return [
        ("raw HTML", raw),
        ("entity-decoded HTML", html.unescape(raw)),
        ("parsed text", "".join(parser.text)),
        *parser.attributes,
    ]


def term_hits(value: str, *, english_only: bool = False):
    value = unicodedata.normalize("NFKC", value)
    for label, pattern in FORBIDDEN[:1] if english_only else FORBIDDEN:
        match = pattern.search(value)
        if match:
            snippet = re.sub(r"\s+", " ", value[max(0, match.start() - 55):match.end() + 95]).strip()
            yield label, snippet


def public_files(root: Path):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS)
        for name in sorted(names):
            if not name.startswith("."):
                yield Path(base) / name


def json_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from json_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from json_strings(child)


class Audit:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.seen: set[tuple[str, str]] = set()
        self.counts = {"HTML": 0, "JSON": 0, "PDF": 0, "PNG": 0}

    def name(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def fail(self, path: Path | str, channel: str, message: str) -> None:
        name = self.name(path) if isinstance(path, Path) else path
        self.errors.append(f"{name} [{channel}]: {message}")

    def scan(self, path: Path, channel: str, value: str, *, english_only: bool = False) -> None:
        for label, snippet in term_hits(value, english_only=english_only):
            key = (self.name(path), label)
            if key not in self.seen:
                self.seen.add(key)
                self.fail(path, channel, f"{label}: {snippet}")

    def require_file(self, path: Path) -> bool:
        if not path.is_file():
            self.fail(path, "input", "required file is missing")
            return False
        return True

    def read(self, path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.fail(path, "read", str(exc))
            return None

    def command(self, path: Path, channel: str, command: list[str]) -> str | None:
        try:
            result = subprocess.run(command, capture_output=True, encoding="utf-8", errors="strict", timeout=60)
        except (OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
            self.fail(path, channel, str(exc))
            return None
        if result.returncode:
            detail = re.sub(r"\s+", " ", result.stderr).strip()[:220]
            self.fail(path, channel, f"command exited {result.returncode}: {detail}")
            return None
        return result.stdout

    def check_html(self, path: Path) -> None:
        raw = self.read(path)
        if raw is None:
            return
        self.counts["HTML"] += 1
        if not raw.strip():
            self.fail(path, "HTML", "empty public HTML")
        try:
            for channel, value in html_parts(raw):
                self.scan(path, channel, value)
        except Exception as exc:
            self.fail(path, "HTML parser", str(exc))

    def check_json(self, path: Path) -> None:
        if not self.require_file(path):
            return
        raw = self.read(path)
        if raw is None:
            return
        self.counts["JSON"] += 1
        self.scan(path, "raw JSON", raw)
        try:
            data = json.loads(raw)
        except ValueError as exc:
            self.fail(path, "JSON parser", str(exc))
            return
        for value in json_strings(data):
            self.scan(path, "decoded JSON", value)
        if path.name == "provenance.json" and isinstance(data, dict):
            assets = data.get("assets", [])
            if not isinstance(assets, list):
                self.fail(path, "provenance", "assets must be a list when present")
                return
            for asset in assets:
                if isinstance(asset, dict) and isinstance(asset.get("file"), str):
                    self.require_file(path.parent / asset["file"])

    def check_pdf(self, path: Path, binaries: dict[str, str | None]) -> None:
        if not self.require_file(path):
            return
        if not binaries["pdftotext"] or not binaries["pdfinfo"]:
            return
        self.counts["PDF"] += 1
        extracted = self.command(path, "PDF text", [binaries["pdftotext"], "-enc", "UTF-8", "-layout", str(path), "-"])
        info = self.command(path, "PDF metadata", [binaries["pdfinfo"], "-enc", "UTF-8", str(path)])
        xmp = self.command(path, "PDF XMP", [binaries["pdfinfo"], "-meta", str(path)])
        if extracted is not None:
            if not extracted.replace("\f", "").strip():
                self.fail(path, "PDF text", "empty extraction; text-layer coverage is unavailable")
            self.scan(path, "PDF text, all pages", extracted)
        if info is not None:
            if not info.strip():
                self.fail(path, "PDF metadata", "empty pdfinfo output")
            self.scan(path, "PDF metadata", info)
        if xmp is not None:
            self.scan(path, "PDF XMP", html.unescape(xmp))
        if extracted is not None and info is not None:
            page_count = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
            pages = extracted.split("\f")
            if pages and not pages[-1].strip():
                pages.pop()
            if not page_count or len(pages) != int(page_count.group(1)):
                self.fail(path, "PDF pages", "extracted page count does not match pdfinfo")
            elif any(not page.strip() for page in pages):
                empty = ", ".join(str(i + 1) for i, page in enumerate(pages) if not page.strip())
                self.fail(path, "PDF pages", f"no extractable text on page(s) {empty}; cannot certify term coverage")

    def check_png(self, path: Path, tesseract: str | None) -> None:
        if tesseract is None:
            return
        self.counts["PNG"] += 1
        has_text = False
        # Sparse-text mode complements automatic page segmentation for small
        # Latin labels embedded in otherwise Korean product interfaces.
        for psm in (3, 11):
            output = self.command(path, f"English OCR psm={psm}", [tesseract, str(path), "stdout", "-l", "eng", "--psm", str(psm)])
            if output is not None:
                has_text |= bool(output.strip())
                self.scan(path, f"English OCR psm={psm}", output, english_only=True)
        if not has_text:
            self.fail(path, "English OCR", "empty OCR output; name coverage is unavailable")


def self_test() -> int:
    positives = ("STC", "stc", "StC-LiTe", "stc_lite", "STClite", "STC로", "/stc-lite-home.css", "build_stc_r5_site.py", "가시외형", "가시 \n\t외형", "가시\u00a0외형")
    negatives = ("ASTC", "STC2", "DISTRICT", "mystcfield", "가시성", "외형 보기", "NC revision R3 / CNC01 / 합성 시험 / 검토 필요", 'rel="manifest"')
    failures = [f"missed positive: {value!r}" for value in positives if not list(term_hits(value))]
    failures += [f"false positive: {value!r}" for value in negatives if list(term_hits(value))]
    documents = (
        ('<div hidden aria-label="sTc-Lite">안내</div>', "attribute div@aria-label"),
        ('<img alt="&#83;&#84;&#67;">', "attribute img@alt"),
        ('<meta content="가시&#32;외형">', "attribute meta@content"),
        ("<span>S</span><span>TC</span>", "parsed text"),
        ("<span>가시</span> <span>외형</span>", "parsed text"),
    )
    for raw, expected_channel in documents:
        if not any(channel == expected_channel and list(term_hits(value)) for channel, value in html_parts(raw)):
            failures.append(f"missed HTML channel: {expected_channel}")
    safe = "<p>S</p><p>TC</p><img alt='ASTC STC2 NC R3'><p>합성 시험 · 검토 필요</p>"
    if any(list(term_hits(value)) for _, value in html_parts(safe)):
        failures.append("false positive across separate blocks or safe attributes")
    escaped_json = json.loads(r'{"product":"\u0053\u0054\u0043-lite"}')
    if not any(list(term_hits(value)) for value in json_strings(escaped_json)):
        failures.append("missed JSON Unicode escape")
    for failure in failures:
        print(f"FAIL self-test: {failure}", file=sys.stderr)
    print(f"Public-term self-test: {'FAIL' if failures else 'PASS'}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this script's repository)")
    parser.add_argument("--self-test", action="store_true", help="test matching/HTML parsing only; do not scan files or run OCR")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    root = args.root.resolve()
    audit = Audit(root)
    if not root.is_dir():
        audit.fail("repository", "input", f"missing directory: {root}")
        files = []
    else:
        files = list(public_files(root))
    html_files = [p for p in files if p.suffix.lower() in {".html", ".htm"}]
    for required in REQUIRED_HTML:
        audit.require_file(root / required)
    for directory in REQUIRED_HTML_DIRS:
        if not any((root / directory) in p.parents for p in html_files):
            audit.fail(directory, "HTML", "required public HTML directory is missing or empty")
    for path in html_files:
        audit.check_html(path)
    metadata = {root / "release.json"}
    metadata.update(p for p in files if p.name == "provenance.json" and "media" == p.relative_to(root).parts[0])
    metadata.update(root / directory / "provenance.json" for directory in PRODUCT_DIRS)
    for path in sorted(metadata):
        audit.check_json(path)
    binaries = {name: shutil.which(name) for name in ("pdftotext", "pdfinfo", "tesseract")}
    for name, executable in binaries.items():
        if executable is None:
            audit.fail(name, "dependency", "required executable is missing")
    tesseract = binaries["tesseract"]
    if tesseract:
        languages = audit.command(root / "media", "OCR language availability", [tesseract, "--list-langs"])
        if languages is None or "eng" not in {line.strip() for line in languages.splitlines()}:
            audit.fail("tesseract", "dependency", "required eng language data is unavailable")
            tesseract = None
    for filename in PDF_FILES:
        audit.check_pdf(root / filename, binaries)
    for directory in PRODUCT_DIRS:
        path = root / directory
        pngs = sorted(p for p in files if path in p.parents and p.suffix.lower() == ".png")
        if not path.is_dir() or not pngs:
            audit.fail(directory, "PNG", "required product image directory is missing or has no PNGs")
        for png in pngs:
            audit.check_png(png, tesseract)
    for error in audit.errors:
        print(f"FAIL {error}", file=sys.stderr)
    counts = ", ".join(f"{count} {kind}" for kind, count in audit.counts.items())
    print(f"Public-term audit: {'FAIL' if audit.errors else 'PASS'} ({counts}; {len(audit.errors)} issue(s))")
    print("Coverage limit: English OCR is heuristic. No Korean pixel-text or visual/PDF-preview completeness validation is claimed.")
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
