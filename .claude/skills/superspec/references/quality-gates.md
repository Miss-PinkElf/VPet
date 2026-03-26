# Quality Gates

Use this file during Apply and Close.

## Implementation Gates

- read the current artifacts before editing code
- implement against `tasks.md`, not memory
- mark task state explicitly
- if the task intent is unclear, ask instead of guessing
- if a design flaw appears, stop and update artifacts first

## Debugging Gates

Trigger systematic debugging when:

- tests fail unexpectedly
- the UI behaves differently from the design
- a fix attempt failed
- the root cause is unknown

Escalation rule:

- after three failed fix attempts, question the design or architecture instead of continuing to patch

## Verification Gates

Before claiming completion:

- re-read `proposal.md`
- re-read `tasks.md`
- run the relevant verification commands
- check runtime behavior
- confirm edge states and console health when relevant

## Frontend Hygiene Gates

Prefer these defaults unless the project uses another established pattern:

- keep types in dedicated type files or type sections
- keep constants in dedicated constant files
- keep mock data separate from production logic
- prefer modular stylesheet organization
- avoid `!important` and avoid ad-hoc inline styles unless there is a clear local reason

## Review Gates

- request review after meaningful milestones
- evaluate feedback technically
- route requirement or design changes back to Propose
