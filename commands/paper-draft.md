---
description: Draft a specific IMRAD section or paragraph for a scientific manuscript in the author's voice. Dispatches paper-section-drafter subagent.
argument-hint: <section[:subsection]> [claim or data pointers]
allowed-tools: Read, Glob, Grep, Task
---

## Context

- Current working directory: !`pwd`
- Recent manuscript files: !`ls -lt Manuscript_*.docx Supporting_*.docx 2>/dev/null | head -5`
- Project context exists: !`test -f .claude/paper-team/project-context.md && echo yes || echo no`
- Style override exists: !`test -f .claude/paper-team/STYLE_PROFILE.override.md && echo yes || echo no`

## Task

User invoked: `/paper-draft $ARGUMENTS`

Parse `$ARGUMENTS` to extract:
1. `section` (required) - one of intro, methods, results, discussion, outlook. May have a subsection identifier like `results:exsolution_optimization`.
2. `claim_or_context` (optional, everything after the section token) - the claim to support, or pointer to data files.

Then:

1. Confirm the section exists in the current manuscript. If unclear, ask the user one clarifying question and STOP.
2. Identify relevant data files (generic patterns; override via project-context.md):
   - Results/Discussion: scan `output/*`, `archive/*figure*/raw_data.xlsx`, `Supporting_Information*.docx`
   - Introduction: scan the references library path from project-context.md (default `archive/06_references/`)
3. Dispatch the `paper-section-drafter` subagent via Task tool with:
   - section
   - subsection (if any)
   - claim (if given)
   - data_pointers (paths you identified)
4. Wait for the draft.
5. Return the draft to the user along with assumptions, gaps, and next suggested command.

Do NOT draft the paragraph yourself. You are a thin dispatcher.
