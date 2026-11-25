# AI tools used

- **Codex:** assisted with design, specifications, implementation, graders, references, shortcuts, Docker/Harbor packaging, the app, validation tooling, and documentation. The submitter directed scope/review, requested checks/corrections, and approved decisions.
- **Antigravity CLI 1.5.17 / Gemini 4 Hydrogen Medium:** produced separate clean-workspace candidates for both tasks. Both passed author-run local and Docker grading. Personal-account weekly quota was used; no API-key/Vertex billing route, paid subscription purchase, or credit purchase was configured for these runs.
- **Gemini CLI 0.71.1:** setup attempt only. Authentication completed but the consumer service rejected the retired client route; it solved neither task.
- **Read-only web tools:** checked public Bottle source/license and official documentation. Python, Node, Docker, and Harbor ran local checks; jsdom and headless Chrome supported frontend verification.

## Corrections

1. Corrected the suggestion that an agent attempt was mandatory: the brief permits self-solving.
2. Specified inventory quantity grammar, schema, sorting, errors, launch interface, and exclusions before final grading.
3. Replaced a weak shortcut proposal with an executed hardcoded candidate that passes the example and fails broader grading.
4. Distinguished a Docker sandbox permission error from daemon status, then verified actual builds/runs.
5. Removed a folder-name assumption in the author harness and ran renamed-copy checks.
6. Corrected the Gemini recommendation after finding the newer retirement notice; approved Antigravity trials supplied independent candidates.
7. Fixed an agent-trial report that tried to hash a cache directory and regraded the unchanged candidate. Expanded candidate capture to preserve additional workspace files.
8. Normalized Windows line endings in Harbor scripts and reran the final controls.

Independent trials had permission-related continuations; author graders executed runtime checks separately. Harbor oracle controls execute supplied references and are not independent model solves. Results and limitations are in [SUBMISSION.md](SUBMISSION.md).
