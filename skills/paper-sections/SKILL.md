---
name: paper-sections
description: Draft IMRAD paper sections (Introduction, Methods, Results, Discussion, Outlook) in the author's voice, using STYLE_PROFILE.md templates. Includes numeric-superscript citation format rules. Forked from scientific-writing. Use when writing or revising a specific section of a scientific manuscript, or when inserting citations. Triggers - paper draft, IMRAD, introduction draft, results 작성, discussion 섹션, 섹션 초안, manuscript section, citation format, 인용 포맷, bibliography, reference format, in-text cite, superscript citation.
allowed-tools: Read, Grep, Glob, Write, Edit
dependencies: paper-style
---

# paper-sections

Fork of global `scientific-writing` skill, specialized to the author's voice via `paper-style`. Absorbs former `paper-citation-format` skill as section 7 below.

## Dependencies
- Load `paper-style` Mode 1 first. Use its output as hard constraint.

## Section playbooks

### Introduction (target: 3-5 paragraphs)
1. **Topic paragraph** - field-level fact opener. Define acronyms parenthetically. Citation density 0.9-1.3 refs/sentence. See STYLE_PROFILE G1.
2. **Gap/motivation paragraph** - quantitative gap statement, one subordinate clause. See STYLE_PROFILE G2. Consider bridge B1 (Paradox-Pivot) or B3 (Enumerated-Walls) sparingly.
3. **Solution/approach paragraph** - solution announcement. See STYLE_PROFILE G3.
4. **Summary of contributions** - `In this work, we ...` with numbered contributions.

### Methods (passive, purpose-forward)
- Every sentence passive. Zero first person.
- Order: materials -> synthesis -> characterization -> computational -> kinetic.
- Parameters in parentheses, not footnotes.

### Results (passive + purpose opener)
- Each subsection opens with purpose sentence (see STYLE_PROFILE 4.2).
- Figures referenced parenthetically `(Fig. 2a)`. NEVER `As shown in Fig.`.
- One finding per paragraph. Close with mechanistic consequence.

### Discussion (mixed voice, active for claims)
- Open with contribution statement + retrace (see G5).
- `we` permitted for active mechanistic claims.
- Citation density drops to 0.2-0.4 refs/sentence.
- Consider bridge B3/B4 for multi-limitation synthesis, B5 for close.

### Outlook / Conclusion
- Start with `In summary, ...` or `By bridging ...` (see STYLE_PROFILE 4.4).
- No hedging adverbs. No rhetorical close.

## 7. Citation format (absorbed from paper-citation-format)

### Default style
Numeric superscript, following Nature Commun / ACS Catal convention.

- Single: `text^1`
- Range: `text^1-4`
- List: `text^1,3,5`
- Mixed: `text^1-3,7`

No space between word and superscript. Superscripts attach to the concept, not the sentence terminator. Attach before punctuation when the cite scopes the clause, after punctuation when it scopes the sentence.

### In-text cite rules (author voice via STYLE_PROFILE)
- Intro: ~1 cite per sentence. Clusters of `^1-4` acceptable.
- Discussion: cite only for specific comparative claims or contradictions to prior art. Mechanistic own-work statements stay uncited.
- Never cite a review when a primary source exists for the specific claim.
- Novelty claim requires contrast cite: `Unlike previous work that ...^12, here we ...`.

### Bibliography entry format

When target journal unknown, emit EndNote-style block:
```
[N] Author, A. B.; Author, C. D. Title. Journal Year, Vol, Pages. DOI.
```

If journal known:
- Nature Commun: `Author, A. B. et al. Title. Journal Vol, Pages (Year).`
- ACS: `Author, A. B.; Author, C. D. Title. Journal Year, Vol, Pages.`

### Citation hard rules
- Never fabricate DOI, year, or author list.
- If any required metadata is missing, return FLAG with the missing field name. Do not guess.
- `et al.` only when author count > 3 in short form journals.

## Workflow when invoked

1. Receive args: `section_name`, optional `subsection_identifier`, optional `existing_text`, optional `data_pointers`.
2. Load STYLE_PROFILE via `paper-style` Mode 1.
3. Gather minimal context: read only the referenced data files. Do not load the whole manuscript.
4. Draft paragraph(s) following the section playbook above.
5. When inserting citations, use the format in section 7 above.
6. Self-check against STYLE_PROFILE section 12 quick checklist before returning.
7. Return: draft text + list of gaps/assumptions + suggested next command.

## Hard rules
- No banned word (STYLE_PROFILE 3.1) may appear.
- Sentence length: 16-22 words mean, 30 word max.
- One subordinate clause per sentence max.
- Active/passive ratio matches section norm.
