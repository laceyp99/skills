---
name: html-communication
description: >-
  Use when the user requests an HTML explanation or report, another skill invokes HTML report mode, or session instructions select HTML delivery.
  Trigger phrases include "turn this into a visual summary", "create a comparison page", and "make an internal report".
  Do not use for short answers, progress updates, or simple handoffs that read clearly in chat.
---

# HTML Communication

Produce a readable HTML explanation or report. The invoking skill defines its purpose and source of truth; preserve canonical plans and review records.

Keep the document clear, self-contained, and appropriate to the material. Choose the structure and visual treatment that best communicates the content; do not force every request into a fixed template.

Follow the user's requested delivery and session preferences. When inline delivery is selected and T3's `html_preview` and `html_render` are available, use them; otherwise deliver the portable file. This skill defines HTML mechanics, not a default medium for other skills. Video remains opt-in.

Use one self-contained document with inline CSS and only necessary vanilla JavaScript, without external runtime dependencies or network access. Choose one presentation by default; add variations only when requested. Share content between requested views instead of copying report bodies. Add controls only when they help the reader.

Save reports as portable UTF-8 files under repository-root `artifacts/reports/` with descriptive filenames. Brief inline illustrations need no file unless requested. Outside a repository, use the requested destination or a local artifacts directory.

Keep artifacts ignored and untracked; if needed, append `/artifacts/` to the local exclude file located by `git rev-parse --git-path info/exclude`. Before writing, check whether Git tracks the target; if unexpectedly tracked, warn the user and leave its tracking state unchanged. Never stage or commit reports automatically. Keep one HTML content value for the file and tool calls; regenerate it only to fix a problem. Keep file styling portable while honoring T3's inline layout guidance.

This is a communication artifact, not a coding plan artifact. If the user wants an executable project plan, implementation plan, or engineering handoff, use the `/blueprint` skill instead.

## Quiz Report Mode

When invoked by `/checkpoint-quiz`, add an interactive section using its supplied quiz contract and the host's placement and question sources. [Checkpoint Quiz](../checkpoint-quiz/SKILL.md) owns question count, types, answer semantics, and reflective behavior; read it only if that contract is not already in context.

Reveal the contract's feedback after selection, using accessible controls and a readable feedback region. Keep selections ephemeral within the page, with no persistence or transmission.

## Checks and delivery

- Default to one rendered inspection: use `html_preview` before `html_render` for T3 inline delivery, or an available browser for file-only delivery. Inspect the layout and available console errors at a width suited to the content. Exercise meaningful controls, including navigation and quiz feedback, when present. Small in-page assertions can check control logic; they do not establish keyboard usability.
- Add checks for complex interactions, explicit accessibility requirements, or observed problems. Use another viewport or preview for a concrete layout or state concern, and recheck behavior affected by a fix. Do not repeat successful checks without a specific coverage gap.
- Use required repository checks. Separate HTML parsing, encoding, and JavaScript syntax checks are not routine prerequisites when the rendered inspection already covers the relevant behavior; use them to diagnose failures or cover a named gap. Keep visual and interaction evidence distinct.
- Pass the same current HTML value to preview and render without printing the document between calls. Both tools require the full HTML input; reuse does not remove that transmission. Forward screenshots as images and summarize dimensions, console diagnostics, and check results. Do not stringify whole results containing encoded images. Do not assume undocumented path inputs, attachment handles, or screenshot-suppression options exist.
- The saved file and inline report use the same content; do not run a second validation cycle unless their behavior differs. Do not add a framework, dependency, app server, or general-purpose validation system for this workflow.

## Interaction and closeout

Inline HTML supports reader interaction through its JavaScript. Selections do not by themselves message the agent, record decisions, or authorize actions. Keep report selections ephemeral unless the user has requested a separate recording workflow.

The collaborative browser is a separate automation surface. Use its status, open, snapshot, and interaction tools according to current ownership rules when browser testing is needed. Do not assume an inline attachment has an automatable tab or shared state; verify access first. In-page assertions can check report control logic, but do not establish keyboard usability or replace a real browser journey when that behavior matters.

Follow the host's closeout format and link a local file when one was created. After inline delivery, keep chat to information the page does not already convey. Stop after delivery and applicable checks. If a failure cannot be resolved with a focused correction, or a check is unavailable, report the exact failure or verification gap without claiming validated output.
