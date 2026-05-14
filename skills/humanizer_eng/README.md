# humanizer_eng

Remove AI signals from English text. Revise AI-generated English prose so it reads like a specific person wrote it for a specific reader.

## Three Rules

| Priority | Rule |
|---|---|
| 1 | **Don't fabricate** — never invent facts, quotes, sources, personal experience, or numbers not in the original |
| 2 | **Remove mechanical signals** — cut banned vocabulary, fix uniform rhythm, break formulaic structure |
| 3 | **Restore specificity** — surface real claims buried under abstraction |

## Before / After

**Before** (AI original):
> Remote work serves as a transformative force in the modern workplace. It has the ability to enhance employee satisfaction and foster greater work-life balance. Furthermore, organizations that leverage remote work arrangements can navigate the complexities of talent acquisition more effectively. It is worth noting that the benefits of remote work are multifaceted, encompassing both individual and organizational dimensions.

**After** (humanized):
> Remote work changed how companies hire and how employees structure their days. People who work from home skip the commute — that's roughly an hour a day in most metro areas — and generally report higher job satisfaction. Companies get to recruit from anywhere, which matters most for roles that are hard to fill locally.

**What changed:**
- "serves as a transformative force" -> specific actions
- "has the ability to enhance" -> direct statement
- "furthermore," "it is worth noting," "multifaceted" -> deleted
- "navigate the complexities of talent acquisition" -> "recruit from anywhere"
- No facts invented

## Usage

```
Humanize this text

<paste AI-generated English text>
```

File paths work too:
```
Humanize draft.md
```

Ask for diagnostics instead of a rewrite:
```
What's wrong with this text?

<paste text>
```

## How It Works

1. **Identify audience and edit depth** — infer reader from terms used without definition, consequences stated without explanation, pronoun patterns. Choose the lightest sufficient edit (light polish, rewrite, or diagnostic).
2. **Edit** — replace generic openings with specific claims, cut banned vocabulary, ensure every sentence has a named actor or falsifiable claim, vary rhythm, engage counter-arguments honestly, end when the point has landed.
3. **Sentence diagnostics** — actor test (who does what?), event test (what happened?), deletion test (does the paragraph survive without it?). Sentences failing all three are AI filler.
4. **Check for over-correction** — if specificity feels performed rather than observed, remove it.

## File Structure

```
humanizer_eng/
├── SKILL.md                          # Skill definition
├── README.md                         # This file
└── references/
    ├── guide.md                      # Deep principles reference
    └── examples.md                   # Before/after calibration
```
