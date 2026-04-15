---
description: Humanize a paragraph or section to the author's voice. Two-pass (global humanizer + STYLE_PROFILE enforcement). Last pass before user review.
argument-hint: <target: paragraph text | para:N | section>
allowed-tools: Read, Edit, Grep, Task
---

## Context

- Global STYLE_PROFILE exists: !`test -f ~/.claude/paper-team/STYLE_PROFILE.md && echo yes || echo no`
- Project override exists: !`test -f .claude/paper-team/STYLE_PROFILE.override.md && echo yes || echo no`

## Task

User invoked: `/paper-humanize $ARGUMENTS`

1. Parse `$ARGUMENTS`:
   - literal text: use as-is
   - `para:N`: locate the referenced paragraph
   - `<section>`: locate the section
2. Dispatch the `paper-style-enforcer` subagent via Task with:
   - text = the target paragraph
   - mode = fix
3. The enforcer runs paper-humanize skill internally (pass 1: global humanizer, pass 2: style profile).
4. Return cleaned text + change log + residual risks + suggested next command (usually user review, or /paper-critic if content changed significantly).

Thin dispatcher only.
