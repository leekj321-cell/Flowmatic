"""Keep the public NC example distinct from shop programs and private reviews."""
from pathlib import Path
import hashlib
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = 'demo-data/flowmatic-nc-sample.nc'
SAMPLE_SHA256 = '6e08e1734bd8b8b3427dd5b8d8917896a6defa2609c6889fb90ce66d929ef31b'
files = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
errors = []
for name in filter(None, files):
    path = Path(name)
    if path.suffix.lower() in {'.nc', '.cnc', '.tap', '.min', '.tc', '.stp', '.step'} or re.fullmatch(r'O\d+', path.name, re.I):
        if name != SAMPLE:
            errors.append(f'Unapproved NC/CAD asset: {name}')
    if path.name.startswith('Flowmatic_NC_3D_Demo_') or 'nc-real-tests' in path.parts:
        errors.append(f'Private review artifact: {name}')
content = (ROOT / SAMPLE).read_bytes().replace(b'\r\n', b'\n')
if hashlib.sha256(content).hexdigest() != SAMPLE_SHA256:
    errors.append('Public example changed; review its provenance before updating the pinned checksum.')
if b'SYNTHETIC VIEWER SAMPLE - NOT A MACHINE PROGRAM' not in content:
    errors.append('Public example must identify itself as synthetic.')
sys.path.insert(0, str(ROOT))
from build_site import nc_browser_demo_section
for language in ('en', 'ar'):
    if re.search('[가-힣]', nc_browser_demo_section(language)):
        errors.append(f'Untranslated Korean text in {language} viewer markup.')
if errors:
    raise SystemExit('\n'.join(errors))
print('PASS: only the reviewed synthetic NC example is tracked; localized viewer markup verified')
