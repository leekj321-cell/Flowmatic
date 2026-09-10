"""Verify the build hook. This installer must never generate or modify tests."""
from pathlib import Path
import ast
root=Path(__file__).resolve().parents[1]
source=(root/'build_site.py').read_text()
ast.parse(source)
assert 'business_narrative.configure(globals())' in source, 'Missing explicit narrative build hook'
assert (root/'homepage-declaration.json').exists(), 'Missing locked declaration'
print('Build hook verified. No source or test files rewritten.')
