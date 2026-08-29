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
assert config["empty_endpoint_policy"] == "INTAKE_ONLY_NO_BUILD_CLAIM"
assert isinstance(config["compiler_endpoint"], str)
assert config["intake_endpoint"].startswith("https://")

modules = catalog["modules"]
assert modules
for problem in catalog["problems"]:
    assert problem["id"] and problem["label"]
    assert problem["modules"]
    for module_id in problem["modules"]:
        assert module_id in modules, (problem["id"], module_id)
for module_id, spec in modules.items():
    assert spec["name"]
    assert spec["capabilities"], module_id
    for capability_id in spec["capabilities"]:
        assert re.fullmatch(r"[a-z0-9_.-]+@\d+", capability_id), capability_id

objective_rules = catalog.get("objective_rules") or []
assert objective_rules
for rule in objective_rules:
    assert rule["id"] and rule["terms"] and rule["modules"]
    for module_id in rule["modules"]:
        assert module_id in modules, (rule["id"], module_id)

# Regression: the user's observed sentence must add CT/Trend and Revision modules.
text = "G코드의 생성과 수정, 사이클타임 예측 및 G코드의 최신 리비전 관리".lower()
matched_modules: set[str] = set()
for rule in objective_rules:
    if any(term.lower() in text for term in rule["terms"]):
        matched_modules.update(rule["modules"])
assert "flowmatic.generator.modular" in matched_modules
assert "flowmatic.data_management.modular" in matched_modules
assert "scada.line_monitor@1" in matched_modules
assert "scada.trend_history@1" in matched_modules

gap_rules = catalog.get("gap_rules") or []
assert gap_rules
matched_gaps = [
    rule for rule in gap_rules
    if any(term.lower() in text for term in rule["terms"])
]
assert any(rule["missing_capability"] == "cycle.forecast@1" for rule in matched_gaps)
for rule in gap_rules:
    assert re.fullmatch(r"[a-z0-9_.-]+@\d+", rule["missing_capability"]), rule

# Public browser code must never contain a real API/token secret.
for forbidden in ("OPENAI_API_KEY=", "GITHUB_DISPATCH_TOKEN=", "ghp_", "github_pat_", "sk-proj-", "sk-"):
    assert forbidden not in html
    assert forbidden not in json.dumps(config)

# Browser/server contract and traceable receipt semantics.
for required_text in (
    "function inferObjective(purpose)",
    "catalog.objective_rules",
    "catalog.gap_rules",
    "cycle.forecast@1",
    "client_request_id:result.clientRequestId",
    "requested_capabilities:allRequestedCapabilities(result)",
    "Request ID",
    "INTAKE TRANSPORT ACCEPTED",
    "SERVER COMPILER ACCEPTED",
    "Demo EXE가 생성된 상태는 아닙니다",
    "fetch('./config.json'",
    "await sendGateway(lastResult);queued=true",
    "await sendIntake(intakePayload(lastResult,'[Flowmatic] Engine Gap Review'))",
    "Canonical Engine Pool에는 자동 반영",
):
    assert required_text in html, required_text

# Missing capabilities must be forwarded to the server, not silently dropped.
assert "...(result.gaps||[]).map(g=>g.missing_capability)" in html

# Intake success is not confused with inbox delivery or Demo completion.
assert "Form intake가 요청을 수락했습니다" in html
assert "메일함 전달은 아직 확인되지 않았습니다" in html

# Engine Gap uses both channels when Gateway is configured; missing Gateway
# degrades only to intake transport without any build-complete claim.
assert "if(config?.compiler_endpoint){" in html
assert "if(queued&&emailed)" in html
assert "if(emailed)" in html

print("SOLUTION_COMPILER_WEB_GATE=PASS")
print(f"PROBLEMS={len(catalog['problems'])}")
print(f"MODULES={len(modules)}")
print(f"OBJECTIVE_RULES={len(objective_rules)}")
print(f"GAP_RULES={len(gap_rules)}")
print("REGRESSION_CYCLE_FORECAST=ENGINE_GAP_WITH_CT_TREND_CONTEXT")
print("RECEIPT_MODE=TRACEABLE_CLIENT_ID_FAIL_CLOSED")
