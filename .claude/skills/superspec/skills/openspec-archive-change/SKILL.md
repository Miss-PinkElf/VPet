---
name: openspec-archive-change
description: Use inside superspec after review and verification have passed to archive or formally close a completed change.
---

# OpenSpec Archive For SuperSpec

Close the lifecycle only after the change is actually done.

## Preconditions

- proposal commitments are implemented
- tasks are complete or explicitly dispositioned
- verification evidence exists
- review findings are resolved or deliberately accepted

## Steps

1. Confirm which change is being archived.
2. Re-check artifact and task completion state.
3. Check whether delta specs need to sync back to the main spec set.
4. Archive the change in the project’s OpenSpec structure, or record equivalent closure if the project uses a lighter workflow.
5. Summarize what shipped, what evidence passed, and what was synced.

## Guardrails

- never archive straight from “implementation seems done”
- if verification failed, return to Apply
- if review feedback implies design or scope changes, return to Propose
