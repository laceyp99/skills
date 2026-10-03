---
name: checkpoint-quiz
description: >-
  Use when a verification checkpoint is reached and the user's understanding should be confirmed or a decision captured as short multiple-choice questions.
  Trigger phrases include "quiz me", "test my understanding", and report-mode quiz sections.
  Do not use for open-ended decision exploration (grill-me).
---

# Checkpoint Quiz

Run a short, focused interview at a host skill's checkpoint: confirm the user's understanding of what happened, what was decided, and how it affects the system, and capture decisions at moments where one must be made. Treat it as a spot-check, not a toll booth.

Host skills own placement and question sourcing. This skill owns the mechanics.

## Question Types

- **Comprehension questions** test understanding of facts whose misunderstanding would change downstream behavior. They have correct answers.
- **Decision-capture questions** present real tradeoffs where the user's choice is what matters. They have no correct answer; never mark one. Try giving multiple choice options, if possible.

## Delivery

1. Ask 2-5 questions, one topic each, in a single group.
2. Use the harness's ask-question tool with multiple-choice options when available.
3. If that tool is unavailable, ask inline with lettered options (A/B/C/D) in markdown text. Keep the format identical to the tool version.
4. Keep options short enough to read at a glance, and questions answerable from what was just presented without scrolling back through long prose.

## Comprehension Failure Path

1. On a wrong answer, immediately reveal the correct answer with a one-to-two sentence explanation grounded in the host's source material.
2. Ask one fresh question on the same topic. Never re-ask the same question.
3. On a second miss, flag the gap in one line and ask whether to re-explain that section or proceed anyway.
4. Never silently pass a missed topic, and never hard-block beyond two attempts.

## Waivers

A checkpoint is mandatory by default but always waivable by one explicit request ("skip", "I already read this", "move on"). Acknowledge in one line and proceed. Never nag, never re-offer more than once, and never maintain a persistent opt-out.

## Recording

- Comprehension answers are ephemeral. Do not persist them.
- Decision-capture selections record into the artifact the host skill already owns; never create a new store. Confirm a selection in chat before writing it.

## Report Mode

When the host skill's report mode is active, deliver the interview as the report's baked quiz instead of chat questions. Invoke `/html-communication` with its quiz-report mode. The baked quiz is reflective only: it shows what each selection implies but writes nothing, so confirm any meaningful selection in chat afterward and record it in the host's normal artifact. Report conclusions never depend on quiz results; the report is the assessment and the quiz verifies reader understanding.