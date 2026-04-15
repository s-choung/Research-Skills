---
description: Hunt candidate references in the current project's references library (and optionally the web) for a given topic or claim. Dispatches paper-ref-hunter subagent.
argument-hint: "<topic or claim>"
allowed-tools: Read, Glob, Grep, Task
---

## Context

- Project context exists: !`test -f .claude/paper-team/project-context.md && echo yes || echo no`
- Default library (archive/06_references/): !`ls -1 archive/06_references/ 2>/dev/null | head -20`
- Library file count: !`find archive/06_references -type f 2>/dev/null | wc -l`

## Task

User invoked: `/paper-ref $ARGUMENTS`

Treat `$ARGUMENTS` as the query (topic keyword or claim statement).

1. Dispatch `paper-ref-hunter` subagent via Task with:
   - query = $ARGUMENTS
   - exclude_list (if the user mentioned exclusions; otherwise empty)
2. Return the ranked candidate table (library + web if needed) + coverage gaps + suggested next command.

Thin dispatcher only. Do not scan the library yourself.
