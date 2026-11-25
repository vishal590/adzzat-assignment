"""Reproducible author checks on disposable workspaces; never edits the starter."""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent


def verify(mode):
    with tempfile.TemporaryDirectory(prefix='task-trial-') as temporary:
        candidate = pathlib.Path(temporary) / 'workspace'
        shutil.copytree(ROOT / 'environment/workspace', candidate, ignore=shutil.ignore_patterns('__pycache__'))
        if mode != 'baseline':
            edit = ROOT / ('solution/solve.py' if mode == 'solution' else 'shortcuts/hardcode.py')
            subprocess.run([sys.executable, str(edit), str(candidate)], check=True, timeout=10)
        started = time.monotonic()
        grade = subprocess.run([sys.executable, str(ROOT / 'tests/grade.py'), str(candidate)],
                               capture_output=True, text=True, timeout=90)
        expected = 0 if mode == 'solution' else 1
        # unittest uses 1 for failures. Crashes/timeouts are not accepted shortcut demonstrations.
        demonstrated = grade.returncode == expected and (
            'OK' in grade.stderr if mode == 'solution' else 'FAILED (' in grade.stderr)
        if mode == 'shortcut':
            demonstrated = demonstrated and any(
                line.startswith('test_published_example (') and line.endswith(' ... ok')
                for line in grade.stderr.splitlines()
            )
        return {'mode': mode, 'returncode': grade.returncode, 'expected_returncode': expected,
                'demonstrated': demonstrated, 'seconds': round(time.monotonic() - started, 3),
                'stdout': grade.stdout, 'stderr': grade.stderr}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['all', 'baseline', 'solution', 'shortcut'], default='all', nargs='?')
    args = parser.parse_args()
    modes = ['baseline', 'solution', 'shortcut'] if args.mode == 'all' else [args.mode]
    results = [verify(mode) for mode in modes]
    print(json.dumps({'task': ROOT.name, 'python': sys.version, 'results': results}, indent=2))
    sys.exit(0 if all(result['demonstrated'] for result in results) else 1)
