
# style (예전 paper-style)

Three modes. **(1) load profile** for drafters, **(2) tighten** for the author's
hard rules on an existing paragraph, **(3) light humanize** for a last-pass
AI-ism scrub.

Source: `~/.claude/paper-team/STYLE_PROFILE.md` (rules only, author-global).
Exemplars: `~/.claude/paper-team/STYLE_EXEMPLARS.md` (drafters only).
Optional per-project override: `<cwd>/.claude/paper-team/STYLE_PROFILE.override.md`.

## Mode 1. Load profile

Called by drafter agents before writing.

1. Read `STYLE_PROFILE.md`. Drafters also read `STYLE_EXEMPLARS.md`.
2. If override exists in cwd, read and merge (override wins on conflict).
3. Return section 3.1 banned words, section 3.2 approved transitions, section 2 dials, section 11 hard rules, section 12 checklist. Verbatim, no paraphrase.

## Mode 2. Tighten

Called when the user says a paragraph is 장황 / 두루뭉실 / too long / vague, or
by `paper-style-enforcer` in `fix` mode. This mode rewrites sentences; it is
the only mode allowed to.

Apply STYLE_PROFILE section 11 in this order, one pass each:

1. **11.9 step-named claims**: every `consumed / regenerated / participates /
   governs` names its elementary step and species, or the sentence goes.
2. **11.3 named referents**: replace event, process, and pronoun subjects with
   the species, step, or quantity they stand for.
3. **11.4 signposts** and **11.8 restating**: delete announcement sentences,
   repeated comparisons, and obvious references (`above the reference`).
4. **11.5 comma-appositive values**: give each number its own predicate.
5. **11.6 abstract verbs**: `rest on / set / posit / lie in / stem from` become
   the direct relation.
6. **11.7 opener**: the first sentence of the paragraph is the claim; move
   `On <surface>` / `Under <conditions>` after the verb or drop.
7. **11.1 nominal padding** and **11.2 claim placement**.
8. Length: split any sentence over 30 words or with more than one `and`-joined
   clause. Target mean 16-22.

Then run `references/fluent-english.md` rules 1-5 (colon/semicolon chains, parenthetical
references, redundant numbers) if the text still has them.

### Hard rules for Mode 2

- Never change numbers, citation markers, chemical formulas, figure numbers, or
  the direction of a claim. If a rule would change what is claimed (for example
  11.9 asks for a step you do not know), flag `[STEP NEEDED]` instead of guessing.
- Do not add facts. If a sentence cannot be made concrete from the paragraph
  itself, delete it or flag it; do not invent the referent.
- Keep the author's route numbering and species notation exactly.

### Output

```
## Tightened text
<paragraph>

## Changes
- <rule id>: <original fragment> -> <new fragment>

## Flags
- <anything that needs the author: STEP NEEDED, claim direction, missing number>
```

## Mode 3. Light humanize

Called by `/paper-humanize`. This is a **light** pass. Do NOT rewrite, do NOT
inject voice, do NOT apply Mode 2. Only strip AI-isms.

### Strip list

- **Hard strip**: STYLE_PROFILE section 3.1 hard-ban list, verbatim.
- **Soft caution**: STYLE_PROFILE section 3.1 soft list. Flag if ≥3 per section, reduce ~50%, do not eliminate.
- **Structural patterns (flag only)**: STYLE_PROFILE section 3.5.
- **Em dash** (U+2014): replace with comma, period, or parenthesis. Max one per paragraph.
- **"As shown in Fig. X"** and **"as can be seen"** as opener: move the figure reference into `(Fig. X)`.
- **Rhetorical questions** and **mic-drop paragraph endings**.

### Density check (pre-rewrite step)

Grep the text for every section 3.1 word. Count per 500 words. Report before/after counts. Scientific terms load-bearing for the claim are always preserved.

### Hard rules for Mode 3

- Never change numbers, citation markers, chemical formulas, or any technical claim.
- If a word on the strip list is load-bearing for the claim, leave it and flag.
- If more than 30% of the paragraph would need editing, STOP and return `ESCALATE` (the paragraph needs Mode 2, not Mode 3).
- If the paragraph is already clean, return it verbatim with `NO_CHANGES`.

### Output

```
## Cleaned text
<paragraph>

## Changes
- <one line per edit>
```

## Computational results sections (all modes)

For a computational Results paragraph, read `~/.claude/skills/computational-section-writing/SKILL.md` (principles
A-F) and apply it before section 11. That file is the single source; nothing about computational paragraphs is
duplicated here.

## Figure and table captions (all modes)

**A caption describes what is shown, never what was found.** Results, values,
rankings, and interpretation belong in the body text; the caption tells the
reader how to read the panel. This is a hard rule, not a preference — a caption
that argues a conclusion is a wrong caption, even when the conclusion is
correct.

Belongs in a caption:

- what is plotted or rendered, and on which axes or in which view
- the system, conditions, and reference state (523 K, referenced to the
  H-precovered slab, etc.)
- how to decode the panel: colour and symbol keys, panel letters, what a dashed
  line or a highlighted band marks, sampling or error-bar definitions
- the source of comparison data, as a citation

Does NOT belong in a caption:

- numerical results ("the largest uphill step is 85 kJ mol⁻¹")
- comparisons and rankings ("the lowest of all routes", "agrees within
  10 kJ mol⁻¹")
- mechanistic or causal claims ("which excludes the ketene route")
- anything phrased as a finding ("shows that", "demonstrates", "confirms")

Rewrite pattern — name the quantity, drop the value and the verdict:

- ✗ "Free-energy profile of the aldol route. The largest single uphill step is
  the aldol coupling (85 kJ mol⁻¹)."
- ✓ "Free-energy profile of the aldol route at 523 K, referenced to the clean
  slab and two gas-phase CH₃COOH molecules. The highlighted band marks the
  largest single uphill step."

When a figure exists only to state a number (a benchmark panel whose entire
caption is residuals), the figure itself is usually the problem: either the
comparison belongs in a table, or the panel belongs in the SI with a caption
that says what was compared rather than how well it agreed.
