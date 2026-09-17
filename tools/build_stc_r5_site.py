"""Canonical Flowmatic website build entry point for STC-lite R5.

The legacy ``build_site.py`` still owns all product/detail pages and protected
motion/media composition. The R5 homepage is a deliberately newer product
narrative. This wrapper runs the legacy generator and then restores the tracked
R5 home surfaces so a normal site rebuild cannot silently downgrade the public
homepage to the R4 narrative.

The checked-in R5 home files are therefore canonical until the STC renderer is
migrated into the legacy generator itself.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "2026.09.17-r5-stc"
CANONICAL = (
    Path("index.html"),
    Path("ko/index.html"),
    Path("en/index.html"),
    Path("ar/index.html"),
    Path("release.json"),
)


def _capture() -> dict[Path, bytes]:
    snapshot: dict[Path, bytes] = {}
    for relative in CANONICAL:
        path = ROOT / relative
        if not path.exists():
            raise SystemExit(f"Missing canonical STC-lite R5 file: {relative}")
        snapshot[relative] = path.read_bytes()

    for relative in CANONICAL[:-1]:
        text = snapshot[relative].decode("utf-8")
        if f'content="{RELEASE}"' not in text:
            raise SystemExit(
                f"Refusing to preserve non-R5 homepage {relative}; expected {RELEASE}."
            )
        if "stc-lite-home-v1.css" not in text or "id=\"stack\"" not in text:
            raise SystemExit(f"Canonical STC-lite structure missing from {relative}.")

    release = json.loads(snapshot[Path("release.json")].decode("utf-8"))
    if release.get("release") != RELEASE:
        raise SystemExit(
            f"release.json is not the STC-lite R5 release: {release.get('release')!r}"
        )
    return snapshot


def _restore(snapshot: dict[Path, bytes]) -> None:
    for relative, payload in snapshot.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def main() -> int:
    snapshot = _capture()
    subprocess.run([sys.executable, str(ROOT / "build_site.py")], cwd=ROOT, check=True)
    _restore(snapshot)
    print(
        "PASS: legacy detail pages rebuilt; STC-lite R5 canonical home and release restored."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
