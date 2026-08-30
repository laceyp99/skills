# Subagent Delegation

Use subagents to keep focused investigation or implementation context out of the primary conversation, not simply to maximize parallelism. The primary agent remains responsible for synthesis, integration, lifecycle decisions, and communication with the user.

Use configured roles by capability:
- `explorer` for read-only investigation
- `worker` for bounded implementation.

Give each delegated task:
- one clear responsibility
- only the context it needs
- the expected evidence or output
- its ownership and mutation boundaries
- a stopping condition

Prefer sequential delegation for context management. Use concurrent work only when tasks are genuinely independent and have disjoint ownership. If the suitable role is unavailable, continue directly when practical and report the limitation when it prevents safe completion.
