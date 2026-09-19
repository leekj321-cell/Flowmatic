"""Canonical Flowmatic website build entry point for the investor-first Factory OS homepage.

The legacy ``build_site.py`` still owns product/detail pages and protected
motion/media composition. This wrapper rebuilds those detail pages and then
restores the tracked public Factory OS home surfaces so a normal rebuild cannot
silently downgrade the current homepage narrative.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "2026.09.19-r6-investor"
ROOT_REDIRECT = Path("index.html")
LOCALE_HOMES = (Path("ko/index.html"), Path("en/index.html"), Path("ar/index.html"))
CANONICAL = (ROOT_REDIRECT, *LOCALE_HOMES, Path("release.json"))


def _capture() -> dict[Path, bytes]:
    snapshot: dict[Path, bytes] = {}
    for relative in CANONICAL:
        path = ROOT / relative
        if not path.exists():
            raise SystemExit(f"Missing canonical Factory OS file: {relative}")
        snapshot[relative] = path.read_bytes()

    root_text = snapshot[ROOT_REDIRECT].decode("utf-8")
    if "/ko/" not in root_text or "Flowmatic Factory OS" not in root_text:
        raise SystemExit("Root index is not the canonical Flowmatic Factory OS locale redirect.")

    for relative in LOCALE_HOMES:
        text = snapshot[relative].decode("utf-8")
        if f'content="{RELEASE}"' not in text:
            raise SystemExit(f"Refusing to preserve non-current homepage {relative}; expected {RELEASE}.")
        if "stc-lite-home-v1.css" not in text or "id=\"stack\"" not in text or "Flowmatic Factory OS" not in text:
            raise SystemExit(f"Canonical Factory OS structure missing from {relative}.")

    release = json.loads(snapshot[Path("release.json")].decode("utf-8"))
    if release.get("release") != RELEASE:
        raise SystemExit(f"release.json is not the current homepage release: {release!r}")
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
    print("PASS: legacy detail pages rebuilt; Factory OS public home surfaces restored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
