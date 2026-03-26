# Brainstorming Guide

Use this guide during SuperSpec Align.

## Mode Selection

Choose full Align when:

- requirements are ambiguous
- multiple implementation strategies are viable
- more than one page, module, or workflow is affected

Choose Mini Align only when:

- the change is small
- the expected outcome is already specific
- architecture and API boundaries are not meaningfully changing

## Question Rules

- ask one question at a time
- prefer 2-4 options when the decision space is known
- ask for constraints, success criteria, and non-goals before implementation detail
- do not stack multiple unrelated questions in a single turn

## Approach Comparison Template

```md
## Option A - Recommended
- Why it fits
- Main tradeoff
- Main risk

## Option B
- Why it fits
- Why it is not the current recommendation

## Option C
- Only include if it is materially different
```

## Approval Summary Template

Use a short summary that can be copied into proposal artifacts:

```md
## Confirmed Direction
- Goal:
- In scope:
- Out of scope:
- Main implementation direction:
- Risks to watch:
- Open questions that remain:
```

## Exit Condition

Do not move to Propose until the user has explicitly confirmed the direction summary.
