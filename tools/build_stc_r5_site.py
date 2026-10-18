"""Canonical build: preserve the detail generator, then generate the approved homes."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]

def main():
    notes = (ROOT / "IMPLEMENTATION_NOTES.md").read_bytes()
    subprocess.run([sys.executable, str(ROOT / "build_site.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "tools/build_investor_home.py")], cwd=ROOT, check=True)
    (ROOT / "IMPLEMENTATION_NOTES.md").write_bytes(notes)
    print("PASS: detail routes rebuilt and current KO/EN/AR homepages generated.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
