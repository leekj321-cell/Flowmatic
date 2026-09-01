"""Static regression checks for the generated Flowmatic V.Next site."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
LANGS = {"ko": "ltr", "en": "ltr", "ar": "rtl"}
PAGES = (
    "",
    "quality",
    "machining-intelligence",
    "operations-intelligence",
    "logistics-intelligence",
    "platform",
    "nc",
    "ct",
    "work-standard",
    "tms",
    "amr",
)
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
    "05 · CURRENT STAGE",
    "FUNCTIONAL PROTOTYPES",
    "KICXUP CHALLENGE",
    "SEALINK PoC",
)
DECISION_COPY_FORBIDDEN = (
    "그림만 바꾼",
    "This is not just a new diagram",
    "ليست مجرد رسمة جديدة",
    "아래 3개 가로 레이어",
    "These three horizontal layers",
    "هذه الطبقات الأفقية الثلاث",
    "각 Module은 어떤 Engine을 쓰는지",
    "Each module shows the engines it uses",
    "كل وحدة توضح المحركات التي تستخدمها",
    "V156 HEADLESS PASS",
    "EXISTING / INTEGRATION",
    "COMPOSITION TARGET",
    "153 / 153 PASS",
    "legacy-free",
    "Windows GUI/OpenGL",
)
GLOBAL_DIRECT_TERMS = ("투자", "투자자", "투자 결정", "investment", "investor", "استثمار", "مستثمر")
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

HOME_CONTEXTS = {
    "context-machine": "Machine",
    "context-product": "Product",
    "context-process": "Process",
    "context-tool": "Tool",
    "context-feature": "Feature",
    "context-quality": "Quality",
    "context-measurement": "Measurement",
    "context-material": "Material",
    "context-worker": "Worker",
    "context-time": "Time",
}
HOME_ENGINES = {
    "engine-nc-semantic": "NC Semantic",
    "engine-geometry": "Geometry",
    "engine-machine-state": "Machine State",
    "engine-quality-analysis": "Quality Analysis",
    "engine-measurement": "Measurement",
    "engine-tool-life": "Tool Life",
    "engine-revision": "Revision",
    "engine-reference-data": "Reference Data",
    "engine-vision-ct": "Vision / CT",
    "engine-workflow": "Workflow",
    "engine-cost-resource": "Cost / Resource",
    "engine-material-flow": "Material Flow",
}
HOME_MODULES = {
    "viewer": ("Viewer", {"nc-semantic", "geometry", "revision"}, {"machining"}),
    "generator": ("Generator", {"nc-semantic", "geometry", "revision"}, {"machining"}),
    "workstandard": ("Work Standard", {"geometry", "workflow", "reference-data"}, {"machining"}),
    "measurement": (
        "Measurement / Compensation",
        {"measurement", "geometry", "quality-analysis"},
        {"machining", "quality"},
    ),
    "tms": ("TMS", {"tool-life", "nc-semantic", "revision"}, {"machining", "operations"}),
    "pm": ("Preventive Maintenance", {"machine-state", "measurement", "tool-life"}, {"operations"}),
    "qualitywork": ("Quality Worklist", {"quality-analysis", "cost-resource", "workflow"}, {"quality"}),
    "machinemonitor": ("Machine Monitor", {"machine-state", "vision-ct", "workflow"}, {"operations"}),
    "rootcause": (
        "Root Cause",
        {"quality-analysis", "machine-state", "tool-life", "revision"},
        {"quality", "operations"},
    ),
    "dispatch": ("Material Dispatch", {"material-flow", "workflow", "machine-state"}, {"logistics"}),
    "data": (
        "Data Management",
        {"revision", "reference-data", "workflow"},
        {"machining", "quality", "operations", "logistics"},
    ),
    "tower": (
        "Control Tower",
        {"machine-state", "quality-analysis", "cost-resource", "workflow"},
        {"quality", "operations", "logistics"},
    ),
}
HOME_AXES = {
    "machining": "Machining Intelligence",
    "quality": "Quality Intelligence",
    "operations": "Operations Intelligence",
    "logistics": "Logistics Intelligence",
}
HOME_MOTION_STATES = {"field", "context-engine", "modules", "intelligence"}
VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Scan(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.lang = ""
        self.direction = ""
        self.title = False
        self.description = False
        self.module_cards = 0
        self.source_nodes: list[tuple[str, str]] = []
        self.solution_nodes: list[str] = []
        self.statuses: Counter[str] = Counter()
        self.hero_titles: list[list[str]] = []
        self.composition_roots: list[dict[str, str]] = []
        self.composition_stages: list[dict[str, str]] = []
        self.composition_tokens: list[dict[str, object]] = []
        self.composition_modules: list[dict[str, object]] = []
        self.composition_axes: list[dict[str, object]] = []
        self.composition_edge_layers: list[dict[str, str]] = []
        self.composition_paths: list[dict[str, str]] = []
        self._hero_title_depth = 0
        self._hero_title_parts: list[str] | None = None
        self._captures: list[dict[str, object]] = []

    def _finish_capture(self, capture: dict[str, object]) -> None:
        record = {
            "attrs": capture["attrs"],
            "text": " ".join(" ".join(capture["text"]).split()),
        }
        capture_types = capture["types"]
        if "token" in capture_types:
            self.composition_tokens.append(record)
        if "module" in capture_types:
            self.composition_modules.append(record)
        if "axis" in capture_types:
            self.composition_axes.append(record)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag not in VOID_ELEMENTS:
            for capture in self._captures:
                capture["depth"] += 1
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
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if "data-composition-motion" in values:
            self.composition_roots.append({key: value or "" for key, value in values.items()})
        if "data-composition-stage" in values:
            self.composition_stages.append({key: value or "" for key, value in values.items()})
        if values.get("data-edge-layer"):
            self.composition_edge_layers.append({key: value or "" for key, value in values.items()})
        if tag == "path" and (values.get("data-from") or values.get("data-to")):
            self.composition_paths.append({key: value or "" for key, value in values.items()})
        if "module-card" in classes:
            self.module_cards += 1
            status = values.get("data-status")
            if status:
                self.statuses[status] += 1
        if "source-node" in classes:
            self.source_nodes.append((values.get("data-source") or "", values.get("data-solutions") or ""))
        if "solution-card" in classes:
            self.solution_nodes.append(values.get("data-solution") or "")
        capture_types = set()
        if values.get("data-token-kind"):
            capture_types.add("token")
        if values.get("data-module-id") or values.get("data-source"):
            capture_types.add("module")
        if "data-motion-axis" in values and values.get("data-axis"):
            capture_types.add("axis")
        elif values.get("data-axis-id") or ("solution-card" in classes and values.get("data-solution")):
            capture_types.add("axis")
        if capture_types:
            self._captures.append({
                "attrs": {key: value or "" for key, value in values.items()},
                "depth": 1,
                "text": [],
                "types": capture_types,
            })
        for key in ("href", "src", "srcset"):
            value = values.get(key)
            if value:
                self.links.append((key, value.split()[0]))

    def handle_endtag(self, tag: str) -> None:
        if tag not in VOID_ELEMENTS:
            completed = []
            for capture in self._captures:
                capture["depth"] -= 1
                if capture["depth"] == 0:
                    completed.append(capture)
            for capture in completed:
                self._captures.remove(capture)
                self._finish_capture(capture)
        if not self._hero_title_depth:
            return
        self._hero_title_depth -= 1
        if self._hero_title_depth == 0 and self._hero_title_parts is not None:
            self.hero_titles.append(self._hero_title_parts)
            self._hero_title_parts = None

    def handle_data(self, data: str) -> None:
        for capture in self._captures:
            capture["text"].append(data)
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
        *(ROOT / lang / "platform" / "index.html" for lang in LANGS),
    ]


def local_target(value: str, current_page: Path) -> tuple[Path | None, str]:
    if value.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None, ""
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None, ""
    path = parsed.path
    if not path:
        return current_page, parsed.fragment
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target /= "index.html"
    return target, parsed.fragment


def has_fragment(target: Path, fragment: str) -> bool:
    if not fragment:
        return True
    if not target.exists():
        return False
    text = target.read_text(encoding="utf-8", errors="ignore")
    return f'id="{fragment}"' in text


def captured_attrs(record: dict[str, object]) -> dict[str, str]:
    return record["attrs"]  # type: ignore[return-value]


def captured_label(record: dict[str, object]) -> str:
    attrs = captured_attrs(record)
    return attrs.get("data-label") or str(record["text"])


def attribute_values(html: str, attribute: str) -> list[str]:
    return re.findall(rf'\b{re.escape(attribute)}=["\']([^"\']*)["\']', html)


def css_at_rule_blocks(stylesheet: str, at_rule_pattern: str) -> list[str]:
    """Return balanced @media blocks whose prelude matches a regular expression."""
    blocks = []
    for match in re.finditer(at_rule_pattern, stylesheet, flags=re.IGNORECASE):
        opening = stylesheet.find("{", match.end())
        if opening < 0:
            continue
        depth = 0
        for index in range(opening, len(stylesheet)):
            character = stylesheet[index]
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    blocks.append(stylesheet[opening + 1:index])
                    break
    return blocks


def javascript_function(script: str, name: str) -> str:
    match = re.search(rf"function\s+{re.escape(name)}\s*\([^)]*\)\s*\{{", script)
    if not match:
        return ""
    opening = script.find("{", match.start())
    depth = 0
    quote = ""
    escaped = False
    for index in range(opening, len(script)):
        character = script[index]
        if quote:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = ""
            continue
        if character in ("'", '"', "`"):
            quote = character
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return script[match.start():index + 1]
    return ""


def check_home_composition(label: str, home: str, errors: list[str]) -> Scan:
    scan = Scan()
    scan.feed(home)

    required = (
        'data-composition-journey',
        'data-composition-motion',
        'data-composition-stage',
        'id="architecture"',
        'id="modules"',
        'id="solutions"',
        'id="current-stage"',
        "PUBLIC DEMOS",
    )
    for marker in required:
        if marker not in home:
            errors.append(f"home motion content missing ({label}): {marker}")

    forbidden = ('class="transformation"', 'id="before-after"', 'id="approach"', 'data-field-story', "KICXUP CHALLENGE")
    for marker in forbidden:
        if marker in home:
            errors.append(f"obsolete home content present ({label}): {marker}")

    if len(scan.composition_roots) != 1:
        errors.append(f"home motion root count ({label}): expected 1, got {len(scan.composition_roots)}")
    elif scan.composition_roots[0].get("data-composition-state") != "field":
        errors.append(f"home initial motion state invalid ({label}): expected field")
    stage_states = [item.get("data-composition-stage", "") for item in scan.composition_stages]
    if len(stage_states) != 4 or set(stage_states) != HOME_MOTION_STATES:
        errors.append(f"home motion stages mismatch ({label}): expected {sorted(HOME_MOTION_STATES)}, got {stage_states}")
    if Counter(item.get("aria-current", "") for item in scan.composition_stages)["step"] != 1:
        errors.append(f"home active motion step count ({label}): expected 1")
    if home.count("data-motion-pause") != 1 or 'aria-pressed="false"' not in home:
        errors.append(f"home motion pause control contract missing ({label})")
    if home.count("data-motion-fallback") != 1:
        errors.append(f"home motion fallback root count ({label}): expected 1")
    if home.count("composition-motion__fallback-step") != 4:
        errors.append(f"home motion fallback step count ({label}): expected 4")

    target_contracts = (
        ("data-motion-align-target", set(HOME_CONTEXTS) | set(HOME_ENGINES)),
        ("data-motion-assembly-target", set(HOME_MODULES)),
        ("data-motion-axis-target", set(HOME_MODULES)),
        ("data-motion-axis-card-target", set(HOME_AXES)),
    )
    for attribute, expected in target_contracts:
        actual = attribute_values(home, attribute)
        if len(actual) != len(expected) or set(actual) != expected:
            errors.append(
                f"home motion target contract ({label}): {attribute} expected {sorted(expected)}, got {actual}"
            )

    by_kind: dict[str, list[dict[str, object]]] = {"context": [], "engine": [], "module": []}
    for record in scan.composition_tokens:
        kind = captured_attrs(record).get("data-token-kind", "")
        if kind in by_kind:
            by_kind[kind].append(record)
        else:
            errors.append(f"home token kind invalid ({label}): {kind or '<missing>'}")

    for kind, expected in (("context", HOME_CONTEXTS), ("engine", HOME_ENGINES)):
        records = by_kind[kind]
        actual: dict[str, str] = {}
        for record in records:
            attrs = captured_attrs(record)
            token_id = attrs.get("data-token-id", "")
            if token_id in actual:
                errors.append(f"home {kind} token ID duplicated ({label}): {token_id or '<missing>'}")
            actual[token_id] = captured_label(record)
        if actual != expected:
            errors.append(f"home {kind} tokens mismatch ({label}): expected {expected}, got {actual}")

    module_records = scan.composition_modules
    module_dom: dict[str, dict[str, object]] = {}
    for record in module_records:
        attrs = captured_attrs(record)
        module_id = attrs.get("data-module-id") or attrs.get("data-source") or ""
        source_id = attrs.get("data-source")
        if source_id and attrs.get("data-module-id") and source_id != attrs["data-module-id"]:
            errors.append(f"home module/source identity mismatch ({label}): {attrs['data-module-id']} != {source_id}")
        if module_id in module_dom:
            errors.append(f"home module rendered more than once ({label}): {module_id or '<missing>'}")
        module_dom[module_id] = record
    if len(module_records) != 12 or set(module_dom) != set(HOME_MODULES):
        errors.append(
            f"home canonical module DOM mismatch ({label}): expected 12 {sorted(HOME_MODULES)}, "
            f"got {len(module_records)} {sorted(module_dom)}"
        )
    if by_kind["module"]:
        errors.append(f"home module duplicated as generic tokens ({label}): expected canonical data-motion-module nodes only")

    engine_edges: set[tuple[str, str]] = set()
    axis_edges: set[tuple[str, str]] = set()
    for module_id, (expected_label, expected_engines, expected_axes) in HOME_MODULES.items():
        record = module_dom.get(module_id)
        if not record:
            continue
        attrs = captured_attrs(record)
        if captured_label(record) != expected_label:
            errors.append(
                f"home module label mismatch ({label}): {module_id} expected {expected_label!r}, "
                f"got {captured_label(record)!r}"
            )
        engines = set(attrs.get("data-engines", "").split())
        axes = set(attrs.get("data-solutions", "").split())
        if engines != expected_engines:
            errors.append(f"home module engine mapping mismatch ({label}): {module_id} -> {sorted(engines)}")
        if axes != expected_axes:
            errors.append(f"home module axis mapping mismatch ({label}): {module_id} -> {sorted(axes)}")
        if attrs.get("data-contexts") != "shared":
            errors.append(f"home module shared context missing ({label}): {module_id}")
        engine_edges.update((engine_id, module_id) for engine_id in engines)
        axis_edges.update((module_id, axis_id) for axis_id in axes)

    if len(engine_edges) != 38:
        errors.append(f"home engine-to-module mapping count ({label}): expected 38, got {len(engine_edges)}")
    if len(axis_edges) != 20:
        errors.append(f"home module-to-axis mapping count ({label}): expected 20, got {len(axis_edges)}")
    axis_inbound = Counter(axis_id for _, axis_id in axis_edges)
    expected_inbound = Counter({"machining": 6, "quality": 5, "operations": 6, "logistics": 3})
    if axis_inbound != expected_inbound:
        errors.append(f"home axis inbound mapping mismatch ({label}): {dict(axis_inbound)}")

    axes: dict[str, str] = {}
    for record in scan.composition_axes:
        attrs = captured_attrs(record)
        axis_id = attrs.get("data-axis") or attrs.get("data-axis-id") or attrs.get("data-solution") or ""
        if axis_id in axes:
            errors.append(f"home axis rendered more than once ({label}): {axis_id or '<missing>'}")
        axes[axis_id] = captured_label(record)
    if set(axes) != set(HOME_AXES):
        errors.append(f"home axes mismatch ({label}): expected {sorted(HOME_AXES)}, got {sorted(axes)}")
    else:
        for axis_id, expected_label in HOME_AXES.items():
            if axes[axis_id].count(expected_label) != 1:
                errors.append(f"home axis label mismatch ({label}): {axis_id} -> {axes[axis_id]!r}")

    edge_layers = Counter(layer.get("data-edge-layer", "") for layer in scan.composition_edge_layers)
    for layer in ("engine-module", "module-axis"):
        if edge_layers[layer] != 1:
            errors.append(f"home SVG edge layer count ({label}): {layer} expected 1, got {edge_layers[layer]}")

    static_paths = [
        item for item in scan.composition_paths
        if item.get("data-edge-layer") in {"engine-module", "module-axis"}
    ]
    if static_paths:
        path_keys = {
            (item.get("data-edge-layer", ""), item.get("data-from", ""), item.get("data-to", ""))
            for item in static_paths
        }
        if len(path_keys) != len(static_paths):
            errors.append(f"home static SVG paths duplicated ({label})")

    for state in HOME_MOTION_STATES:
        if home.count(f'data-composition-stage="{state}"') != 1:
            errors.append(f"home motion stage missing or duplicated ({label}): {state}")
    return scan


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
        duplicate_ids = [item for item, count in Counter(scan.ids).items() if count > 1]
        if duplicate_ids:
            errors.append(f"duplicate IDs: {page.relative_to(ROOT)} -> {', '.join(sorted(duplicate_ids))}")
        for phrase in GLOBAL_DIRECT_TERMS:
            if phrase.lower() in text.lower():
                errors.append(f"direct decision-language term: {page.relative_to(ROOT)} -> {phrase}")
        for phrase in DECISION_COPY_FORBIDDEN:
            if phrase.lower() in text.lower():
                errors.append(f"decision copy contains prohibited wording: {page.relative_to(ROOT)} -> {phrase}")
        for _, value in scan.links:
            target, fragment = local_target(value, page)
            if target is not None and not target.exists():
                errors.append(f"broken asset/link: {page.relative_to(ROOT)} -> {value}")
            elif target is not None and fragment and not has_fragment(target, fragment):
                errors.append(f"broken fragment: {page.relative_to(ROOT)} -> {value}")

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
        home_scan = check_home_composition(lang, home, errors)
        if home_scan.hero_titles != [list(BRAND_HERO_LINES)]:
            errors.append(f"fixed brand slogan mismatch ({lang}): {home_scan.hero_titles}")

        operations = (ROOT / lang / "operations-intelligence" / "index.html").read_text(encoding="utf-8")
        if operations.count("data-field-story") != 1:
            errors.append(f"Operations story count ({lang}): expected 1")
        for stage in ("read", "event", "action", "confirm"):
            if operations.count(f'data-story-stage="{stage}"') != 1:
                errors.append(f"Operations story stage ({lang}): {stage}")
        machining = (ROOT / lang / "machining-intelligence" / "index.html").read_text(encoding="utf-8")
        for phrase in ("Manufacturing Recipe", "INFERRED", "USER CONFIRMED", "Managed Metadata Comment Block", "Conflict review", "fail-closed"):
            if phrase not in machining:
                errors.append(f"machining content missing ({lang}): {phrase}")

    root_home = (ROOT / "index.html").read_text(encoding="utf-8")
    root_scan = check_home_composition("index.html", root_home, errors)
    if root_scan.hero_titles != [list(BRAND_HERO_LINES)]:
        errors.append(f"fixed brand slogan mismatch (index.html): {root_scan.hero_titles}")

    ko_home = (ROOT / "ko" / "index.html").read_text(encoding="utf-8")
    for phrase in ("Machining · Recipe", "Machining · Safety Contract", "Machining · V.Next scope", "deterministic source test", "prototype integration"):
        if phrase in ko_home:
            errors.append(f"Korean evidence contains internal memo wording: {phrase}")

    script = (ROOT / "script.js").read_text(encoding="utf-8")
    stylesheet = (ROOT / "style-v5.20.css").read_text(encoding="utf-8")
    qr_signature = (ROOT / "assets" / "branding" / "flowmatic-qr-contact-signature.svg").read_text(
        encoding="utf-8"
    )
    if 'href="/assets/branding/canonical/' in qr_signature:
        errors.append("QR signature must not depend on an external nested CI asset")
    for marker in (
        'id="qr-ci-amber"',
        'id="qr-ci-blue"',
        'id="qr-ci-red"',
        'aria-label="Flowmatic global wordmark"',
        "MANUFACTURING INTELLIGENCE OS",
    ):
        if marker not in qr_signature:
            errors.append(f"QR signature embedded global CI missing: {marker}")
    home_paths = ("index.html", *(f"{lang}/index.html" for lang in LANGS))
    for home_path in home_paths:
        home = (ROOT / home_path).read_text(encoding="utf-8")
        if "flowmatic-qr-contact-signature.svg?v=20260902.2" not in home:
            errors.append(f"QR signature cache version missing ({home_path})")
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

    motion_function = javascript_function(script, "initHomeCompositionMotion")
    if not motion_function:
        errors.append("home composition motion initializer missing: initHomeCompositionMotion")
    else:
        motion_js_markers = (
            "[data-composition-motion]",
            "[data-motion-token]",
            "[data-motion-module]",
            "[data-motion-axis]",
            "[data-edge-layer",
            "createElementNS",
            "requestAnimationFrame",
            "ResizeObserver",
            "prefersReducedMotion",
            "dataset.engines",
            "dataset.solutions",
            "dataset.motionAlignTarget",
            "dataset.motionAssemblyTarget",
            "dataset.motionAxisTarget",
            "dataset.motionAxisCardTarget",
            "dataset.composeEdgeCount",
            "dataset.axisEdgeCount",
            "axisEntryPoints.get(edge.to)",
            "measuredHeight > 1 ? measuredHeight",
            "data-edge-index",
            "[data-motion-pause]",
        )
        for marker in motion_js_markers:
            if marker not in motion_function:
                errors.append(f"home composition motion JS contract missing: {marker}")
        for state in HOME_MOTION_STATES:
            if state not in motion_function:
                errors.append(f"home composition motion JS state missing: {state}")
        path_contracts = {
            "data-from": r"['\"]data-from['\"]",
            "data-to": r"['\"]data-to['\"]",
            "path d": r"setAttribute\(\s*['\"]d['\"]",
        }
        for label, pattern in path_contracts.items():
            if not re.search(pattern, motion_function):
                errors.append(f"home composition generated path contract missing: {label}")
        if not re.search(r"innerWidth\s*<=\s*900", motion_function):
            errors.append("home composition JavaScript compact motion breakpoint missing: 900px")
        for marker in ("Math.cos(angle)", "Math.sin(angle)", "placeRing(contextTokens", "placeRing(engineTokens"):
            if marker not in motion_function:
                errors.append(f"home composition mobile radial layout missing: {marker}")
    if script.count("initHomeCompositionMotion();") != 1:
        errors.append("home composition motion initializer call count: expected 1")

    motion_css_selectors = (
        r"\[data-composition-motion\][^{}]*\.composition-motion__canvas[^{}]*\{",
        r"\[data-composition-motion\][^{}]*\[data-motion-token\][^{}]*\{",
        r"\[data-composition-motion\][^{}]*\[data-motion-module\][^{}]*\{",
        r"\[data-composition-motion\][^{}]*\[data-motion-axis\][^{}]*\{",
        r"\[data-composition-motion\][^{}]*\.composition-motion__links[^{}]*path[^{}]*\{",
        r"\[data-composition-motion\][^{}]*\[data-motion-pause\][^{}]*\{",
    )
    for pattern in motion_css_selectors:
        if not re.search(pattern, stylesheet):
            errors.append(f"home composition HTML/CSS selector contract missing: {pattern}")
    for state in HOME_MOTION_STATES:
        state_selector = rf'\[data-composition-motion\]\[data-composition-state=["\']{re.escape(state)}["\']\]'
        if not re.search(state_selector, stylesheet):
            errors.append(f"home composition CSS state missing: {state}")
    if (
        not re.search(r"@keyframes\s+composition(?:-motion|-token)-drift", stylesheet)
        or not re.search(r"width\s*:\s*max-content", stylesheet)
    ):
        errors.append("home composition word-sized floating token CSS missing")

    mobile_motion_blocks = css_at_rule_blocks(
        stylesheet,
        r"@media[^{}]*max-width\s*:\s*900px[^{}]*prefers-reduced-motion\s*:\s*no-preference[^{}]*",
    )
    mobile_motion = any(
        "[data-composition-motion]" in block
        and ".composition-motion__canvas" in block
        and "position: sticky" in block
        and "min-height: 380svh" in block
        and re.search(r"\.composition-motion__canvas\s*\{[^{}]*display\s*:\s*block", block)
        and re.search(r"\.composition-motion__links\s*\{[^{}]*display\s*:\s*block", block)
        for block in mobile_motion_blocks
    )
    if not mobile_motion:
        errors.append("home composition mobile scroll-motion CSS missing")

    reduced_blocks = css_at_rule_blocks(
        stylesheet,
        r"@media[^{}]*prefers-reduced-motion\s*:\s*reduce[^{}]*",
    )
    reduced_fallback = any(
        "[data-composition-motion]" in block
        and "[data-motion-fallback]" in block
        and "position: static" in block
        and re.search(r"display\s*:\s*(?:grid|block|flex)", block)
        for block in reduced_blocks
    )
    if not reduced_fallback:
        errors.append("home composition prefers-reduced-motion fallback CSS missing")
    elif any(re.search(r"\.composition-motion__canvas\s*\{[^{}]*display\s*:\s*grid", block) for block in reduced_blocks):
        errors.append("home composition reduced-motion fallback duplicates the live motion canvas")

    if errors:
        print("STATUS: FAIL")
        print("\n".join(f"- {item}" for item in sorted(set(errors))))
        raise SystemExit(1)
    print(f"STATUS: PASS ({len(pages)} generated pages checked)")


if __name__ == "__main__":
    main()
