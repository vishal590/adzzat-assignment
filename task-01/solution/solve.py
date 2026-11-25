"""Reference edit, applied to a disposable copy of the starter."""
import pathlib
import sys

path = pathlib.Path(sys.argv[1]) / 'bottle.py'
source = path.read_text(encoding='utf-8')
old = 'return self.dict.get(key) or []'
assert source.count(old) == 1, 'Expected the pinned MultiDict implementation'
path.write_text(source.replace(old, 'return list(self.dict.get(key) or [])'), encoding='utf-8')
