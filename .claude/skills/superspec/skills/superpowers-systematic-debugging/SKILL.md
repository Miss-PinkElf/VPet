---
name: superpowers-systematic-debugging
description: Use inside superspec whenever Apply encounters a bug, failing test, unexpected behavior, or repeated unsuccessful fixes.
---

# Superpowers Systematic Debugging For SuperSpec

No fixes without root-cause investigation first.

## Required Sequence

1. Reproduce the failure reliably.
2. Read errors and traces carefully.
3. Check recent changes and relevant dependencies.
4. Gather evidence at component boundaries.
5. Form one hypothesis at a time.
6. Test the smallest possible change.
7. Implement the real fix only after the cause is understood.

## Stop Rules

- if you cannot reproduce, gather more data instead of guessing
- if two attempts have already failed, slow down and re-check assumptions
- if three attempts fail, question the design or architecture and consider rolling back to Propose

## Outputs

- confirmed root cause
- evidence chain
- minimal fix plan
- regression proof after the fix
