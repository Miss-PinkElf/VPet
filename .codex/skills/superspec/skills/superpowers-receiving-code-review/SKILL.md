---
name: superpowers-receiving-code-review
description: Use inside superspec when review feedback arrives and each suggestion needs technical verification before implementation.
---

# Superpowers Receiving Code Review For SuperSpec

Feedback is input to evaluate, not an order to obey blindly.

## Sequence

1. Read all feedback calmly.
2. Restate or clarify anything ambiguous.
3. Verify each point against the codebase and the approved artifacts.
4. Fix technically valid issues one at a time.
5. Push back with evidence when the feedback is incorrect or out of scope.

## Rollback Rule

If review feedback implies a requirement or design change, return to Propose instead of silently patching around it.

## Guardrails

- no performative agreement
- no partial implementation if key items are unclear
- no blind acceptance of suggestions that break current behavior or violate the plan
