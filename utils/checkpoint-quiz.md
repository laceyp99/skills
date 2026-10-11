# Checkpoint Quiz

Read when a host skill reaches its quiz checkpoint. This is an on-demand reference, not an invokable skill. Use `grill-me` for open-ended decision exploration.

Provide a short, focused quiz at a host skill's checkpoint so the user can self-grade their understanding of what happened, what was decided, and how it affects the system, and capture decisions at moments where one must be made. The quiz lives in the host's artifact, not in chat. Host skills own placement, question sourcing, and the artifact the quiz section is written into; this utility owns the mechanics.

## Quiz Contract

Ask 2-5 questions, one topic each, with short options. Keep them answerable from the surrounding artifact without scrolling back through long prose. The user self-grades; never score or enforce retakes. Quiz completion does not require answers in chat.

- **Comprehension questions** test understanding of facts whose misunderstanding would change downstream behavior. They have correct answers.
- **Decision-capture questions** present real tradeoffs where the user's choice is what matters. They have no correct answer; never mark one. Try giving multiple choice options, if possible.

Keep comprehension answers hidden until the user reveals them or selects an option; then show the correct answer and a one-to-two sentence explanation grounded in the host's source material. For decision-capture questions, show what each selection implies. Report quizzes are reflective; report conclusions never depend on quiz results.

## Markdown Quiz Sections

Write the quiz as a section in the host's markdown artifact:

Use short lettered options (A/B/C/D). Put comprehension feedback inside a `<details><summary>Reveal answer</summary>` block so the user can answer first, then reveal.

## HTML Report Mode

When the host's deliverable is an HTML report, pass this contract and the host's placement and question sources to [HTML Communication](../html-communication/SKILL.md) for an interactive baked section. Reuse skill guidance already in context. HTML selections are ephemeral and write nothing; any later decision recording follows the host's normal workflow and the Recording rules below, independently of quiz completion.

## Recording

- Comprehension answers are self-graded and are not recorded anywhere.
- Decision-capture selections record into the artifact the host skill already owns; never create a new store. Confirm a selection with the user before writing it.
