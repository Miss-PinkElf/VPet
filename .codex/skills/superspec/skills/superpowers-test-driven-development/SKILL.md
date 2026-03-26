---
name: superpowers-test-driven-development
description: Use inside superspec for pure logic, data transformation, or boundary-heavy behavior where a failing test should define the work before implementation.
---

# Superpowers TDD For SuperSpec

Use TDD selectively where it materially increases correctness.

## Best Fits

- pure calculation
- data formatting or transformation
- parser or mapper logic
- edge-case-heavy utilities

## Cycle

1. Write one failing test for one behavior.
2. Run it and confirm the failure is the expected one.
3. Write the smallest production code that makes it pass.
4. Re-run the test and any nearby affected tests.
5. Refactor only while keeping tests green.

## Guardrails

- if you did not see the test fail, you do not know whether it protects the behavior
- avoid over-engineering beyond what the test requires
- if this is mostly UI wiring or exploratory debugging, TDD is optional rather than mandatory
