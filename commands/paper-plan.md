---
description: Build a multi-step plan for a paper writing or revision goal, using writing-plans skill. Returns a numbered plan with subagent assignments.
argument-hint: "<goal>"
allowed-tools: Read, Glob, Grep
---

## Context

- Current TODO file: !`test -f TODO.md && echo yes || echo no`
- Manuscript last modified: !`ls -l Manuscript_*.docx 2>/dev/null | head -1`
- SPEC: !`test -f .claude/paper-team/SPEC.md && echo yes || echo no`

## Task

User invoked: `/paper-plan $ARGUMENTS`

Treat `$ARGUMENTS` as the goal statement.

1. Load `~/.claude/skills/writing-plans/SKILL.md` and apply its planning methodology.
2. Decompose the goal into 3-7 numbered steps.
3. For each step, identify:
   - Which paper-team subagent or command executes it (`/paper-ref`, `/paper-draft`, `/paper-critic`, `/paper-humanize`, or manual user step)
   - Inputs required
   - Outputs produced
   - Blocking dependencies on other steps
4. Return the plan as:

```
## Goal
<restated>

## Plan
| # | Step | Executor | Inputs | Outputs | Depends on |
|---|------|----------|--------|---------|------------|
| 1 | ...  | /paper-ref | ... | ... | - |
| 2 | ...  | /paper-draft | ... | ... | 1 |

## First command to run
<exact command the user should invoke next>

## Assumptions
- <what you assumed about the goal>

## Ask user before continuing
- <any clarifying question>
```

This command does planning only. It does NOT execute steps.
