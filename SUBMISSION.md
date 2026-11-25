# Submission note

## Delivered and checked

Two standalone tasks use pinned, MIT-licensed Bottle 0.13.4. Task-01 requests independent shallow MultiDict snapshots; task-02 requests an exact CSV inventory HTTP summary without prescribing code changes. Each includes a statement/environment/difficulty, grader, reference, shortcut, Docker targets, and Harbor configuration. The sample page has a standard-library backend returning both tasks and a frontend list/detail view.

Executed on Windows Python 3.13.5 and Linux Docker Python 3.13.18; Harbor 0.15.0. Dockerfiles pin the base-image digest. Task READMEs record Bottle provenance and hashes.

| Check | Result |
| --- | --- |
| task-01 local and Docker controls | Starter rejected; reference passes 6 methods/subcases; shortcut rejected |
| task-02 local and Docker controls | Starter rejected; reference passes 5 methods including generated data and invalid-quantity subcases; shortcut rejected |
| Shortcut demonstrations | Both hardcoded candidates pass the published example and fail broader checks |
| Harbor controls | Starter 0, reference 1, shortcut 0 for both tasks; all six final jobs complete without trial errors |
| Standalone portability | Renamed copies run without the sibling task, page, or internal references |
| Solver separation | Solver images exclude author tests and references |
| Backend | Exactly two canonical records; assets work; unknown/private paths return 404 |
| Frontend | Both details, selections, history, deep links, and API-error state pass |
| Mobile Chrome | Both tasks pass at 320/390/430px with touch emulation, no horizontal overflow, and screenshot inspection |

README commands reproduce the controls and generate fresh reports under results/. Existing logs are not required inputs.

## Agent trials and ambiguity

Initial Codex-assisted self-solves used disposable starter copies, manual contract walkthroughs, and executed graders. Separate independent trials later used Antigravity CLI 1.5.17 with gemini-4-hydrogen-medium through the personal-account weekly quota. Each task received its own clean program/instruction/fixture/license workspace outside the author repository. No grader, reference, or evaluator feedback was supplied to improve the candidates.

Both candidates passed trusted author-run local and Linux Docker grading. Host permission interruptions required continuations; these were not uninterrupted single-shot runs. Agents did not execute their own runtime tests; author tooling did. Both reported no further ambiguity. These solver conversations ran on Windows; the later Harbor controls used nop/oracle, not an independent model inside Harbor.

Clarifications before final grading: task-01 defines shallow copying, alias behavior, missing keys without insertion, contained-object identity, scalar access, and scope excluding HeaderDict overrides. This is an assignment behavior change, not a claimed upstream defect. Task-02 defines quantity grammar/range, exact JSON/types, category preservation/sorting, quoting/line endings, launch/port/input selection, complete-error behavior, and explicit exclusions.

## Changes made

- Completed the initial inventory contract to avoid grading unstated requirements.
- Replaced a weak shortcut proposal with executed hardcoded-example controls.
- Removed a folder-name assumption in the author harness and reran renamed-copy checks.
- Added Harbor entry points and moved starters to environment/workspace/, retaining plain-Docker support.
- Normalized Harbor shell scripts to Unix line endings and reran all six controls.
- Made setup, validation output paths, and submission notes independent of internal reference documents.

## Limits and next steps

These few runs do not establish a general model success rate or measured difficulty. Shortcut demonstrations do not prove resistance to arbitrary malicious code or all evaluator attacks. Physical-device, Safari, and Firefox checks were not performed. Harbor emitted an image-OS preflight warning; actual execution completed with expected tests/rewards. Other versions/providers were not validated.

The app is for local review. Hosted deployment, a database, authentication, a third task, and solution-result UI were outside the delivered scope. Total focused effort across initial work and follow-ups was not separately tracked.

Next improvements would be additional independent solver attempts and targeted grader review based on observed failures/ambiguity. Tool use and corrections are disclosed in [AI_TOOLS.md](AI_TOOLS.md).
