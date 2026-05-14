---
name: humanize-writing
description: Revise AI-generated or mechanical-sounding text so it reads like a specific person wrote it. Use this skill when the user asks to "humanize", "make natural", "remove AI feel", "rewrite like a person wrote it", fix "AI-sounding" or "기계적인" text, or pass AI detection. Also trigger when the user pastes text and asks for a more natural or human tone, in either English or Korean. Do NOT use for summarization, translation, or creative writing from scratch.
---

# Human Writing Revision

Revise text so it reads as if a specific person wrote it for a specific reader.

## Three Rules (in priority order)

1. **Don't fabricate.** Never invent facts, quotes, sources, personal experience, numbers, named actors, or emotions that aren't in the original. If the original is vague, make it honestly vague — don't fill the gap with plausible fiction.
2. **Remove mechanical signals.** Cut banned vocabulary, fix uniform sentence rhythm, break formulaic structure, restore contractions where natural.
3. **Restore specificity.** Where the original contains a real claim buried under abstraction, surface it. Where it contains nothing specific, leave the gap visible rather than decorating it.

## Process

### Step 1: Identify audience and edit depth

Infer the audience from three signals in the text:
- Terms used without definition → assumed reader knowledge
- Consequences stated without explanation → assumed reader stakes
- Pronoun pattern (you/we/one) → assumed relationship

Then choose the lightest sufficient edit:

| Signal | Action |
|---|---|
| Structure sound, surface awkward | **Light polish** — vocabulary, rhythm, contractions |
| Multiple paragraphs with no actor, event, or consequence | **Rewrite** — rebuild those paragraphs from their intended claim |
| User asks "what's wrong with this?" | **Diagnostic** — explain problems, don't rewrite unless asked |

If more than half the paragraphs need rebuilding, tell the user the text needs rewriting, not polishing, and confirm before proceeding.

### Step 2: Edit

**Opening.** If the first sentence could open any piece on the same general topic, replace it with the first specific claim, finding, event, or problem.

**Second paragraph.** Must advance the opening, not retreat to context or methodology. Context goes third or later.

**Sentences.** Each sentence needs: a named actor doing something, or a specific claim that could be wrong. If a sentence has neither and removing it doesn't break the paragraph, remove it.

**Rhythm.** Vary sentence length to reflect emphasis. Short after long lands harder. Don't vary for its own sake.

**Counter-arguments.** If the text dismisses a counter-argument with "both perspectives have merit" or equivalent, either engage it honestly (state the strongest objection, bring evidence, say what the evidence can't settle) or remove the false engagement entirely.

**Endings.** End when the point has landed. No summaries of what was just said, no generic forward-looking statements, no invitations to continue.

**Sources.** If a source is cited, it needs author, work, year, and specific claim. If any of these are missing and can't be found, flag it as unverified or remove it. Never present an unverifiable source with the confidence of a verified one.

### Step 3: Check for over-correction

Read the result and ask: is every specific detail earned by the original text, or was it inserted because this skill said to be specific? If a detail feels performed rather than observed — if the specificity announces itself — remove it. The goal is writing that could only come from someone who thought about this subject, not writing that demonstrates awareness of humanization techniques.

## Language-Specific References

- For Korean text: read `references/korean-patterns.md` before editing.
- For difficult judgment calls or calibration: read `references/examples.md`.
- For deeper principles behind any rule above: read `references/guide.md`.

## Output

Return the revised text first, without preamble.
Add a brief note on what changed only if the user asked for explanation.
Do not describe your process or mention this skill.
