"""Run local Harbor controls without any model/API calls.

Usage: python tools/verify_harbor.py
Requires Harbor 0.15.0 and Docker. Writes evidence under results/harbor.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'results/harbor'


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output(['harbor', '--version'], text=True).strip()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stage = OUTPUT / 'staging' / stamp
    records = []
    for task in ('task-01', 'task-02'):
        for mode, agent, expected in [('baseline', 'nop', 0), ('reference', 'oracle', 1),
                                      ('shortcut', 'oracle', 0)]:
            task_path = ROOT / task
            if mode == 'shortcut':
                task_path = stage / task
                shutil.copytree(ROOT / task, task_path,
                                ignore=shutil.ignore_patterns('__pycache__'))
                shutil.copyfile(task_path / 'shortcuts/hardcode.py',
                                task_path / 'solution/hardcode.py')
                (task_path / 'solution/solve.sh').write_text(
                    '#!/bin/sh\nset -eu\npython /solution/hardcode.py /workspace\n',
                    encoding='utf-8', newline='\n')
            job = f'{stamp}-{task}-{mode}'
            command = ['harbor', 'run', '-p', str(task_path), '-a', agent,
                       '--env', 'docker', '--jobs-dir', str(OUTPUT / 'jobs'),
                       '--job-name', job, '--n-concurrent', '1']
            started = datetime.now(timezone.utc).isoformat()
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=420)
            folder = OUTPUT / 'jobs' / job
            result = json.loads((folder / 'result.json').read_text(encoding='utf-8'))
            rewards = list(folder.glob('*/verifier/reward.txt'))
            reward = float(rewards[0].read_text()) if len(rewards) == 1 else None
            verifier_output = (rewards[0].parent / 'test-stdout.txt').read_text(
                encoding='utf-8', errors='replace') if rewards else ''
            demonstrated = (run.returncode == 0 and reward == expected
                            and result['stats']['n_completed_trials'] == 1
                            and result['stats']['n_errored_trials'] == 0
                            and ('OK' in verifier_output if mode == 'reference'
                                 else 'FAILED (' in verifier_output))
            if mode == 'shortcut':
                demonstrated = demonstrated and any(
                    line.startswith('test_published_example (') and line.endswith(' ... ok')
                    for line in verifier_output.splitlines())
            record = dict(task=task, mode=mode, agent=agent, expected_reward=expected,
                          reward=reward, demonstrated=demonstrated, command=command,
                          started_utc=started, returncode=run.returncode,
                          stdout=run.stdout, stderr=run.stderr,
                          result=str((folder / 'result.json').relative_to(ROOT)))
            records.append(record)
            (OUTPUT / f'{task}-{mode}.json').write_text(
                json.dumps(record, indent=2), encoding='utf-8')
            print(f'{task} {mode}: reward={reward}; expected={expected}; '
                  f'{"PASS" if demonstrated else "FAIL"}', flush=True)
    manifest = {}
    for task in ('task-01', 'task-02'):
        for p in (ROOT / task).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                manifest[p.relative_to(ROOT).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    summary = dict(harbor_version=version, model_calls=False, source_hashes=manifest,
                   checks=records, passed=all(r['demonstrated'] for r in records))
    (OUTPUT / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
