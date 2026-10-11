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

Produce one portable, self-contained UTF-8 HTML file with inline CSS and only necessary vanilla JavaScript. The whole report must work without external runtime dependencies or network access. Add controls only when they help the reader; preserve the host's requested variations and their count.

This is a communication artifact, not a coding plan artifact. If the user wants an executable project plan, implementation plan, or engineering handoff, use the `/blueprint` skill instead.

## Quiz Report Mode

When the host requests a checkpoint quiz, add an interactive section using its supplied quiz contract and the host's placement and question sources. [checkpoint quiz utility](../utils/checkpoint-quiz.md) owns question count, types, answer semantics, and reflective behavior; read it only if that contract is not already in context.

Reveal the contract's feedback after selection, using accessible controls and a readable feedback region. Keep selections ephemeral within the page, with no persistence or transmission.

## Checks and Delivery

- Use existing repository checks where applicable. Otherwise use an explicit available interpreter and read the file as UTF-8. `HTMLParser.feed()` is only a parsing check; it does not establish valid markup, usable layout, or working JavaScript. Check JavaScript syntax separately when scripts are present.
- Inspect the rendered layout and console output, and exercise meaningful controls, including quiz feedback. Check a narrow layout when wrapping, navigation, or controls could affect usability. Keep parsing, JavaScript syntax, visual inspection, and interaction results distinct.
- When T3's `html_preview` and `html_render` are available, follow their current tool guidance. Keep one HTML content value for the local file and both calls; do not regenerate it or print it between calls. Preview before rendering, inspect the screenshot and console output, and verify controls with available browser tools or in-page checks. Fix observed problems and recheck affected behavior before `html_render`. Keep local-file styling portable while honoring T3's inline layout guidance.
- Without T3 inline delivery, deliver the local file and use an available browser for visual and interaction checks. Do not add a framework, dependency, app server, or general-purpose validation system for this workflow.

Follow the host skill's closeout format and retain a link to the local artifact. T3 rendering is inline delivery, not a replacement for the portable file. Stop after delivery and applicable checks; if a check fails or is unavailable, report the exact failure or verification gap without claiming validated output.
