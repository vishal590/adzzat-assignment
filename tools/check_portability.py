"""Check copied task packages without docs, siblings, or original folder names."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
results = []
with tempfile.TemporaryDirectory(prefix='standalone-tasks-') as temporary:
    for task, destination in (('task-01', 'renamed-python'), ('task-02', 'renamed-http')):
        copied = Path(temporary) / destination
        shutil.copytree(root / task, copied, ignore=shutil.ignore_patterns('__pycache__'))
        assert not (copied.parent / 'docs').exists()
        for mode in ('solution', 'shortcut'):
            command = [sys.executable, str(copied / 'verify.py'), mode]
            run = subprocess.run(command, cwd=copied, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=90)
            results.append({'task': task, 'copied_name': destination, 'mode': mode,
                            'command': command, 'cwd': str(copied), 'returncode': run.returncode,
                            'stdout': run.stdout, 'stderr': run.stderr})
print(json.dumps({'results': results, 'passed': all(r['returncode'] == 0 for r in results)}, indent=2))
sys.exit(0 if all(r['returncode'] == 0 for r in results) else 1)
