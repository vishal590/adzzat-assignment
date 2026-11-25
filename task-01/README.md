# task-01: Independent value-list snapshots

Read [instruction.md](instruction.md) for the solver statement, environment, and difficulty. `task.json` is the canonical catalog metadata; the instruction is its readable counterpart.

## Run and grade

From this task directory, with Python 3.13:

```sh
python verify.py all
```

This author check copies `environment/workspace/` to fresh temporary directories. It expects baseline failure, reference-solution success, and shortcut failure. Exit 0 means those three expectations held; it does **not** mean the unsolved starter passed. Use `baseline`, `solution`, or `shortcut` instead of `all` for an individual trial.

To grade a solver's edited workspace directly, use the trusted grader:

```sh
python tests/grade.py /absolute/path/to/candidate-workspace
```

Direct grading exits 0 only for a passing candidate, 1 for failed tests. Keep an unchanged evaluator copy outside the solver environment.

## Docker

Run these commands from this task directory. Build needs access to the pinned Python image; task execution needs no internet.

```sh
docker build --target solver -t adzzat-task-01-solver .
docker run --rm -it --network none adzzat-task-01-solver
docker build --target evaluator -t adzzat-task-01-evaluator .
docker run --rm --network none adzzat-task-01-evaluator
```

Only distribute the `solver` target to a solver. Its `/workspace` contains source and the instruction; it has no author grader, shortcut, or reference solution. The default build target is the author `evaluator`, so specify `--target solver` explicitly.

For persistent edits, mount a disposable copy of `environment/workspace/` at `/workspace`; read `instruction.md` separately if the mount hides it. Then mount that completed candidate read-only into the evaluator:

```sh
docker run --rm --network none --mount type=bind,source=/absolute/path/to/candidate-workspace,target=/candidate,readonly adzzat-task-01-evaluator python /task-01/tests/grade.py /candidate
```

Use an absolute host path appropriate to your OS. No sibling task or sample-page files are required.

## Harbor 0.15.0

This directory is also a standalone Harbor task. From this directory's parent, run:

```sh
harbor run -p task-01 -a oracle --env docker --jobs-dir jobs
harbor run -p task-01 -a nop --env docker --jobs-dir jobs
```

The oracle installs the reference solution and should earn reward 1; nop leaves the starter unchanged and should earn 0. Neither invokes a model. `tests/test.sh` initializes `/logs/verifier/reward.txt` to 0, runs the trusted behavioral grader against `/workspace`, and writes 1 only on success. The verifier uses no downloads or additional packages. `task.toml` sets a 120-second verifier timeout and disables external runtime networking. `environment/` alone is the image build context and contains starter source and its license, excluding tests and solutions. Harbor provides the instruction and uploads verification files separately.

The existing root Dockerfile and `verify.py` commands remain supported. Both use the same `environment/workspace/` starter. No sibling task or root tooling is needed. A repository-level `python tools/verify_harbor.py` additionally checks the shortcut in an isolated copied task; this convenience tool is optional.

## Grader and shortcut

Six unittest methods cover both method names, edits in both directions, fresh missing-key lists, order/duplicates, scalar access, shallow value identity, varied keys, and separate instances. Tests check behavior, not a source-code pattern.

`shortcuts/hardcode.py` returns `['red', 'blue']` for every request. It passes the published example, including clearing a fresh list, but fails varied inputs, missing keys, and mutable-value identity. `python verify.py shortcut` executes this demonstration and requires the example to pass while the full grader fails.

## Manual self-solve walkthrough

1. Trace `MultiDict.getall`: the pinned implementation returns its internal list for an existing key. Confirm that clearing the result changes stored values.
2. Return a new outer list. Preserve nested value references, insertion order, and duplicates.
3. Check `getlist = getall`: editing the original method definition updates the alias at class creation. A separate override must handle the alias too.
4. Run the six tests on the edited copy and run the hardcoded negative control.

Reference edit: `solution/solve.py`. Ambiguities resolved before grading: this is an intentional new contract; only MultiDict is in scope, the copy is shallow, missing keys must not be inserted, and HeaderDict overrides are excluded. This initial walkthrough is a Codex-assisted reference self-solve with executed tests, not evidence of human-only solving or agent success rates. A later separate Antigravity CLI 1.5.17 / Gemini 4 Hydrogen (Medium) conversation produced a candidate that passes this grader locally and in Linux Docker. The conversation had host permission interruptions, and the agent did not execute its own runtime checks. The root submission note summarizes these trials; it is not needed to run or grade this task.

## Provenance

Vendored `environment/workspace/bottle.py` is unmodified Bottle 0.13.4 from https://github.com/bottlepy/bottle/tree/0.13.4. SHA-256: `e7e27201eda83d31324484235b1f17b77b26c1d1c015023101fdd84f5fd70176`. Copyright Marcel Hellkamp; MIT terms are in `LICENSE.bottle`. Task instructions, grader, solution edit, and shortcut demonstration were created for this assignment.
