---
name: checkpoint-quiz
description: >-
  Use when a verification checkpoint is reached and the user's understanding should be confirmed or a decision captured as short multiple-choice questions.
  Trigger phrases include "quiz me", "test my understanding", and report-mode quiz sections.
  Do not use for open-ended decision exploration (grill-me).
---

# Checkpoint Quiz

Provide a short, focused quiz at a host skill's checkpoint so the user can self-grade their understanding of what happened, what was decided, and how it affects the system, and capture decisions at moments where one must be made. The quiz lives in the host's artifact, not in chat. Host skills own placement, question sourcing, and the artifact the quiz section is written into; this skill owns the mechanics.

## Question Types

- **Comprehension questions** test understanding of facts whose misunderstanding would change downstream behavior. They have correct answers.
- **Decision-capture questions** present real tradeoffs where the user's choice is what matters. They have no correct answer; never mark one. Try giving multiple choice options, if possible.

## Markdown Quiz Sections

Write the quiz as a section in the host's markdown artifact:

1. Ask 2-5 questions, one topic each.
2. Write each question with short lettered options (A/B/C/D) readable at a glance.
3. For comprehension questions, hide the correct answer and a one-to-two sentence explanation grounded in the host's source material inside a `<details><summary>Reveal answer</summary>` block.
4. For decision-capture questions, state what each selection implies instead of revealing an answer.
5. Keep questions answerable from the surrounding artifact without scrolling back through long prose.

The user self-grades: they answer first, then reveal. Never write answers inline, never score, and never enforce retakes.

## HTML Report Mode

When the host's deliverable is an HTML report, deliver the quiz as an interactive baked section via `/html-communication`'s quiz-report mode instead of a markdown section. The baked quiz is reflective only: it writes nothing, so confirm any meaningful selection with the user afterward and record it in the host's normal artifact. Report conclusions never depend on quiz results; the report is the assessment and the quiz verifies reader understanding.

## Recording

- Comprehension answers are self-graded and are not recorded anywhere.
- Decision-capture selections record into the artifact the host skill already owns; never create a new store. Confirm a selection with the user before writing it.