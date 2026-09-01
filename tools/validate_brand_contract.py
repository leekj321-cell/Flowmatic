from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "brand-policy.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []

    if not POLICY_PATH.is_file():
        print("FAIL: brand-policy.json is missing")
        return 1

    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    if policy.get("status") != "APPROVED_LOCKED":
        failures.append("policy status must be APPROVED_LOCKED")
    if policy.get("enforcement") != "FAIL_CLOSED":
        failures.append("policy enforcement must be FAIL_CLOSED")

    for asset_id, asset in policy.get("assets", {}).items():
        relative = Path(asset["path"])
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"{asset_id}: missing {relative.as_posix()}")
            continue
        actual = sha256(path)
        expected = asset["sha256"].lower()
        if actual != expected:
            failures.append(
                f"{asset_id}: checksum mismatch for {relative.as_posix()} "
                f"(expected {expected}, got {actual})"
            )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"PASS: {len(policy['assets'])} canonical Flowmatic CI assets verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())

