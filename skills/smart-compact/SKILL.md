---
name: smart-compact
description: |
  Save session state to .claude/session-state.md for recovery after /clear.
  Designed to be fast — required sections first, optional sections only when relevant.
  Trigger: /smart-compact
user-invocable: true
---

# Smart Compact

Save session state to file. User then runs `/clear` to reset.
The session-state.md is auto-read on next session start (via CLAUDE.md instruction).

## Instructions

When the user runs `/smart-compact`:

1. Write `.claude/session-state.md` in the **current working directory**
2. Tell the user it's done so they can `/clear`

**Speed principle**: This should take ~10 seconds, not minutes. Write dense, not verbose.

### Template

```markdown
# Session State
> /smart-compact at [date/time]

## Tone
[One line. e.g. "Korean casual + English tech terms, concise"]

## What We Did
[Numbered list of what happened this session, chronologically. Keep each item to 1-2 lines.
Include: what was requested → what was done → outcome]

## Key Decisions
[Bullet list of decisions + WHY. Quote user's exact words for preferences.]

## Files
| File | What Changed |
|------|-------------|
| path | one-line summary with key function/variable names |

## Current Status
- [x] Done tasks
- [ ] In-progress (note current state)
- [ ] TODO

## Bugs & Fixes
[Only if any. "Problem → cause → fix" format, one line each.]

## Code Notes
[Only for tricky/non-obvious code that would be hard to reconstruct.
Paste ONLY the critical snippets, not whole files. Skip if nothing tricky.]

## Tech Context
[Key paths, model names, config values, env details. Dense bullet list.]

## Next Steps
[Priority-ordered. What to do immediately after recovery.]
```

### Writing Guidelines
- **Dense, not verbose** — bullet points, not paragraphs
- Skip sections that are empty (except Tone, What We Did, Files, Current Status, Next Steps — always include these 5)
- Include specific names: variables, functions, paths, config values
- Quote user feedback verbatim when it matters
- For bugs: what didn't work is as important as what did
- Write for a new Claude that knows NOTHING about this conversation

## Post-Clear Recovery

Project CLAUDE.md auto-reads `.claude/session-state.md` on session start. No manual action needed.
