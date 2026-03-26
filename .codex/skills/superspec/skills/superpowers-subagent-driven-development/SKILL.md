---
name: superpowers-subagent-driven-development
description: Use inside superspec for larger Apply phases where isolated implementer and reviewer loops per task improve quality and keep context under control.
---

# Superpowers Subagent-Driven Development For SuperSpec

Use this mode when the task list is large enough that isolated execution and review loops are cheaper than one overloaded session.

## Pattern

For each task:

1. give one implementer the exact task text, artifact context, and acceptance criteria
2. let the implementer complete the task and self-check it
3. run a spec-compliance review against the artifacts
4. run a code-quality review
5. close the task only after both gates pass

## Best Fits

- many tasks with low or medium coupling
- large codebase surface area
- need for strong separation between implementation and review

## Guardrails

- do not dispatch multiple implementers onto the same file set without coordination
- do not skip the review loops just because the implementer reported success
- if repeated review failures reveal a flawed task or design, return to Propose
