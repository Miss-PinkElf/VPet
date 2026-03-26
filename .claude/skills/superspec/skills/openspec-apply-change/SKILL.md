---
name: openspec-apply-change
description: Use inside superspec to implement approved tasks from tasks.md while enforcing debugging, review, and verification gates.
---

# OpenSpec Apply For SuperSpec

Implement the approved change from `tasks.md`.

## Inputs

- approved `proposal.md`
- approved `design.md`
- approved `tasks.md`

## Steps

1. Read all current artifacts before coding.
2. Choose an execution mode:
   - sequential for coupled tasks
   - parallel for independent tasks
   - subagent mode for larger isolated units
3. For each task:
   - mark it `in_progress`
   - implement only that task’s scope
   - self-check against its acceptance criteria
   - mark it complete only with evidence
4. If failures appear, route immediately to [../superpowers-systematic-debugging/SKILL.md](../superpowers-systematic-debugging/SKILL.md).
5. If the task is a pure logic or transformation unit, optionally use [../superpowers-test-driven-development/SKILL.md](../superpowers-test-driven-development/SKILL.md).
6. If the task set is clearly independent, consider [../superpowers-dispatching-parallel-agents/SKILL.md](../superpowers-dispatching-parallel-agents/SKILL.md).
7. If the work is large and benefits from isolated implement/review loops, consider [../superpowers-subagent-driven-development/SKILL.md](../superpowers-subagent-driven-development/SKILL.md).

## Stop Conditions

Pause Apply and return to Propose when:

- a design flaw is exposed
- task boundaries are wrong
- new user constraints invalidate the design

## Guardrails

- do not implement from memory; implement from the artifacts
- do not batch unrelated fixes into one task
- do not keep guessing after repeated failures
