---
name: html-communication
description: Create readable local HTML communication artifacts when the user asks for internal reports, comparisons, summaries, and insights. Do not use for planning features, patches, or refactors; use /blueprint for that.
---

# HTML Communication

Use this skill when the requested deliverable is a visual, readable HTML document for internal communication. Such as a report, comparison, summary, or insight brief.

Keep the document clear, self-contained, and appropriate to the material. Choose the structure and visual treatment that best communicates the content; do not force every request into a fixed template.

This is a communication artifact, not a coding plan artifact. If the user wants an executable project plan, implementation plan, or engineering handoff, use the `/blueprint` skill instead.

Write the HTML file locally and report its path to the user. 

Validate it with:

```bash
python -c "import sys, html.parser; p = html.parser.HTMLParser(); p.feed(open(<filepath>).read())"
```

If validation fails, fix the markup and retry. Do not verify in a browser unless the user asks.
