---
name: paper-style
description: Load the author's scientific writing style profile AND apply the 2-pass humanize protocol. Single skill for voice rules + enforcement. Use when drafting, reviewing, or humanizing any paragraph for a scientific manuscript. Triggers - paper style, 저자 문체, style profile, voice check, writing voice, academic voice, 논문 스타일, humanize, 논문 humanize, AI 흔적 제거, paper humanize, style cleanup, 문장 다듬기.
allowed-tools: Read, Edit, Grep
dependencies: humanizer
---

# paper-style

Merged skill for (1) loading the author's style profile and (2) applying style enforcement via a 2-pass humanize protocol. Replaces former paper-style-profile + paper-humanize.

Single source of truth: `~/.claude/paper-team/STYLE_PROFILE.md` (author-global).
Optional per-project override: `<cwd>/.claude/paper-team/STYLE_PROFILE.override.md`.
Optional per-project topic context: `<cwd>/.claude/paper-team/project-context.md`.

## Mode 1 - Load profile

For drafter agents that need style context before writing.

1. Read `~/.claude/paper-team/STYLE_PROFILE.md` in full.
2. If `<cwd>/.claude/paper-team/STYLE_PROFILE.override.md` exists, read and merge as deltas (override wins on conflict).
3. If `<cwd>/.claude/paper-team/project-context.md` exists, read for topic context (acronyms, key facts, references path).
4. Return to caller:
   - Section 3.1 banned words (verbatim)
   - Section 3.2 approved transitions (verbatim)
   - Section 2 quantitative dials (table)
   - Section 12 quick checklist
   - Pointers to section 4 openers, section 8 bridges, sections 9-10 exemplars and counter-examples

Do NOT paraphrase the rules. Copy them exactly. Drift is the main failure mode.

## Mode 2 - Humanize (2-pass)

For style enforcement after drafting. This is the LAST pass before user review.

### STEP 0 - Precondition check (fail loud)

Before any cleanup, verify both dependencies resolve:
1. `~/.claude/paper-team/STYLE_PROFILE.md` is readable.
2. `~/.claude/skills/humanizer/SKILL.md` is readable.

If either is missing, STOP and return:
```
ERROR: paper-style Mode 2 precondition failed.
Missing: <path>
Without STYLE_PROFILE loaded, humanize degrades to baseline AI cleanup,
which is already done well by the upstream humanizer alone. The author-voice
alignment IS the whole point.
```

### Pass 1 - Global humanizer
1. Load `~/.claude/skills/humanizer/SKILL.md` and apply its full ruleset to the input paragraph.
2. Record changes in a change log.

### Pass 2 - Author style enforcement
1. Run the paragraph against STYLE_PROFILE section 12 quick checklist:
   - Sentence > 30 words
   - More than 1 subordinate clause per sentence
   - Any hard-banned word (section 3.1)
   - `As shown in Fig.` / `as can be seen`
   - Rhetorical question
   - Hedge stack (>= 2 of may/might/could/possibly/potentially in one sentence)
   - First-person singular (I, my, me)
   - Italicized essayistic connector (And yet, In that sense, ...)
   - Affect verb (surprised, discomfort, believe, care)
   - Acronym used without parenthetical first definition within paragraph
   - Figure as grammatical subject more than twice in the paragraph
   - `In recent years` / `With the rapid development of` opener
   - Paragraph ending in rhetorical mic-drop
2. For each flagged issue, apply a minimal edit. Prefer deletion over rewording when a banned word appears.
3. Verify sentence length dial (16-22 word mean, 30 word cap).
4. Preserve all numerical claims, citations, and technical content. Do not paraphrase findings.

## Output formats

### Mode 1 output
```
## Banned (hard)
<list>

## Approved transitions
<list>

## Dials
<table>

## Checklist (paper-style-enforcer)
<checklist>
```

### Mode 2 output
```
## Cleaned text
<final paragraph>

## Pass 1 changes (humanizer)
- <change 1>
- <change 2>

## Pass 2 changes (style profile)
- <change 1>
- <change 2>

## Residual risks
- <anything unchanged that is still borderline>
```

## Hard rules
- Never change technical claims, numbers, or citation markers.
- If the paragraph is already compliant in Mode 2, return verbatim with `NO_CHANGES`.
- If more than 30% of the paragraph would need rewriting, FLAG for human review instead of rewriting.
- If the caller is working on a non-author manuscript, flag it in Mode 1 and offer to skip.
- If STYLE_PROFILE.md is missing, fail loud with the expected path.
