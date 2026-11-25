# task-02: Inventory summary over HTTP

Read [instruction.md](instruction.md) for the outcome, environment, and difficulty. `task.json` is the canonical catalog metadata; the instruction is its readable counterpart.

## Run and grade

From this task directory, with Python 3.13:

```sh
python verify.py all
```

The author check creates three disposable workspace copies and expects baseline failure, reference-solution success, and shortcut failure. Exit 0 means those expectations held. The shipped starter is deliberately unsolved. Select `baseline`, `solution`, or `shortcut` for one trial.

To grade any edited workspace using a trusted evaluator copy:

```sh
python tests/grade.py /absolute/path/to/candidate-workspace
```

Direct grading exits 0 only if the candidate passes, 1 for failed tests. The grader launches `python server.py --port PORT` from the candidate directory with an absolute `INVENTORY_CSV` path. It tests real HTTP responses and always terminates its owned processes. No module name or algorithm is inspected.

## Docker

From this task directory:

```sh
docker build --target solver -t adzzat-task-02-solver .
docker run --rm -it --network none adzzat-task-02-solver
docker build --target evaluator -t adzzat-task-02-evaluator .
docker run --rm --network none adzzat-task-02-evaluator
```

The solver works at `/workspace` and launches `python server.py --port 8080`. Its default `INVENTORY_CSV` is `/workspace/inventory.csv`. Both Python and Bottle are supplied; no installs are needed. For browser access during manual development use `-p 127.0.0.1:8080:8080` instead of `--network none`. For automated grading, loopback requests work with external networking disabled.

Only give the `solver` target to a solver. The default build target is the author `evaluator`; specify `--target solver` explicitly. To persist work, mount a disposable copy of `environment/workspace/` at `/workspace`; read the task instruction separately if the mount hides it.

To grade a completed candidate without trusting its own tests:

```sh
docker run --rm --network none --mount type=bind,source=/absolute/path/to/candidate-workspace,target=/candidate,readonly adzzat-task-02-evaluator python /task-02/tests/grade.py /candidate
```

Use an absolute host path appropriate to your OS. No sibling task, package registry, or sample-page service is required.

## Harbor 0.15.0

This directory is also a standalone Harbor task. From this directory's parent, run:

```sh
harbor run -p task-02 -a oracle --env docker --jobs-dir jobs
harbor run -p task-02 -a nop --env docker --jobs-dir jobs
```

The oracle installs the reference solution and should earn reward 1; nop leaves the starter unchanged and should earn 0. Neither invokes a model. `tests/test.sh` initializes `/logs/verifier/reward.txt` to 0, runs the trusted behavioral grader against `/workspace`, and writes 1 only on success. The verifier uses no downloads or additional packages. `task.toml` sets a 120-second verifier timeout and disables external runtime networking. `environment/` alone is the image build context and contains starter source and its license, excluding tests and solutions. Harbor provides the instruction and uploads verification files separately.

The existing root Dockerfile and `verify.py` commands remain supported. Both use the same `environment/workspace/` starter. No sibling task or root tooling is needed. A repository-level `python tools/verify_harbor.py` additionally checks the shortcut in an isolated copied task; this convenience tool is optional.

## Grader and shortcut

Five unittest methods cover the example, header-only input, repeated requests, aggregation, Unicode sorting, quoted commas, category space/case preservation, leading zeros, zero/maximum quantities, LF/CRLF, generated datasets up to 100 rows, and ten explicitly invalid quantity forms. Tests check status, JSON media type, exact schema/data, and integer types.

`shortcuts/hardcode.py` serves the sample books response regardless of the input. It passes the published example, but fails other datasets and error cases. `python verify.py shortcut` requires that example pass and full-grader failure.

## Manual self-solve walkthrough

1. Launch the starter on a temporary port against the sample CSV. It returns an empty summary, so the example fails.
2. Inspect the CSV contract: parse records with quoting support and validate ASCII quantity syntax and range before accepting a total.
3. Aggregate identical categories without normalizing their names, sort the output, and return integer quantities. Any invalid quantity makes the whole request fail with the specified JSON 400 response.
4. Launch the reference service with separate fixtures and verify repeated HTTP responses, boundaries, and errors. Run the sample-only shortcut as a negative control.

Reference: `solution/server.py`, installed into a fresh copy by `solution/solve.py`. Ambiguities resolved before grading: startup input selection, launch/port interface, precise quantity grammar/range, schema, sorting, whole-input error behavior, and explicit exclusions. The implementation is free to read at startup or per request. This initial walkthrough is a Codex-assisted reference self-solve with executed tests, not a human-only or model-success claim. A later separate Antigravity CLI 1.5.17 / Gemini 4 Hydrogen (Medium) conversation produced a candidate that passes this grader locally and in Linux Docker. The conversation had a host permission interruption, and the agent did not execute its own runtime checks. The root submission note summarizes these trials; it is not needed to run or grade this task.

## Provenance

Vendored `environment/workspace/bottle.py` is unmodified Bottle 0.13.4 from https://github.com/bottlepy/bottle/tree/0.13.4. SHA-256: `e7e27201eda83d31324484235b1f17b77b26c1d1c015023101fdd84f5fd70176`. Copyright Marcel Hellkamp; retained MIT notice: `LICENSE.bottle`. The small starter application, fixture, instructions, graders, and solutions are assignment-specific work.
