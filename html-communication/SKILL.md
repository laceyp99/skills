---
name: html-communication
description: >-
  Prefer T3 inline HTML for substantive reports and visual explanations, or use when the user requests a local HTML artifact or another skill invokes HTML report mode.
  Trigger phrases include "turn this into a visual summary", "create a comparison page", and "make an internal report".
  Do not use for short answers, progress updates, or simple handoffs that read clearly in chat.
---

# HTML Communication

Produce a readable HTML explanation or report. The invoking skill defines its purpose and source of truth; preserve canonical plans and review records.

Keep the document clear, self-contained, and appropriate to the material. Choose the structure and visual treatment that best communicates the content; do not force every request into a fixed template.

Prefer T3 inline delivery when `html_preview` and `html_render` are available. Honor explicit output requests. Without inline delivery, use plain chat unless a local HTML artifact is requested or required by the host. Video remains opt-in.

Use one self-contained document with inline CSS and only necessary vanilla JavaScript, without external runtime dependencies or network access. Choose one presentation by default; add variations only when requested. Share content between requested views instead of copying report bodies. Add controls only when they help the reader.

Save a portable UTF-8 file for substantive reports, explicit file requests, or host requirements. A brief inline visual explanation need not create a second artifact. Keep one HTML content value for the file, when needed, and tool calls; regenerate it only to fix a problem. Keep file styling portable while honoring T3's inline layout guidance.

This is a communication artifact, not a coding plan artifact. If the user wants an executable project plan, implementation plan, or engineering handoff, use the `/blueprint` skill instead.

## Quiz Report Mode

When invoked by `/checkpoint-quiz`, add an interactive section using its supplied quiz contract and the host's placement and question sources. [Checkpoint Quiz](../checkpoint-quiz/SKILL.md) owns question count, types, answer semantics, and reflective behavior; read it only if that contract is not already in context.

Reveal the contract's feedback after selection, using accessible controls and a readable feedback region. Keep selections ephemeral within the page, with no persistence or transmission.

## Checks and delivery

- Use existing repository checks where applicable. Check a saved file's UTF-8 encoding and check JavaScript syntax once when scripts are present. A separate `HTMLParser.feed()` pass is optional and establishes parsing only, not valid markup, usable layout, or working controls.
- Default to one `html_preview` before `html_render`, following current tool guidance. Choose a width that covers the main layout risk, including narrow wrapping or navigation when relevant. Inspect its screenshot and console output. Exercise meaningful controls, including quiz feedback, through available browser tools or small in-page assertions that emit compact console results in that preview. Keep syntax, visual, and interaction evidence distinct.
- Add a preview only to check an observed fix or a named coverage gap, such as a materially different layout, hidden view, keyboard behavior, or control state. Recheck behavior affected by an edit before delivery. One preview is a default, not permission to skip a needed check. Stop when applicable checks pass; do not repeat successful checks for cosmetic reassurance.
- Pass the same current HTML value to preview and render without printing the document between calls. Both tools require the full HTML input; reuse does not remove that transmission. Forward screenshots as images and summarize dimensions, console diagnostics, and check results. Do not stringify whole results containing encoded images. Do not assume undocumented path inputs, attachment handles, or screenshot-suppression options exist.
- Without T3 inline delivery, validate a requested local file with an available browser. Do not add a framework, dependency, app server, or general-purpose validation system for this workflow.

## Interaction and closeout

Inline HTML supports reader interaction through its JavaScript. Selections do not by themselves message the agent, record decisions, or authorize actions. Keep report selections ephemeral unless the user has requested a separate recording workflow.

The collaborative browser is a separate automation surface. Use its status, open, snapshot, and interaction tools according to current ownership rules when browser testing is needed. Do not assume an inline attachment has an automatable tab or shared state; verify access first. In-page assertions can check report control logic, but do not establish keyboard usability or replace a real browser journey when that behavior matters.

Follow the host's closeout format and link a local file when one was created. After inline delivery, keep chat to information the page does not already convey. Stop after delivery and applicable checks. If a failure cannot be resolved with a focused correction, or a check is unavailable, report the exact failure or verification gap without claiming validated output.
