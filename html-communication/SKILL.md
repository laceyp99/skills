---
name: html-communication
description: >-
  Use when the user asks for a readable local HTML communication artifact, or another skill explicitly invokes an HTML report mode.
  Trigger phrases include "turn this into a visual summary", "create a comparison page", and "make an internal report".
  Do not use for ordinary prose that does not need an HTML artifact.
---

# HTML Communication

Use this skill when the requested deliverable is a visual, readable HTML document for internal communication, including a report mode invoked by another skill. The invoking skill defines the report's purpose and source of truth.

Keep the document clear, self-contained, and appropriate to the material. Choose the structure and visual treatment that best communicates the content; do not force every request into a fixed template.

This is a communication artifact, not a coding plan artifact. If the user wants an executable project plan, implementation plan, or engineering handoff, use the `/blueprint` skill instead.

## Quiz Report Mode

When invoked by `/checkpoint-quiz` on behalf of a host skill's report checkpoint, add one interactive quiz section to the report alongside the normal content. Source the questions from the host skill's checkpoint placement.

- Keep the script vanilla JavaScript inline in the single self-contained file, with no network access and no external dependencies.
- Ask 2-5 questions, one topic each, with short options.
- Comprehension questions reveal the correct answer with a one-to-two sentence explanation after each selection.
- Decision-capture questions show what each selection implies and never mark a correct answer.
- The quiz is reflective: nothing is written, persisted, or sent anywhere, and the report's conclusions never depend on quiz results.

Write the HTML file locally and report its path to the user. 

Validate it with:

```bash
python -c "import sys, html.parser; p = html.parser.HTMLParser(); p.feed(open(<filepath>).read())"
```

If validation fails, fix the markup and retry. Do not verify in a browser unless the user asks.
