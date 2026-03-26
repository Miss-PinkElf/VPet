---
name: superspec
description: Use when the user asks for planned feature delivery, page or component work, UI/UX changes, or any implementation that should follow an OpenSpec lifecycle with Superpowers quality gates. Trigger even for small existing-page tweaks; route discussion-only work to internal explore and root-cause bug work to internal debugging.
---

# SuperSpec

OpenSpec manages the lifecycle. Superpowers manages the quality gates.

Use this skill as a single orchestrator for frontend or product-facing work that needs a deliberate flow:

```txt
Classify -> Align -> Propose -> Apply -> Review/Verify -> Archive
```

This skill is self-contained. Read sibling files inside this directory tree instead of assuming external skills.

## Scope And Routing

| Request shape | Route |
| --- | --- |
| Pure discussion, solution exploration, requirement clarification | Read [skills/openspec-explore/SKILL.md](skills/openspec-explore/SKILL.md) |
| Pure bug fixing, root cause unknown, existing failure first | Read [skills/superpowers-systematic-debugging/SKILL.md](skills/superpowers-systematic-debugging/SKILL.md) |
| Small explicit tweak on an existing page or component | Use light path: Classify -> Mini Align -> Propose -> Apply -> Verify |
| Normal feature delivery, page rebuild, component refactor, UX optimization | Use standard path: Classify -> Align -> Propose -> Apply -> Review/Verify -> Archive |
| Brand-new large module with major architecture design | Use a separate planning skill outside SuperSpec |

### Light Path Signals

Most of these should be true:

- Target state is already clear
- Change stays inside existing pages, components, interactions, or styles
- No new end-to-end business flow is needed
- No broad module, API contract, or state architecture design is required

Exit the light path immediately if ambiguity, multi-page impact, or multiple valid implementation strategies appear.

## Core Rules

### 1. OpenSpec Owns Stage Progress

OpenSpec answers:

- which stage the work is in
- what artifact is required now
- what must be true before moving forward
- where to roll back when new information invalidates the current stage

### 2. Superpowers Only Hooks At Gates

| Gate | Read | Why |
| --- | --- | --- |
| Before proposal | [skills/superpowers-brainstorming/SKILL.md](skills/superpowers-brainstorming/SKILL.md) | Align requirements, constraints, and options |
| During apply when failures appear | [skills/superpowers-systematic-debugging/SKILL.md](skills/superpowers-systematic-debugging/SKILL.md) | Find root cause before fixes |
| During apply for pure logic | [skills/superpowers-test-driven-development/SKILL.md](skills/superpowers-test-driven-development/SKILL.md) | Raise correctness for pure transformations |
| After implementation | [skills/superpowers-requesting-code-review/SKILL.md](skills/superpowers-requesting-code-review/SKILL.md) and [skills/superpowers-receiving-code-review/SKILL.md](skills/superpowers-receiving-code-review/SKILL.md) | Review before claiming completion |
| Before completion | [skills/superpowers-verification-before-completion/SKILL.md](skills/superpowers-verification-before-completion/SKILL.md) | Require evidence, not confidence |

### 3. Artifact Truth Source

From Step 2 onward, these files are the only source of truth:

- `proposal.md`
- `design.md`
- `tasks.md`

Conversation history is not the final decision record unless it has been synced into those artifacts.

## Workflow

## Step 0: Classify

Decide whether the task belongs in SuperSpec, and whether it should use the light path or standard path.

Checklist:

1. Determine if the request is discussion, bug fixing, planned implementation, or large greenfield planning.
2. Decide light path vs standard path.
3. Announce the chosen route before continuing.

## Step 1: Align

Goal: align on intent, constraints, boundaries, and preferred direction before proposal artifacts exist.

Always perform alignment. The difference is depth, not existence.

### Standard Align

Use for ambiguous or larger work.

Required actions:

1. Scan the relevant code, docs, and existing patterns.
2. Extract unknowns and risks.
3. Ask one question at a time.
4. Present 2-3 approaches with tradeoffs and a recommendation.
5. Summarize the proposed direction and wait for explicit user confirmation.

Read:

- [references/brainstorming-guide.md](references/brainstorming-guide.md)
- [skills/superpowers-brainstorming/SKILL.md](skills/superpowers-brainstorming/SKILL.md)

### Mini Align

Use only for small, clear changes.

Minimum bar:

1. Scan the code and any supplied docs.
2. Extract the critical confirmation points.
3. Ask at least one interactive confirmation question.
4. Summarize the recommended plan.
5. Wait for confirmation before proposal.

Never skip user confirmation just because a spec or design doc exists.

## Step 2: Propose

Turn the aligned conclusion into executable artifacts.

Actions:

1. Read [skills/openspec-propose/SKILL.md](skills/openspec-propose/SKILL.md).
2. Create or select the change workspace.
3. Produce `proposal.md`, `design.md`, and `tasks.md`.
4. If the user supplied a spec, map it into artifacts with [references/spec-to-artifact-mapping.md](references/spec-to-artifact-mapping.md).
5. Break tasks into independently implementable and independently verifiable units.

Templates:

- [assets/templates/proposal-template.md](assets/templates/proposal-template.md)
- [assets/templates/design-template.md](assets/templates/design-template.md)
- [assets/templates/tasks-template.md](assets/templates/tasks-template.md)

Do not enter Step 3 until:

- proposal covers scope and edge cases
- design explains structure, interfaces, and data flow
- tasks are atomic enough to execute and verify independently
- the user approves the artifacts or explicitly authorizes direct implementation

