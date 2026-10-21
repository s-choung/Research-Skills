
# sections (예전 paper-sections)

Fork of global `scientific-writing` skill, specialized to the author's voice via `references/style.md`. Absorbs former `paper-citation-format` skill as section 7 below.

## Dependencies
- Load `references/style.md` Mode 1 first. Use its output as hard constraint.

## Section playbooks

### Abstract / summary paragraph (Nature template, added 2026-10-21)
Source: Nature, "How to construct a Nature summary paragraph" (`~/Downloads/nature-summary-paragraph.pdf`).
Sentence budget, in this order:
1. 1-2 sentences: basic introduction to the field, readable by a scientist in any discipline.
2. 2-3 sentences: more detailed background, readable by scientists in related disciplines.
3. 1 sentence: the general problem this study addresses ("However, ... remains unknown").
4. 1 sentence: the main result, opened with "Here we show" or an equivalent.
5. 2-3 sentences: what the main result reveals compared with what was thought before, or how it adds to previous knowledge.
6. 1-2 sentences: the result in a more general context.
7. Optional 2-3 sentences: broader perspective. Total up to about 200 words, 300 with the optional part.
For a computational part inside an experimental paper, the computational contribution usually appears only in sentences 4-5.

### Whole-paper structure (Mensh & Kording 2017, PLoS Comput Biol 13:e1005619)
- One central contribution per paper; title, abstract, every Results subsection and the Discussion point at it (Rule 1).
- Context, content, conclusion at every scale: Introduction gives context, Results the content, Discussion the conclusion; inside a paragraph, the first sentence sets the question, the middle gives the data, the last sentence gives the answer (Rule 3, 7).
- Results subsection titles and figure titles are noun phrases that carry the conclusion (e.g., `Superior catalytic activity of exsolved Pt NPs`), not topic-only phrases (Rule 7).
- Discussion: first paragraph recaps the findings; following paragraphs each take one strength or weakness and link it to the literature; last paragraph says how the field moves forward (Rule 8).

### Introduction (target: 3-5 paragraphs)
1. **Topic paragraph** - field-level fact opener. Define acronyms parenthetically. Citation density 0.9-1.3 refs/sentence. See STYLE_EXEMPLARS G1.
2. **Gap/motivation paragraph** - quantitative gap statement, one subordinate clause. See STYLE_EXEMPLARS G2. Consider bridge B1 (Paradox-Pivot) or B3 (Enumerated-Walls) sparingly.
3. **Solution/approach paragraph** - solution announcement. See STYLE_EXEMPLARS G3.
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
2. Load STYLE_PROFILE via `references/style.md` Mode 1.
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
