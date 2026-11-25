# Taskroom

Two verified Harbor tasks based on MIT-licensed Bottle 0.13.4 and a minimal full-stack task catalog. Task-01 is a Python behavior change; task-02 specifies an inventory-summary HTTP outcome.

## Contents

```text
task-01/       MultiDict snapshot task, grader, reference, shortcut
task-02/       CSV inventory HTTP task, grader, reference, shortcut
app/           Python backend and HTML/CSS/JavaScript list/detail page
tools/         Reproducible validation and optional frontend checks
SUBMISSION.md  Checks, changes, agent trials, limitations, next steps
AI_TOOLS.md    AI tools used and corrections
```

Each task runs independently. Its instruction.md contains the statement, environment, and difficulty. Starters are intentionally unfinished; reference solutions are separate author material.

## Setup and run

Use Python 3.13, Docker with Linux containers for container checks, and Harbor 0.15.0 for Harbor checks. The app and Python graders need no pip/npm dependencies, account, or API key. Docker may download the pinned base image once.

```sh
python app/server.py --port 8000
```

Open http://127.0.0.1:8000. GET /api/tasks returns both complete task records from their task.json files. Select a card for its statement, environment, and difficulty. URL hashes support direct links and browser history. Stop the loopback-only local server with Ctrl+C.

## Test

From the repository root:

```sh
python tools/validate.py
python tools/validate.py --docker
python tools/verify_harbor.py
```

The first command runs local task controls, renamed-copy portability checks, backend tests, and JavaScript syntax checking when Node is installed. --docker also builds solver/evaluator images, runs container controls, and checks solver/evaluator separation. The Harbor command runs six local Docker controls without model calls.

Expected outcomes per task: starter fails, reference passes, and shortcut fails while passing the published example. Harbor rewards are **0, 1, 0**. Overall author-harness exit 0 means those expectations held. Generated reports/logs go under results/ and are not required inputs.

Individual checks:

```sh
python task-01/verify.py all
python task-02/verify.py all
python -m unittest discover -s app -v
```

Grade an edited candidate directly, using a trusted evaluator copy:

```sh
python task-01/tests/grade.py /absolute/path/to/candidate-workspace
python task-02/tests/grade.py /absolute/path/to/candidate-workspace
```

Direct grading exits 0 only for a passing candidate. Each task README explains its contract, shortcut, and manual self-solve walkthrough.

## Harbor

Each task has task.toml, instruction.md, environment/Dockerfile, tests/test.sh, and solution/solve.sh. Starter files live at environment/workspace/ on the host and /workspace in the container. The initial image excludes author tests/reference; Harbor uploads tests after the agent phase. External runtime networking is disabled.

```sh
harbor run -p task-01 -a oracle --env docker --jobs-dir jobs
harbor run -p task-02 -a oracle --env docker --jobs-dir jobs
```

oracle executes the supplied reference and should earn 1. Replacing it with nop leaves the starter unchanged and should earn 0. The full tools/verify_harbor.py harness additionally checks hardcoded shortcuts in isolated copies and verifies actual test output and job-error counts. No account, paid API, upload, or registry publication is needed.

## Plain Docker

```sh
docker build --target solver -t adzzat-task-01-solver task-01
docker build --target evaluator -t adzzat-task-01-evaluator task-01
docker run --rm --network none adzzat-task-01-evaluator
docker build --target solver -t adzzat-task-02-solver task-02
docker build --target evaluator -t adzzat-task-02-evaluator task-02
docker run --rm --network none adzzat-task-02-evaluator
```

Give only solver images/workspaces to solvers. Evaluator images and this inspectable author repository include tests and references. Each task README describes interactive runs and grading a read-only candidate mount. Specific shortcut rejection is not a claim of arbitrary-adversary security.

## Optional frontend checks

With Node 22 installed and the page running, in another terminal:

```sh
cd tools/frontend-qa
npm ci --ignore-scripts --no-audit --no-fund
npm test
```

This uses jsdom to check both details, selections, history, deep links, and API-error handling. The app runtime itself has no npm dependencies.

For Chrome mobile viewport/touch/layout checks, run from the repository root after the optional install:

```sh
node tools/frontend-qa/mobile.cjs
```

The default executable is Windows Chrome; set CHROME_PATH for another installation. Both tasks are checked at 320/390/430px; screenshots go under results/mobile/. This is emulation, not physical-device or Safari/Firefox validation.

See [the submission note](SUBMISSION.md) for results and limits and [the AI disclosure](AI_TOOLS.md) for tools and corrections.
