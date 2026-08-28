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

# Public browser code must never contain a real API/token secret.
for forbidden in ("OPENAI_API_KEY=", "GITHUB_DISPATCH_TOKEN=", "ghp_", "github_pat_", "sk-proj-", "sk-"):
    assert forbidden not in html
    assert forbidden not in json.dumps(config)

# The browser sends the server gateway's canonical intake shape.
for required_text in (
    "selected_problem_keys:result.selected",
    "free_text_problem:result.custom||''",
    "objective:result.purpose",
    "requested_capabilities:result.caps",
    "fetch('./config.json'",
    "Demo가 생성된 상태는 아닙니다",
    "await sendGateway(lastResult);queued=true",
    "await sendIntake(intakePayload(lastResult,'[Flowmatic] Engine Gap Review'))",
    "Canonical Engine Pool에는 자동 반영되지 않습니다",
):
    assert required_text in html, required_text

# Engine Gap uses both channels when Gateway is configured, while a missing
# Gateway can still degrade to inbound email without any Demo claim.
assert "if(config?.compiler_endpoint){" in html
assert "if(queued&&emailed)" in html
assert "if(emailed)" in html
assert "Gateway가 아직 비활성 또는 일시 실패" in html

print("SOLUTION_COMPILER_WEB_GATE=PASS")
print(f"PROBLEMS={len(catalog['problems'])}")
print(f"MODULES={len(modules)}")
print("GAP_ROUTE=CANDIDATE_QUEUE_PLUS_EMAIL_WHEN_GATEWAY_READY")
