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

Write the HTML file locally and report its path to the user. 

Validate it with:

```bash
python -c "import sys, html.parser; p = html.parser.HTMLParser(); p.feed(open(<filepath>).read())"
```

If validation fails, fix the markup and retry. Do not verify in a browser unless the user asks.
