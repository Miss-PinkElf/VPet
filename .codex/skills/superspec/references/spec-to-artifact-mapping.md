# Spec To Artifact Mapping

Use this guide when the user provides a PRD, design brief, system analysis, or annotated screenshots.

## Map Into `proposal.md`

Capture:

- business goal
- user value
- scope and non-goals
- impacted scenarios
- abnormal and edge cases
- unresolved decisions

Questions to ask:

- what is the minimum acceptable shipped behavior?
- which scenarios are explicitly out of scope?
- what failure or empty states matter?

## Map Into `design.md`

Capture:

- page and component structure
- state ownership
- data flow
- API or service contracts
- reuse points
- performance or migration risks

Questions to ask:

- which existing modules can be reused?
- where does new state live?
- what interfaces or contracts might change?

## Map Into `tasks.md`

Capture:

- setup and dependency tasks
- UI tasks
- state or service tasks
- test or verification tasks
- follow-up cleanup tasks only if they are required for the change

Task quality rules:

- each task should have one main concern
- each task should be small enough to verify independently
- avoid bundling implementation, debugging, and verification into a vague mega-task
