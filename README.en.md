# Research-Skills

Claude Code skills, subagents, and slash commands for scientific research. Paper writing, scientific figures, document automation, and Korean research project paperwork.

**Authored by Seokhyun Choung** | https://schoung.com

[한국어 README](README.md) (default)

---

## Heads-up: subagent token usage

The paper team dispatches subagents (`paper-ref-hunter`, `paper-section-drafter`, `paper-scientific-critic`, `paper-style-enforcer`). Each subagent spawns its own context window, so **token consumption grows fast**. Fire them deliberately, not habitually.

---

## Install

Tell Claude Code (or Codex):

> clone https://github.com/s-choung/Research-Skills.git then "install the skills from `~/Research-Skills` for me."

That's it.

---

## Tree view

```text
/smart-compact                      save session state before /clear

/paper                              paper-team umbrella
├── /paper-ref <citation|topic>     hunt a citation or discover topic papers
├── /paper-plan <goal>              multi-step writing/revision plan
├── /paper-draft <section>          draft an IMRAD section in author voice
├── /paper-critic <paragraph>       rigor critique
└── /paper-humanize <paragraph>     final voice pass

/youtube <URL> [--frames N]         transcript + metadata + key frames -> md
/youtube2mp4 <URL> [--audio]        video download
/transcript2html <path>             dark-mode HTML render

/blender-atom-render <xyz|cif>      atom sphere render + legend
/slide-audit <html>                 detect slide layout bugs
/meetingnote-paperwork <task name>  Korean research meeting notes
```

Natural-language phrases also trigger these (e.g. "clean up this docx table", "plot data.csv", "single-file HTML report").

---

## Skills

### Daily drivers

- **`smart-compact`** -- save session state to `.claude/session-state.md` before `/clear`. Next session reads it back automatically.
  Example: `/smart-compact` -> `saved: 12 tasks, 3 open questions, focus "manuscript revision"`

- **`docx-scientific-formatting`** -- proof-reads `.docx` manuscripts for chemical subscripts (H2O -> H₂O, CO2 -> CO₂), italics (*in situ*, *operando*), superscripts, and equation formatting.
  Example: `"clean up chemical formulas in manuscript.docx"` -> `14 fixes: H2O -> H₂O ×8, in situ -> *in situ* ×3, CO2 -> CO₂ ×3`

- **`html-minimal`** -- standalone HTML reports and briefings with no external JS framework. Self-contained output.
  Example: `"today's analysis as an HTML report"` -> `output/2026-04-15_analysis.html (single file, 23 KB)`

- **`youtube`** -- pulls transcript, metadata, and key-frame screenshots from a YouTube URL into a single markdown file. Smart frame capture: heatmap peaks -> chapter starts -> uniform interval.
  Example: `/youtube https://youtu.be/ID --frames 8` -> `transcript.md + frames/frame_000_0020.jpg ×8`

- **`paper-humanize`** -- final pass on a draft paragraph before user review. 2-pass pipeline (global humanize -> `STYLE_PROFILE.md` enforcement).
  Example: `/paper-humanize <paragraph>` -> `pass 1: 6 AI-tells removed | pass 2: 3 voice fixes + sentence length rebalanced`

### Reach for when needed

- **`paper`** -- umbrella. Parses natural-language intent and dispatches to the right sub-command.
  Example: `/paper find refs for the introduction` -> `dispatched to /paper-ref (discovery mode)`

- **`paper-ref`** -- HUNT mode (specific citation -> Crossref verified DOI) + DISCOVERY mode (topic -> OpenAlex shortlist). Mode auto-detected from input shape.

  - Hunt: `/paper-ref Tanaka 2021 grain boundary zirconia JACS` -> `DOI verified, no field discrepancies`
  - Discovery: `/paper-ref recent transition metal oxide review papers` -> `top 5 candidates with title, authors, journal, year`

- **`paper-plan`** -- multi-step writing/revision plan (reviewer responses, section outlines, rebuttal structure).
  Example: `/paper-plan manuscript revision, 4 reviewer comments to address` -> `8-step plan with subagent assignment (triage -> ref hunt -> draft -> critic -> humanize)`

- **`paper-draft`** -- draft an IMRAD section in the author's voice.
  Example: `/paper-draft Introduction -- computational screening motivation` -> `4-paragraph draft with numeric-superscript citations`

- **`paper-critic`** -- rigor critique (unsupported claims, overclaims, logical gaps, missing controls).
  Example: `/paper-critic <paragraph>` -> `3 issues: unsupported claim (L4), missing control (L7), overclaim (L9)`

- **`paper-sections`, `paper-style`** -- internal reference libraries. You don't call these directly.

- **`matplotlib-scientific`** -- publication-quality matplotlib figures (rcParams, colormaps, subplot, legend/axis formatting).
  Example: `"plot data.csv"` -> `figures/plot.png (300 DPI, publication rcParams)`

- **`blender-atom-render`** -- structure file (XYZ, CIF, POSCAR) -> Blender sphere render + per-system legend.
  Example: `/blender-atom-render structure.xyz` -> `render/structure.png + legend.png (4K)`

- **`slide-audit`** -- detect layout bugs in HTML slide decks (overlap, clipping, overflow) via Playwright + visual review.
  Example: `/slide-audit deck.html` -> `23 slides, 4 issues: slide 5 text clipped / slide 12 title-chart overlap / ...`

- **`meetingnote-paperwork`** -- draft Korean research project meeting notes (회의록) in a fixed template, in a computational chemistry / materials design voice.
  Example: `/meetingnote-paperwork <task name> 2` -> `2 notes, 3-4 bullets each, template format preserved`

- **`youtube2mp4`** -- YouTube video download (audio-only, resolution cap, time trim).
  Example: `/youtube2mp4 <URL> --audio` -> `VIDEO_ID.m4a (audio-only, 4:32)`

- **`transcript2html`** -- renders `/youtube` markdown output as a Korean dark-mode HTML document.
  Example: `/transcript2html output/ID/transcript.md` -> `transcript.html (dark mode, frames embedded)`

---

## Paper team setup

`paper-style` and `paper-style-enforcer` read `~/.claude/paper-team/STYLE_PROFILE.md`. This is **not shipped** -- the author's voice profile is personal. To use the paper team:

1. Create `~/.claude/paper-team/STYLE_PROFILE.md`
2. Start with a short paragraph describing your voice preferences, banned words/patterns, sentence rhythms, and citation format.
3. Expand the file iteratively -- add a rule whenever the enforcer misses something.

`paper-ref-hunter` calls Crossref and OpenAlex via `Bash` + `curl`. No API keys required.

---

## Dependencies

- `slide-audit` -- Playwright. `cd skills/slide-audit && npm install && npx playwright install chromium`
- `youtube`, `youtube2mp4` -- `brew install yt-dlp ffmpeg`
- `blender-atom-render` -- `brew install --cask blender`
- `docx-scientific-formatting` -- `pip install python-docx lxml`

---

## License

By Seokhyun Choung. Feel free to fork, modify, and contribute back. If this helped, an iced coffee from **더랩** would be much appreciated.
