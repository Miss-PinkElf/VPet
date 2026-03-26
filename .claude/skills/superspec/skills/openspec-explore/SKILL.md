---
name: openspec-explore
description: Use inside superspec when the user wants discussion, requirement exploration, idea comparison, or codebase investigation without implementation.
---

# OpenSpec Explore For SuperSpec

This is the discussion-only branch of SuperSpec.

## Use It When

- the user wants to think through options
- requirements are still fuzzy
- the user asked for exploration, tradeoff analysis, or investigation
- implementation should not start yet

## Stance

- explore, do not implement
- inspect code and documents freely
- ask questions that uncover constraints
- use diagrams or tables when they clarify the problem
- offer to capture conclusions into artifacts, but do not force it

## Output

Aim to leave the conversation with one of these:

- clearer requirements
- a comparison of approaches
- identified risks and unknowns
- a recommendation for whether to enter SuperSpec Align or Propose next

## Guardrails

- never write implementation code in this mode
- if the conversation hardens into an approved direction, hand off to `superspec` Step 1 or Step 2
- if the issue is actually a bug hunt, route to [../superpowers-systematic-debugging/SKILL.md](../superpowers-systematic-debugging/SKILL.md)
