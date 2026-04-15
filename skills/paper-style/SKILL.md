---
name: paper-style
description: Load the author's scientific writing style profile, or do a light AI-ism cleanup on a paragraph. Use when drafting, reviewing, or humanizing any paragraph for a scientific manuscript. Triggers - paper style, 저자 문체, style profile, 논문 스타일, humanize, 논문 humanize, AI 흔적 제거, paper humanize.
allowed-tools: Read, Edit, Grep
---

# paper-style

Two modes: **(1) load profile** for drafters, **(2) light humanize** for a last-pass AI-ism scrub.

Source: `~/.claude/paper-team/STYLE_PROFILE.md` (author-global).
Optional per-project override: `<cwd>/.claude/paper-team/STYLE_PROFILE.override.md`.

## Mode 1. Load profile

Called by drafter agents before writing.

1. Read `~/.claude/paper-team/STYLE_PROFILE.md`.
2. If override exists in cwd, read and merge (override wins on conflict).
3. Return section 3.1 banned words, section 3.2 approved transitions, section 2 dials, section 12 checklist. Verbatim, no paraphrase.

## Mode 2. Light humanize

Called by `/paper-humanize`. This is a **light** pass. Do NOT rewrite, do NOT inject voice, do NOT enforce the full STYLE_PROFILE checklist (that is the drafter's job). Only strip the AI-isms below.

### Strip list (scientific-safe)

- **AI vocab**: `delve into`, `leverage`, `intricate`, `underscores`, `nuanced`, `tapestry`, `realm`, `in the realm of`, `it is worth noting`, `it should be noted`, `plays a crucial role`, `stands as a testament`, `navigating the complexities`, `comprehensive understanding`, `shed light on`, `pave the way`.
- **Em dash overuse** (Unicode U+2014): replace with comma, period, or parenthesis. Keep at most one per paragraph.
- **Rule of three**: triple parallel constructions where all three items are near-synonyms. Cut to one.
- **"As shown in Fig. X"** and **"as can be seen"** as sentence opener: move the figure reference into a parenthetical `(Fig. X)`.
- **Rhetorical questions** and **mic-drop paragraph endings**.

### Hard rules

- Never change numbers, citation markers, chemical formulas, or any technical claim.
- If a word on the strip list is load-bearing for the claim, leave it and flag.
- If more than 30% of the paragraph would need editing, STOP and return `ESCALATE`.
- If the paragraph is already clean, return it verbatim with `NO_CHANGES`.

### Output

```
## Cleaned text
<paragraph>

## Changes
- <one line per edit>
```
