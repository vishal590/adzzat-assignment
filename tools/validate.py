"""Run author checks and save exact commands/results under results.

Usage: python tools/validate.py [--docker]
Each task also works on its own via its local verify.py and Dockerfile.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'results'


def now():
    return datetime.now(timezone.utc).isoformat()


def command(args, filename, timeout=180):
    started = now()
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=timeout)
    record = {'command': args, 'cwd': str(ROOT), 'started_utc': started,
              'finished_utc': now(), 'returncode': result.returncode,
              'stdout': result.stdout, 'stderr': result.stderr}
    (EVIDENCE / filename).write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(('PASS' if result.returncode == 0 else 'FAIL'), filename, flush=True)
    if result.returncode:
        print(result.stdout[-3000:] + result.stderr[-3000:])
        raise SystemExit(result.returncode)
    return record


def manifest():
    files = []
    for folder in ('task-01', 'task-02', 'app', 'tools'):
        for path in sorted((ROOT / folder).rglob('*')):
            if path.is_file() and not {'__pycache__', 'node_modules'}.intersection(path.parts) and path.suffix != '.pyc':
                files.append({'path': path.relative_to(ROOT).as_posix(),
                              'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docker', action='store_true', help='Also build and run all four Docker targets')
    args = parser.parse_args()
    EVIDENCE.mkdir(exist_ok=True)
    summary = {'started_utc': now(), 'host': platform.platform(), 'python': sys.version,
               'docker_requested': args.docker, 'source_manifest': manifest(), 'checks': []}
    for task in ('task-01', 'task-02'):
        record = command([sys.executable, f'{task}/verify.py', 'all'], f'{task}-local-command.json')
        report = json.loads(record['stdout'])
        (EVIDENCE / f'{task}-local.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        summary['checks'].append({'task': task, 'local': True})
    command([sys.executable, '-m', 'unittest', 'discover', '-s', 'app', '-v'], 'app-command.json')
    record = command([sys.executable, 'tools/check_portability.py'], 'portability-command.json')
    (EVIDENCE / 'portability.json').write_text(record['stdout'], encoding='utf-8')
    if shutil.which('node'):
        command(['node', '--check', 'app/static/app.js'], 'frontend-check.json')
    if args.docker:
        command(['docker', 'version'], 'docker-version.json')
        for task in ('task-01', 'task-02'):
            for target in ('solver', 'evaluator'):
                image = f'adzzat-{task}-{target}'
                command(['docker', 'build', '--target', target, '-t', image, task], f'{task}-{target}-build.json', 300)
                command(['docker', 'image', 'inspect', image], f'{task}-{target}-image.json')
            image = f'adzzat-{task}-evaluator'
            record = command(['docker', 'run', '--rm', '--network', 'none', '--cap-drop', 'ALL',
                              '--security-opt', 'no-new-privileges', image], f'{task}-docker-command.json')
            report = json.loads(record['stdout'])
            (EVIDENCE / f'{task}-docker.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            code = ("from pathlib import Path; import bottle; "
                    "assert bottle.__version__ == '0.13.4'; "
                    "assert Path('/workspace/instruction.md').is_file(); "
                    "assert not any(Path(p).exists() for p in "
                    "['/task-01','/task-02','/docs','/workspace/tests','/workspace/solution']); "
                    "print('solver source and instruction present; author artifacts absent')")
            command(['docker', 'run', '--rm', '--network', 'none', f'adzzat-{task}-solver',
                     'python', '-c', code], f'{task}-solver-separation.json')
            summary['checks'].append({'task': task, 'docker': True, 'solver_separation': True})
    summary['finished_utc'] = now()
    summary['passed'] = True
    (EVIDENCE / ('validation-docker.json' if args.docker else 'validation-local.json')).write_text(
        json.dumps(summary, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
