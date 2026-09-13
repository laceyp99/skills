# Writing Guide

Expanded guidance for skill prose: section-by-section before/after examples and the anti-pattern catalog. Read this when drafting or revising the actual wording of a skill.

## Description

The description is routing metadata. A reader sees it alongside every other skill's description and must pick correctly without reading the body.

**Before (catchall: routes everything, so nothing):**
> Helps with files, documents, code, data, automation, and various other tasks.

**After:**
> Create or edit Word documents when formatting, tracked changes, or comments require document-specific handling. Not for plain-text notes or PDFs.

**Before (capability list: the reader can't tell what matters):**
> Supports creating documents, converting formats, working with tracked changes, generating reports, managing templates, validating schemas, and more.

**After:**
> Convert PDF files to images and extract text. Use for one-off PDF transformations; for editing PDFs, use a PDF editor instead.

Rules:
- Lead with the action, then the condition that makes this skill the right one.
- Name the boundary, (the nearest skill or request type that should *not* route here) when confusion is likely.
- Keep it under ~3 sentences. Everything else belongs in the body.

## Opening Summary

**Before (restates the description and adds preamble):**
> This skill is about creating Word documents. Word documents are a common format. Below you will find guidance on many aspects of document creation.

**After:**
> Produce .docx output using python-docx. Prefer editing existing files over regenerating them.

The opening earns its place by stating the *stance* or the approach the skill takes that a generic agent would not assume.

## Body Instructions

**Before (lecture: true but behavior-neutral):**
> It is important to be careful when modifying configuration files. Configuration files can contain many important settings. Always think before editing.

**After:**
> Before editing a config file, read the whole file; settings are order-dependent in [this format]. Never reorder existing keys.

**Before (vague directive that doesn't decide anything):**
> Handle errors appropriately and ensure good quality output.

**After:**
> On HTTP 429, retry once after 30s, then surface the error to the user. Never retry 4xx errors other than 429.

Rules:
- Every sentence must change a decision: what to do, what not to do, when to stop, or where to look.
- Replace adjectives ("good", "appropriate", "robust") with concrete criteria.
- Prefer one example over a rule, and one rule over three paragraphs of explanation.

## Stop Conditions

Scale with autonomy. A single-file edit needs one line; an autonomous multi-step loop needs explicit bounds.

**Before (autonomous skill with no bounds):**
> Keep improving the code until it passes all tests.

**After:**
> Run the test suite at most 3 iterations. Stop when all tests pass. If failures persist after 3 iterations, report the failing tests and stop. Do not weaken assertions to force a pass.

**Before (retry loop, unbounded):**
> Retry the API call if it fails.

**After:**
> Retry up to twice with backoff. After the second failure, report the error and stop. Never retry mutations (POST/DELETE). Confirm with the user first.

As autonomy increases, stop conditions must state: the completion signal, the maximum effort/iteration bound, the failure behavior, and the point of return to the user.

## Anti-Pattern Catalog

Each entry: symptom → fix.

1. **Universal rule from one scar.** A skill mandates a step because one past task went wrong. → State the trigger condition, not the horror story: "when the repo uses pnpm, use `pnpm` commands" not "always check package managers because of that one failure."

2. **Restating the obvious.** Instructions the agent would follow anyway ("write clean code", "read the file first"). → Cut; spend the line on the non-obvious constraint.

3. **Description as table of contents.** Listing modes and features in the description. → Description routes; body instructs. One discriminating sentence pair.

4. **Boilerplate sections.** An "Overview" that says nothing, a "Notes" section of trivia, headers with one generic line under each. → Condense or delete; sections earn existence by containing decisions.

5. **Duplicated reference content in the body.** The body paraphrases what a reference says, so two copies drift. → Body carries the trigger line and the one-line takeaway; reference holds the detail.

6. **Unbounded autonomy.** Loops, retries, or multi-step chains without stop conditions proportional to risk. → Add completion signal, iteration cap, failure behavior, return-to-user point.

7. **Rigid steps for open-ended work.** Numbered procedure where multiple valid approaches exist. → State the outcome and decision criteria; fix steps only for fragile operations.

8. **Placeholder scaffolding shipped.** TODOs, example files, empty directories left in the final skill. → Delete or fill before finishing; run the validator.

9. **Over-prompting.** Triple-redundant warnings, restating principles multiple ways, explaining why the instruction matters after stating it. → One statement, one example if needed. Trust the reader.

10. **Tool pasteurization.** Forbidding or demanding specific tools where the environment's defaults are fine. → Constrain only when a real incompatibility or permission issue exists.

## Worked Examples

### Lean skill (single-mode, routine)

```text
commit-lint/
`-- SKILL.md        (~40 lines)
```

Body contains: when to apply, the convention, 2 before/after message examples, and one exclusion ("not for merge commits"). No scripts, no references. Adding a reference here would be structure for its own sake.

### Multi-mode skill

```text
doc-toolkit/
|-- SKILL.md                 (~50 lines: shared guidance + mode selection)
|-- references/
|   |-- redlining.md         (read when handling tracked changes)
|   `-- ooxml.md             (read when inspecting document internals)
`-- scripts/
    `-- unpack_docx.py       (deterministic OOXML extraction)
```

The body holds what every mode shares (file conventions, safety constraints) and one line per mode pointing to its reference. Reading only the relevant reference is the point; the body never duplicates them.
