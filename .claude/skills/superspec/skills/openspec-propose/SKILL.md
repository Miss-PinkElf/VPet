---
name: openspec-propose
description: Use inside superspec after alignment is approved to create or update proposal.md, design.md, and tasks.md for a planned change.
---

# OpenSpec Propose For SuperSpec

Create executable artifacts from the approved direction.

## Inputs

- the confirmed output of Align or Mini Align
- relevant codebase context
- any user-provided PRD, design spec, or system analysis

## Steps

1. Confirm the change name and working location.
2. If OpenSpec CLI is available, create or select the change workspace.
3. Read the artifact templates:
   - [../../assets/templates/proposal-template.md](../../assets/templates/proposal-template.md)
   - [../../assets/templates/design-template.md](../../assets/templates/design-template.md)
   - [../../assets/templates/tasks-template.md](../../assets/templates/tasks-template.md)
4. If external specs exist, map them with [../../references/spec-to-artifact-mapping.md](../../references/spec-to-artifact-mapping.md).
5. Write:
   - `proposal.md`: what, why, scope, non-goals, edge cases, open questions
   - `design.md`: structure, interfaces, data flow, reuse, risks
   - `tasks.md`: small tasks with acceptance checks
6. Request user approval unless the user explicitly authorized direct implementation.

## Quality Bar

- proposal covers all affected change points and abnormal paths
- design explains the key technical path instead of hand-waving it
- tasks are atomic, ordered, and independently verifiable
- anything still uncertain is called out explicitly

## Guardrails

- do not skip artifacts because the change feels simple
- do not use chat history as the final truth source once artifacts exist
- if agreement is not actually complete, return to Align
