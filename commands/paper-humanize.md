---
description: Light AI-ism cleanup on a paragraph or section. Strips a small scientific-safe blocklist only. Last pass before user review.
argument-hint: <target: paragraph text | para:N | section>
allowed-tools: Read, Edit, Grep
---

## Task

User invoked: `/paper-humanize $ARGUMENTS`

1. Parse `$ARGUMENTS`:
   - literal text: use as-is
   - `para:N`: locate the referenced paragraph in the current draft
   - `<section>`: locate the section in the current draft
2. Run `paper-style` skill Mode 2 (light humanize) directly on the target text. No subagent dispatch, no global humanizer, no full STYLE_PROFILE checklist.
3. Return the cleaned text and the change log in the Mode 2 output format.

Thin dispatcher only. Do not rewrite or add voice.
