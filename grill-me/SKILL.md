---
name: grill-me
description: Stress-test a plan, proposal, architecture, or technical design by interviewing the user one decision at a time. Use when the user asks to be grilled, wants a plan challenged, needs hidden assumptions exposed, wants design trade-offs walked branch by branch, or asks for relentless questioning before implementation.
---

# Grill Me

Use this skill to pressure-test a plan or design until the important decisions are explicit. Keep the interaction simple: ask one high-leverage question, give the recommended answer, wait for the user's response, then continue from the new state.

## Operating Rules

- Ask exactly one question at a time.
- Include your recommended answer with each question.
- Explain briefly why that answer is your recommendation and what decision it unlocks.
- Prefer concrete trade-offs over broad brainstorming.
- Do not edit source files, implement changes, create commits, or produce a full implementation plan. A local `decisions.md` artifact is permitted at closeout when the grilling result needs to persist and no `plan.md` exists.
- When the decision tree is resolved, apply the decisions to the next planning step instead of merely repeating them in chat.
- If an existing `plan.md` is in scope, identify the sections and tasks that the decisions change. Update the plan every time there is an agreement or a decision confidently made; respect its existing structure, task IDs, and unrelated content.
- If no `plan.md` exists and the grilling result will be used later, create a local `decisions.md` artifact containing only the resolved decisions, assumptions, open questions, risks, and recommended next step. Keep it untracked by default and do not turn it into an implementation plan.
- If the answer can be discovered from the codebase, inspect the codebase instead of asking the user.
- If the user has supplied a document, plan, issue, or design notes, use that artifact as the source of truth.

## Question Loop

1. Build a mental map of the decision tree: goal, users, constraints, data model, interfaces, risks, failure modes, rollout, tests, and maintenance burden.
2. Pick the unresolved question that most affects downstream choices.
3. Ask it in a narrow form so the user can answer directly.
4. Provide a recommended answer and a short reason.
5. After the user answers, update the decision tree and ask the next highest-leverage question.

Use this format by default:

```markdown
Question: {{one narrow decision question}}

Recommended answer: {{your recommendation}}

Why: {{short reasoning and trade-off}}
```

## What To Probe

Focus on decisions that would materially change implementation or product behavior:

- The exact problem being solved and what is out of scope.
- Which user or system gets priority when requirements conflict.
- Data ownership, validation boundaries, error handling, and permissions.
- Backward compatibility, migration needs, rollout order, and failure recovery.
- Test strategy, observability, operational burden, and future maintenance.
- Whether a simpler solution would satisfy the real requirement.

## Closeout

When the plan is clear enough to act on, stop grilling and summarize:

- Decisions confirmed.
- Assumptions still in play.
- Risks or unknowns that remain.
- The recommended next step.

If an existing `plan.md` is being updated, state which decisions were applied and which sections or task IDs were affected.

If no plan artifact exists, create `decisions.md` with this compact structure:

```markdown
# Grilling Decisions

> Status: Resolved | Needs follow-up
> Updated: YYYY-MM-DD

## Context

{{Short description of the problem or design being pressure-tested.}}

Confirmed decisions:
- {{decision}}

Assumptions:
- {{assumption}}

Open questions:
- {{question}}

Risks and checks:
- {{risk_or_check}}

Recommended next step:
- Use `/blueprint`, `/assembly`, or another explicitly named next skill.
```

If an existing `plan.md` or plan artifact exists and the user makes a decision that updates it, update only the sections affected by the grilling session. Preserve the artifact's existing structure, task IDs, and unrelated content.
