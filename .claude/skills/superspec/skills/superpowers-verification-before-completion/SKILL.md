---
name: superpowers-verification-before-completion
description: Use inside superspec before any completion claim, task closure, or archive step to require fresh verification evidence.
---

# Superpowers Verification Before Completion For SuperSpec

No completion claims without fresh evidence.

## Required Gate

1. Identify which command or check proves the claim.
2. Run it now.
3. Read the actual output and exit status.
4. Reconcile that result with `proposal.md` and `tasks.md`.
5. Only then state what passed and what still does not.

## Evidence Checklist

- task checklist status
- compile, typecheck, test, lint, or build output as applicable
- runtime behavior evidence for the changed flow
- manual spot-checks for empty, loading, error, and edge states when relevant

## Guardrails

- “should work” is not evidence
- partial verification cannot support a global completion claim
- if verification fails, return to Apply or Propose based on the failure source
