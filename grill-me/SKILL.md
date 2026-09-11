---
name: grill-me
description: >-
  Use when the user asks to solidify a plan, architecture, or technical design through one decision at a time. 
  Trigger phrases include "grill me", "narrow this down", and "help me think this through".
  Do not use for directly creating or executing a plan, investigating a bug, or implementing the decided changes.
---

# Grill Me

Use this skill to pressure-test a plan or design until the important decisions are explicit. Keep the interaction simple: ask one high-leverage question, give the recommended answer, wait for the user's response, then continue from the new state.

## Determine Mode

Use the user's current request to choose the mode.

- **Normal mode**: Use by default, and whenever the user has not asked for batching. Ask one high-leverage question at a time and wait for each answer.
- **Batch mode**: Use only when the user explicitly asks for "batching", "grouped questions", or "several questions at a time", in whatever phrasing they use. Group 2-5 related questions per round by topic; the grouping does not need to be uniform.

## Operating Rules

- In normal mode, ask exactly one question at a time. In batch mode, ask one batch 2-5 questions at a time.
- Include your recommended answer with each question.
- Explain briefly why that answer is your recommendation and what decision it unlocks.
- Prefer concrete trade-offs over broad brainstorming.
- Do not edit source files, implement changes, create commits, or produce a full implementation plan. A local `decisions.md` artifact is permitted at closeout when the grilling result needs to persist and no `plan.md` exists.
- When the decision tree is resolved, apply the decisions to the next planning step instead of merely repeating them in chat.
- If an existing `plan.md` is in scope, identify the sections and tasks that the decisions change. Update the plan every time there is an agreement or a decision confidently made; respect its existing structure, task IDs, and unrelated content.
- If no `plan.md` exists and the grilling result will be used later, create a local `decisions.md` artifact containing only the resolved decisions, assumptions, open questions, risks, and recommended next step. Keep it untracked by default and do not turn it into an implementation plan.
- Before writing `plan.md`, `decisions.md`, or another planning artifact, check whether Git already tracks it. Leave untracked artifacts untracked; if one is tracked unexpectedly, warn the user and do not change its tracking state. Never stage or commit these artifacts.
- If the answer can be discovered from the codebase, inspect the codebase instead of asking the user.
- If the user has supplied a document, plan, issue, or design notes, use that artifact as the source of truth.

## Response Format

Use this format for every question in both modes. The italicized recap line is omitted when there is nothing to confirm.

```markdown
_Any confirmation or recap of the decisions from the questions before._
## Current Question
Here is where you should put the question within plain text.

**Suggested answer:**
> This is where you should put the suggested answer to your proposed question.

**Why:** Here is the reasoning behind the suggested answer.
```

In batch mode, repeat the format block for each question under numbered headings (`## Question 1 of 4`, `## Question 2 of 4`, and so on). Give each question its own suggested answer, and note briefly if two suggested answers in the same batch conflict.

Each question in a batch must be independently answerable with no dependencies on other questions in the same batch. A question that hinges on an earlier answer may be included only as a self-contained conditional, such as "if X is chosen, should Y? If not, then does that mean Z?" 

## Question Loop

1. Build a mental map of the decision tree: goal, users, constraints, data model, interfaces, risks, failure modes, rollout, tests, and maintenance burden.
2. Pick the unresolved question that most affects downstream choices.
3. Ask it in a narrow form so the user can answer directly.
4. Provide a recommended answer and a short reason.
5. After the user answers, update the decision tree and ask the next highest-leverage question.

In batch mode, after the user answers a round, present the next batch first with the numbered question headings, then open with a single italicized recap line of the decisions just confirmed. Omit the recap if nothing was confirmed.

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
