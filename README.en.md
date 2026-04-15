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

  ```
  pass everything we've discussed to the next session. /smart-compact
  ```

- **`docx-scientific-formatting`** -- proof-reads `.docx` manuscripts for chemical subscripts (H2O -> H₂O), italics (*in situ*, *operando*), superscripts, and equation formatting.

  ```
  proof-reading manuscript.docx, please fix chemical formulas and italics
  ```

- **`html-minimal`** -- standalone HTML reports and briefings with no external JS framework. Self-contained output.

  ```
  turn today's analysis into a minimal HTML report
  ```

- **`youtube`** -- pulls transcript, metadata, and key-frame screenshots from a YouTube URL into a single markdown file. Smart frame capture: heatmap peaks -> chapter starts -> uniform interval.

  ```
  /youtube https://youtu.be/<video> let's talk about what this video is about
  ```

- **`paper-humanize`** -- final pass on a draft paragraph before user review. 2-pass pipeline (global humanize -> `STYLE_PROFILE.md` enforcement).

  ```
  /paper-humanize <paragraph> make it sound human, watch out for em-dashes
  ```

### Reach for when needed

- **`paper`** -- umbrella. Parses natural-language intent and dispatches to the right sub-command.

  ```
  /paper find intro refs > auto-dispatches to /paper-ref
  ```

- **`paper-ref`** -- HUNT mode (specific citation -> Crossref verified DOI) + DISCOVERY mode (topic -> OpenAlex shortlist). Mode auto-detected from input shape.

  ```
  /paper-ref Tanaka 2021 grain boundary zirconia JACS, look this up
  /paper-ref there was a recent transition metal oxide review, find it
  ```

- **`paper-plan`** -- multi-step writing/revision plan (reviewer responses, section outlines, rebuttal structure).

  ```
  /paper-plan ~~ my data is ready, read this and outline a plan
  ```

- **`paper-draft`** -- draft an IMRAD section in the author's voice.

  ```
  /paper-draft Introduction -- the motivation for computation is weak here
  ```

- **`paper-critic`** -- rigor critique (unsupported claims, overclaims, logical gaps, missing controls).

  ```
  /paper-critic tear this part apart
  <paragraph>
  ```

- **`paper-sections`, `paper-style`** -- internal reference libraries. You don't call these directly.

- **`matplotlib-scientific`** -- publication-quality matplotlib figures (rcParams, colormaps, subplot, legend/axis formatting).

  ```
  plot data.csv, matplotlib-scientific follow this format
  ```

- **`blender-atom-render`** -- Claude can do Blender rendering too. Structure file (XYZ, CIF, POSCAR) -> Blender sphere model + per-system legend.

  ```
  /blender-atom-render structure.xyz render as bird-eye view
  ```

- **`slide-audit`** -- catches slide text overlap well. Layout bugs (overlap, clipping, overflow) via Playwright + visual review.

  ```
  /slide-audit deck.html
  ```

- **`meetingnote-paperwork`** -- drafts Korean research project meeting notes (회의록).

  ```
  /meetingnote-paperwork nano materials XYZ project, 3 notes
  ```

- **`youtube2mp4`** -- YouTube video download (audio-only, resolution cap, time trim).

  ```
  /youtube2mp4 <URL> --audio
  ```

- **`transcript2html`** -- renders `/youtube` markdown output as a Korean dark-mode HTML document.

  ```
  /transcript2html output/ID/transcript.md
  ```

---

## Dependencies

- `slide-audit` -- Playwright. `cd skills/slide-audit && npm install && npx playwright install chromium`
- `youtube`, `youtube2mp4` -- `brew install yt-dlp ffmpeg`
- `blender-atom-render` -- `brew install --cask blender`
- `docx-scientific-formatting` -- `pip install python-docx lxml`

---

## License

By Seokhyun Choung. Feel free to fork, modify, and contribute back. If this helped, an iced coffee from **더랩** would be much appreciated.
