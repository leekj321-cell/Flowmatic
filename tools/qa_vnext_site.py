"""Static regression checks for the generated Flowmatic V.Next site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
LANGS = {"ko": "ltr", "en": "ltr", "ar": "rtl"}
PAGES = ("", "quality", "machining-intelligence", "operations-intelligence", "logistics-intelligence", "platform")
COMPAT = ("nc.html", "ct.html", "quality.html", "work-standard.html", "tms.html", "amr.html")
FORBIDDEN = ("v0.5.13", "QUALITY_V513", "Production Ready", "production certified", "Production Certified")


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.lang = ""
        self.direction = ""
        self.title = False
        self.description = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang") or ""
            self.direction = values.get("dir") or ""
        if tag == "title":
            self.title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description = True
        for key in ("href", "src", "srcset"):
            value = values.get(key)
            if value:
                self.links.append((key, value.split()[0]))


def generated_pages() -> list[Path]:
    pages = [ROOT / "index.html"] + [ROOT / item for item in COMPAT]
    for lang in LANGS:
        pages.extend(ROOT / lang / (page or "index.html") / ("index.html" if page else "") for page in PAGES)
    return [Path(str(page).rstrip("\\/")) for page in pages]


def local_target(value: str) -> Path | None:
    if value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = parsed.path
    if not path:
        return None
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target /= "index.html"
    return target


def main() -> None:
    errors: list[str] = []
    pages = generated_pages()
    for page in pages:
        if not page.exists():
            errors.append(f"missing page: {page.relative_to(ROOT)}")
            continue
        text = page.read_text(encoding="utf-8")
        scan = Scan()
        scan.feed(text)
        language = page.relative_to(ROOT).parts[0] if page.relative_to(ROOT).parts else "ko"
        if language in LANGS:
            if scan.lang != language or scan.direction != LANGS[language]:
                errors.append(f"language metadata: {page.relative_to(ROOT)}")
        if not scan.title or not scan.description:
            errors.append(f"metadata missing: {page.relative_to(ROOT)}")
        for _, value in scan.links:
            target = local_target(value)
            if target is not None and not target.exists():
                errors.append(f"broken asset/link: {page.relative_to(ROOT)} -> {value}")

    source_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (ROOT / "build_site.py", ROOT / "factory_os_v2.py")
    )
    generated_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in pages if path.exists())
    for phrase in FORBIDDEN:
        if phrase.lower() in (source_text + generated_text).lower():
            errors.append(f"outdated or prohibited phrase: {phrase}")

    for lang in LANGS:
        home = (ROOT / lang / "index.html").read_text(encoding="utf-8")
        required = ("class=\"transformation\"", "class=\"before-after", "class=\"what-changes", "Platform / Control Tower")
        for phrase in required:
            if phrase not in home:
                errors.append(f"home content missing ({lang}): {phrase}")
        machining = (ROOT / lang / "machining-intelligence" / "index.html").read_text(encoding="utf-8")
        for phrase in ("Manufacturing Recipe", "INFERRED", "USER CONFIRMED", "Managed Metadata Comment Block", "Conflict review", "fail-closed"):
            if phrase not in machining:
                errors.append(f"machining content missing ({lang}): {phrase}")

    if errors:
        print("STATUS: FAIL")
        print("\n".join(f"- {item}" for item in sorted(set(errors))))
        raise SystemExit(1)
    print(f"STATUS: PASS ({len(pages)} generated pages checked)")


if __name__ == "__main__":
    main()
