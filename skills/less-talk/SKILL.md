---
name: less-talk
description: Cut what Claude says and what Claude puts on a page to the minimum the reader needs to decide. Use when the user says less talk, 말 줄여, too much talker, 짧게, 인지부하, 요약만, 결론만, simple 버전, or when a reply, report, figure or caption is about to run long. Applies to chat replies, HTML reports, figure labels, legends and captions.
---

# less-talk

The reader wants to decide, not to watch me think. Every sentence, label and legend entry costs attention.
Default is silence: a thing stays only if removing it would change what the reader does next.

## Chat replies

- Lead with the outcome in one sentence. Numbers that drive a decision go in a table or one line each.
- No narration of process ("I checked", "then I ran"). No restating the request. No closing offer.
- No hedges, no self-assessment, no "note that". If unverified, say "unverified" once.
- One bullet per finding, one line per bullet. Max 5 bullets. Prose only for a single argument.
- Progress reports: one status line per running job (what, where, ETA). Nothing else.
- When asked a question: answer, then stop. Background goes only if the answer is wrong without it.
- Target length: a third of what I would write by default. If over 120 words, cut again.

## Reports and pages

- One headline sentence per section that states the decision. Evidence under it in at most 3 bullets.
- Everything that justifies but does not change the decision goes into a collapsed `<details>` block.
- Methods, parameters, cost, file paths: one collapsed block for the whole document.
- A number appears once. Summary, section and Limits do not repeat it.
- Tables: keep only the one the reader scans to decide. Convert the rest to a figure or collapse them.
- No figure toggles. Show the one default variant; put the others in a heatmap or in a collapsed block.

## Figures

- One message per figure, stated in the caption's first sentence. If two messages, two figures or a collapse.
- Text elements (title, axis labels, ticks, legend entries, annotations): cut to half of the first draft.
- Set and model names are short codes (`champion`, `cond+steric9`, GP, ET). The code-to-name table lives once, collapsed.
- Legends below the axes, never inside the data area. Axis titles at most 4 words plus a unit.
- Annotate values only where the value is the decision. Drop parenthetical secondary numbers.
- Show the full data set or say the cut rule in the caption ("top 8 by new-ligand rho"); do not silently subset.
- After building, run a browser overlap scan and a visual check; matplotlib's own audit is not enough.

## Self-check before sending

1. Delete the first paragraph if it is not the answer.
2. Delete every sentence that explains why I did something.
3. Merge bullets that share a subject.
4. Replace any three-item list of adjectives with the one that matters.
5. If the reply still explains the reasoning, move it into one line marked "why:".
