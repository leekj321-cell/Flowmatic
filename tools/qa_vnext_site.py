"""Static regression checks for the generated Flowmatic V.Next site."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
LANGS = {"ko": "ltr", "en": "ltr", "ar": "rtl"}
PAGES = ("", "quality", "machining-intelligence", "operations-intelligence", "logistics-intelligence", "platform")
COMPAT = ("nc.html", "ct.html", "quality.html", "work-standard.html", "tms.html", "amr.html")
FORBIDDEN = ("v0.5.13", "QUALITY_V513", "Production Ready", "production certified", "Production Certified")
V156_MARKERS = (
    'id="field-problem"',
    'id="architecture"',
    'id="modules"',
    'id="solutions"',
    "Manufacturing Context",
    "Engine Pool",
    "Module Pool",
    "Event Bus",
    "Audit",
    "153 / 153 PASS",
    "GUI/OpenGL",
    "Candidate",
)
V156_LEGACY = (
    "Shared context → Event Core → Control Tower",
    "Shared Manufacturing Context → Event Core",
    "Event Core & Control Tower Architecture",
    "00_factory_os_four_axes",
)
BRAND_HERO_LINES = (
    "Elegant Engineering.",
    "Intelligent Operations.",
    "Flowmatic.",
)


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.lang = ""
        self.direction = ""
        self.title = False
        self.description = False
        self.module_cards = 0
        self.source_nodes: list[tuple[str, str]] = []
        self.solution_nodes: list[str] = []
        self.statuses: Counter[str] = Counter()
        self.hero_titles: list[list[str]] = []
        self._hero_title_depth = 0
        self._hero_title_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang") or ""
            self.direction = values.get("dir") or ""
        if tag == "title":
            self.title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.description = True
        if tag == "h1" and values.get("id") == "hero-title":
            self._hero_title_depth = 1
            self._hero_title_parts = []
        elif self._hero_title_depth:
            self._hero_title_depth += 1
        classes = set((values.get("class") or "").split())
        if "module-card" in classes:
            self.module_cards += 1
            status = values.get("data-status")
            if status:
                self.statuses[status] += 1
        if "source-node" in classes:
            self.source_nodes.append((values.get("data-source") or "", values.get("data-solutions") or ""))
        if "solution-card" in classes:
            self.solution_nodes.append(values.get("data-solution") or "")
        for key in ("href", "src", "srcset"):
            value = values.get(key)
            if value:
                self.links.append((key, value.split()[0]))

    def handle_endtag(self, tag: str) -> None:
        if not self._hero_title_depth:
            return
        self._hero_title_depth -= 1
        if self._hero_title_depth == 0 and self._hero_title_parts is not None:
            self.hero_titles.append(self._hero_title_parts)
            self._hero_title_parts = None

    def handle_data(self, data: str) -> None:
        if self._hero_title_parts is None:
            return
        value = " ".join(data.split())
        if value:
            self._hero_title_parts.append(value)


def generated_pages() -> list[Path]:
    pages = [ROOT / "index.html"] + [ROOT / item for item in COMPAT]
    for lang in LANGS:
        pages.extend(ROOT / lang / (page or "index.html") / ("index.html" if page else "") for page in PAGES)
    return [Path(str(page).rstrip("\\/")) for page in pages]


def v156_pages() -> list[Path]:
    return [
        ROOT / "index.html",
        *(ROOT / lang / "index.html" for lang in LANGS),
        *(ROOT / lang / "platform" / "index.html" for lang in LANGS),
    ]


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

    for page in v156_pages():
        if not page.exists():
            continue
        label = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8")
        scan = Scan()
        scan.feed(text)

        for marker in V156_MARKERS:
            if marker not in text:
                errors.append(f"V156 content missing ({label}): {marker}")
        if "headless" not in text.lower():
            errors.append(f"V156 headless evidence missing ({label})")
        if scan.module_cards != 12:
            errors.append(f"V156 module card count ({label}): expected 12, got {scan.module_cards}")
        if len(scan.source_nodes) != 12:
            errors.append(f"V156 source node count ({label}): expected 12, got {len(scan.source_nodes)}")
        if len(scan.solution_nodes) != 4:
            errors.append(f"V156 solution card count ({label}): expected 4, got {len(scan.solution_nodes)}")

        expected_statuses = Counter({"v156": 7, "existing": 3, "target": 2})
        if scan.statuses != expected_statuses:
            errors.append(f"V156 status counts ({label}): expected 7/3/2, got {dict(scan.statuses)}")

        source_ids = [source_id for source_id, _ in scan.source_nodes]
        if not all(source_ids) or len(set(source_ids)) != len(source_ids):
            errors.append(f"V156 source IDs missing or duplicated ({label})")
        solution_ids = [solution_id for solution_id in scan.solution_nodes if solution_id]
        if len(solution_ids) != 4 or len(set(solution_ids)) != 4:
            errors.append(f"V156 solution IDs missing or duplicated ({label})")
        valid_solutions = set(solution_ids)
        for source_id, memberships in scan.source_nodes:
            linked = set(memberships.split())
            if not linked or not linked <= valid_solutions:
                errors.append(f"V156 source mapping invalid ({label}): {source_id or '<missing>'}")

        if "[('machining'" in text or "[(&#x27;machining&#x27;" in text:
            errors.append(f"raw Python navigation tuple leaked ({label})")
        for lang in LANGS:
            if f"/{lang}/contact/" in text:
                errors.append(f"obsolete contact route ({label}): /{lang}/contact/")
        for phrase in V156_LEGACY:
            if phrase.lower() in text.lower():
                errors.append(f"legacy platform positioning ({label}): {phrase}")

    for lang in LANGS:
        home = (ROOT / lang / "index.html").read_text(encoding="utf-8")
        home_scan = Scan()
        home_scan.feed(home)
        required = ('class="transformation"', "Platform / Engine-Module Composition")
        for phrase in required:
            if phrase not in home:
                errors.append(f"home content missing ({lang}): {phrase}")
        if home_scan.hero_titles != [list(BRAND_HERO_LINES)]:
            errors.append(f"fixed brand slogan mismatch ({lang}): {home_scan.hero_titles}")
        machining = (ROOT / lang / "machining-intelligence" / "index.html").read_text(encoding="utf-8")
        for phrase in ("Manufacturing Recipe", "INFERRED", "USER CONFIRMED", "Managed Metadata Comment Block", "Conflict review", "fail-closed"):
            if phrase not in machining:
                errors.append(f"machining content missing ({lang}): {phrase}")

    root_home = (ROOT / "index.html").read_text(encoding="utf-8")
    root_scan = Scan()
    root_scan.feed(root_home)
    if root_scan.hero_titles != [list(BRAND_HERO_LINES)]:
        errors.append(f"fixed brand slogan mismatch (index.html): {root_scan.hero_titles}")

    ko_home = (ROOT / "ko" / "index.html").read_text(encoding="utf-8")
    for phrase in ("Machining · Recipe", "Machining · Safety Contract", "Machining · V.Next scope", "deterministic source test", "prototype integration"):
        if phrase in ko_home:
            errors.append(f"Korean evidence contains internal memo wording: {phrase}")

    script = (ROOT / "script.js").read_text(encoding="utf-8")
    stylesheet = (ROOT / "style-v5.20.css").read_text(encoding="utf-8")
    if "initEvidenceSequence();" not in script or ".evidence-card.is-scroll-active" not in stylesheet:
        errors.append("evidence scroll highlight wiring missing")
    js_markers = (
        "function initV156Convergence()",
        "initV156Convergence();",
        ".v156-platform [data-convergence]",
        "source.dataset.solutions",
    )
    for marker in js_markers:
        if marker not in script:
            errors.append(f"V156 convergence wiring missing: {marker}")

    for selector in ("module-card", "solution-card", "convergence-field"):
        scoped_rule = rf"\.v156-platform[^{{}}]*\.{re.escape(selector)}[^{{}}]*\{{"
        if not re.search(scoped_rule, stylesheet):
            errors.append(f"V156 scoped CSS missing: {selector}")
    if "@media (max-width: 1100px)" not in stylesheet:
        errors.append("V156 tablet/mobile breakpoint missing")

    if errors:
        print("STATUS: FAIL")
        print("\n".join(f"- {item}" for item in sorted(set(errors))))
        raise SystemExit(1)
    print(f"STATUS: PASS ({len(pages)} generated pages checked)")


if __name__ == "__main__":
    main()