## Step 3: Apply

Implement from `tasks.md`, not from memory.

Actions:

1. Read [skills/openspec-apply-change/SKILL.md](skills/openspec-apply-change/SKILL.md).
2. Choose execution mode.
3. Work task by task from `tasks.md`.
4. Mark a task `in_progress` before starting.
5. Self-check, then mark it done only after the acceptance criteria is met.
6. If implementation reveals a design problem, stop and roll back to Step 2.

### Execution Mode

| Mode | Use when | Read |
| --- | --- | --- |
| Sequential | Few tasks or strong coupling | Stay in `tasks.md` order |
| Parallel | Independent tasks with low coupling | [skills/superpowers-dispatching-parallel-agents/SKILL.md](skills/superpowers-dispatching-parallel-agents/SKILL.md) |
| Subagent | Many tasks, large context, or implement/review separation helps | [skills/superpowers-subagent-driven-development/SKILL.md](skills/superpowers-subagent-driven-development/SKILL.md) |

Default to sequential unless low coupling is clear.

### Per-Task Loop

```txt
Read task -> mark in_progress -> implement -> self-check
  bug or unexpected failure? -> systematic debugging
  pure logic or data transform? -> optional TDD
  design flaw discovered? -> stop Apply and update artifacts
mark done only with evidence
```

### Apply Gates

Read [references/quality-gates.md](references/quality-gates.md).

Non-negotiables:

- unclear task meaning -> ask instead of guessing
- design flaw -> return to Step 2 before more code
- 3 failed fix attempts -> stop thrashing and question the plan
- keep file ownership and style conventions consistent with the project

## Step 4: Review, Verify, Archive

Implementation finished is not the same as work finished.

### Review

1. Read [skills/superpowers-requesting-code-review/SKILL.md](skills/superpowers-requesting-code-review/SKILL.md).
2. Request review after a milestone or when all implementation tasks are done.
3. Read [skills/superpowers-receiving-code-review/SKILL.md](skills/superpowers-receiving-code-review/SKILL.md) before acting on feedback.
4. If review feedback changes requirements or design, roll back to Step 2.

### Verify

1. Re-read `proposal.md`.
2. Re-read `tasks.md`.
3. Run the verification commands.
4. Collect explicit evidence for correctness.

Read [skills/superpowers-verification-before-completion/SKILL.md](skills/superpowers-verification-before-completion/SKILL.md).

At minimum, verify:

- compilation or type checking passes
- the changed UI renders normally
- critical console errors are absent
- behavior matches the approved expectation
- edge cases, empty states, loading states, and error paths were considered

### Archive

After review and verification pass:

1. Read [skills/openspec-archive-change/SKILL.md](skills/openspec-archive-change/SKILL.md).
2. Archive the completed change or record closure in the project’s OpenSpec workflow.
3. Sync delta specs back to the main spec set when applicable.

## Rollback Matrix

| Current stage | Trigger | Roll back to |
| --- | --- | --- |
| Align | User adds substantial new constraints | Stay in Align |
| Propose | User overturns the agreed direction | Align |
| Apply | Design gap or bad task split discovered | Propose |
| Apply | Three failed fix attempts suggest the plan is wrong | Debugging first, then usually Propose |
| Review | Feedback implies requirement or design change | Propose |
| Verify | Verification fails but design still holds | Apply |
| Verify | Verification exposes a design flaw | Propose |

Rollback is correction, not failure.

## Definition Of Done

Only claim completion when all of these are true:

- interactive confirmation happened during Align
- the direction or artifact set was approved
- `proposal.md` covers scope and edge cases
- `design.md` explains structure, interfaces, and data flow
- `tasks.md` contains atomic tasks
- all tasks are marked complete
- review issues are resolved or explicitly dispositioned
- verification commands were run and passed
- UI, interaction, styles, and console state match expectation

## Anti-Patterns

Avoid these:

- treating OpenSpec and Superpowers as two parallel main workflows
- skipping Align because the task looks simple
- asking many questions in one message
- writing tasks before the approach is confirmed
- continuing to trust chat history after artifacts exist
- guessing fixes during failures
- continuing with a known design flaw
- calling work complete without proof

## Progressive Reading Map

```txt
Pure discussion -> skills/openspec-explore/SKILL.md
Pure bug fixing -> skills/superpowers-systematic-debugging/SKILL.md
Planned change ->
  Step 1 Align:
    references/brainstorming-guide.md
    skills/superpowers-brainstorming/SKILL.md
  Step 2 Propose:
    skills/openspec-propose/SKILL.md
    assets/templates/*.md
    references/spec-to-artifact-mapping.md
  Step 3 Apply:
    skills/openspec-apply-change/SKILL.md
    references/quality-gates.md
    skills/superpowers-systematic-debugging/SKILL.md
    skills/superpowers-test-driven-development/SKILL.md
    skills/superpowers-dispatching-parallel-agents/SKILL.md
    skills/superpowers-subagent-driven-development/SKILL.md
  Step 4 Close:
    skills/superpowers-requesting-code-review/SKILL.md
    skills/superpowers-receiving-code-review/SKILL.md
    skills/superpowers-verification-before-completion/SKILL.md
    skills/openspec-archive-change/SKILL.md
```

Examples:

- [references/examples/simple-change.md](references/examples/simple-change.md)
- [references/examples/complex-change.md](references/examples/complex-change.md)
