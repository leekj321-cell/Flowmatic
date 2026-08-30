from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
html = (ROOT / "index.html").read_text(encoding="utf-8")

assert catalog["schema_version"] == 1
assert int(catalog["demo_days"]) == 30
assert config["schema_version"] == 1
assert config["compiler_authority"] == "server"
assert isinstance(config["compiler_endpoint"], str)
assert config["compiler_endpoint"].startswith("https://")
assert config["intake_endpoint"].startswith("https://")

modules = catalog["modules"]
assert modules
for problem in catalog["problems"]:
    assert problem["id"] and problem["label"] and problem["modules"]
    for module_id in problem["modules"]:
        assert module_id in modules
for module_id, spec in modules.items():
    assert spec["name"] and spec["capabilities"]
    for capability_id in spec["capabilities"]:
        assert re.fullmatch(r"[a-z0-9_.-]+@\d+", capability_id)

assert catalog.get("objective_rules")
assert catalog.get("gap_rules")

# V0.4 UX contract: only one free-text intent field remains.
assert 'id="customProblem"' not in html
assert 'id="intent"' in html
assert '목적 / 완료 조건 / 추가 요구사항' in html
assert 'function inferIntent(intent)' in html
assert 'function extractUnclassified(intent)' in html
assert "free_text_problem:unclassifiedText(result)" in html
assert "objective:result.intent" in html
assert "requirement.unclassified@1" in html
assert 'PARTIAL MATCH / GAP REVIEW' in html
assert 'SERVER COMPILER ACCEPTED' in html
assert 'Flowmatic Solution Compiler / V0.4' in html

# Existing cycle forecast behavior is still fail-closed.
text = "G코드의 생성과 수정, 사이클타임 예측 및 G코드의 최신 리비전 관리".lower()
matched_modules = set()
for rule in catalog["objective_rules"]:
    if any(term.lower() in text for term in rule["terms"]):
        matched_modules.update(rule["modules"])
assert "flowmatic.generator.modular" in matched_modules
assert "flowmatic.data_management.modular" in matched_modules
assert "scada.line_monitor@1" in matched_modules
assert "scada.trend_history@1" in matched_modules
assert any(
    rule["missing_capability"] == "cycle.forecast@1"
    and any(term.lower() in text for term in rule["terms"])
    for rule in catalog["gap_rules"]
)

for forbidden in ("OPENAI_API_KEY=", "GITHUB_DISPATCH_TOKEN=", "ghp_", "github_pat_", "sk-proj-", "sk-"):
    assert forbidden not in html
    assert forbidden not in json.dumps(config)

print("SOLUTION_COMPILER_WEB_GATE=PASS")
print("UX=SINGLE_INTENT_FIELD")
print("UNCLASSIFIED=FAIL_CLOSED_CANDIDATE_REVIEW")
print(f"PROBLEMS={len(catalog['problems'])}")
print(f"MODULES={len(modules)}")
