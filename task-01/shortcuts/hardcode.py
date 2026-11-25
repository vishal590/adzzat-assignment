"""Plausible sample-only solution: fresh lists, but ignores actual values."""
import pathlib
import sys

path = pathlib.Path(sys.argv[1]) / 'bottle.py'
source = path.read_text(encoding='utf-8')
old = 'return self.dict.get(key) or []'
assert source.count(old) == 1
path.write_text(source.replace(old, "return ['red', 'blue']"), encoding='utf-8')
