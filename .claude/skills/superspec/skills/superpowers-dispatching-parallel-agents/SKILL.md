---
name: superpowers-dispatching-parallel-agents
description: Use inside superspec when tasks in tasks.md are clearly independent and can be implemented or investigated concurrently without shared state.
---

# Superpowers Parallel Agents For SuperSpec

Parallelism is useful only when task boundaries are real.

## Use It When

- two or more tasks are independent
- tasks do not edit the same files or rely on the same transient state
- the integration order is clear

## Steps

1. Partition `tasks.md` into independent domains.
2. Give each agent one focused task, its acceptance criteria, and explicit boundaries.
3. Keep shared files or interfaces owned by one coordinating agent.
4. Review returned changes for conflicts.
5. Run integrated verification after merging the outputs.

## Do Not Use It When

- tasks are tightly coupled
- the work requires a single evolving design context
- agents would likely edit the same files at once
