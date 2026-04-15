---
description: Scientifically critique a paragraph, section, or claim in the current scientific manuscript for rigor and claim-evidence alignment. Dispatches paper-scientific-critic subagent.
argument-hint: <target: section name | para:N | paragraph text>
allowed-tools: Read, Glob, Grep, Task
---

## Context

- Current working directory: !`pwd`
- Manuscript: !`ls -1 Manuscript_*.docx 2>/dev/null | head -1`
- SI: !`ls -1 Supporting_Information*.docx 2>/dev/null | head -1`

## Task

User invoked: `/paper-critic $ARGUMENTS`

Parse `$ARGUMENTS`:
1. If it looks like a section name (`intro`, `methods`, `results`, `discussion`), target that section.
2. If it starts with `para:`, target the specified paragraph.
3. If it is free text, target it as a literal paragraph.

Then:

1. Identify the data the claim should be grounded in (svg output files, raw_data.xlsx, SI tables).
2. Collect any refs cited inside the target text.
3. Dispatch the `paper-scientific-critic` subagent via Task with:
   - target text
   - data_pointers
   - related_refs
4. Return the structured issue table (Blockers / Major / Minor) to the user + suggested next action.

Do NOT perform the critique yourself. Thin dispatcher only.
