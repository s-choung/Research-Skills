<p align="center">
  <a href="README.md">한국어</a> | <b>English</b>
</p>

<h1 align="center">Research-Skills</h1>

<p align="center">
  <b>One line in Claude Code for paper writing, figures, document automation, and AI text humanization</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skills-8A2BE2?style=flat" alt="Claude Code">
  <img src="https://img.shields.io/badge/Skills-16-blue?style=flat" alt="Skills">
  <img src="https://img.shields.io/badge/Agents-4-green?style=flat" alt="Agents">
  <img src="https://img.shields.io/badge/Commands-6-orange?style=flat" alt="Commands">
  <a href="https://schoung.com"><img src="https://img.shields.io/badge/Author-Seokhyun_Choung-black?style=flat" alt="Author"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> &middot;
  <a href="#-skills">Skills</a> &middot;
  <a href="#-benchmark">Benchmark</a> &middot;
  <a href="#-dependencies">Dependencies</a> &middot;
  <a href="#-license">License</a>
</p>

---

## Quick Start

In Claude Code, just say:

```
Clone https://github.com/s-choung/Research-Skills.git and install the skills
```

That's it.

---

## Skills

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>humanize-writing</h3>
      Remove mechanical signals from AI-generated text and make it read like a specific person wrote it. Korean and English.<br><br>
      <code>Humanize this text</code><br><br>
      <a href="skills/humanize-writing">README</a> · <a href="skills/humanize-writing/benchmark/benchmark_report.html">Benchmark</a>
    </td>
    <td width="50%" valign="top">
      <h3>paper (team)</h3>
      Full paper writing pipeline with subagent team. Reference hunting, section drafting, critique, and humanization.<br><br>
      <code>/paper find references for introduction</code><br><br>
      <a href="commands/paper.md">paper</a> · <a href="commands/paper-ref.md">ref</a> · <a href="commands/paper-draft.md">draft</a> · <a href="commands/paper-critic.md">critic</a> · <a href="commands/paper-humanize.md">humanize</a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>youtube / youtube2mp4</h3>
      Extract transcript + metadata + key frames from a YouTube URL as markdown. Video download supported.<br><br>
      <code>/youtube https://youtu.be/... what is this about?</code>
    </td>
    <td width="50%" valign="top">
      <h3>design2html</h3>
      Read a design spec MD and generate a single-file HTML showcase page. 7 built-in specs included.<br><br>
      <code>/design2html ease-health</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>docx-scientific-formatting</h3>
      Automated proof reading for scientific .docx files. Chemical formula subscripts, italic, superscript formatting.<br><br>
      <code>Fix chemical formulas and italics in manuscript.docx</code>
    </td>
    <td width="50%" valign="top">
      <h3>matplotlib-scientific</h3>
      Publication-quality matplotlib figures. rcParams, colormap, subplot, legend/axis formatting.<br><br>
      <code>Plot data.csv as a scientific figure</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>blender-atom-render</h3>
      Render structure files (XYZ, CIF, POSCAR) as Blender sphere models with per-system legends.<br><br>
      <code>/blender-atom-render structure.xyz</code>
    </td>
    <td width="50%" valign="top">
      <h3>slide-audit</h3>
      Detect text overlap, clipping, and overflow in HTML slide decks via Playwright + visual review.<br><br>
      <code>/slide-audit deck.html</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>html-minimal</h3>
      Self-contained HTML reports and briefings with no external JS frameworks.<br><br>
      <code>Make an HTML report of the analysis</code>
    </td>
    <td width="50%" valign="top">
      <h3>smart-compact</h3>
      Save session state before /clear. The next session picks up automatically.<br><br>
      <code>/smart-compact</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>transcript2html</h3>
      Render YouTube transcript markdown as a Korean dark-mode HTML reading view.<br><br>
      <code>/transcript2html transcript.md</code>
    </td>
    <td width="50%" valign="top">
      <h3>meetingnote-paperwork</h3>
      Draft Korean research project meeting notes in a fixed paperwork template.<br><br>
      <code>/meetingnote-paperwork project-name</code>
    </td>
  </tr>
</table>

---

## Benchmark

### humanize-writing

Benchmark on 100 AI-generated Korean paragraphs across 20 genres.

<p align="center">
  <img src="assets/humanize_bench_overview.png" width="90%" alt="Humanize Benchmark Overview"/>
</p>

| Metric | Original (AI) | Humanized |
|---|---|---|
| AI-Tell Score (lower = better) | 54.9 | **1.0** (-98.1%) |
| Naturalness (1-10) | 2.9 | **9.2** |
| Fidelity (1-10) | 10.0 | 8.8 |
| Change Rate | 0% | 27.9% |

> Interactive dashboard: [`skills/humanize-writing/benchmark/benchmark_report.html`](skills/humanize-writing/benchmark/benchmark_report.html)

### transcript2html

YouTube transcript rendered as a dark-mode Korean reading view.

<p align="center">
  <img src="assets/transcript2html_example.png" width="90%" alt="transcript2html example"/>
</p>

---

## Tree

```
skills/
  humanize-writing/       AI text humanizer (KR/EN)
  paper-sections/          IMRAD section drafting
  paper-style/             Author style profile
  docx-scientific-formatting/  .docx scientific proofing
  matplotlib-scientific/   Publication figures
  blender-atom-render/     Atom structure rendering
  slide-audit/             Slide layout verification
  html-minimal/            Minimal HTML reports
  design2html/             Design spec -> HTML
  smart-compact/           Session state save
  youtube/                 YouTube transcript extraction
  youtube2mp4/             YouTube video download
  transcript2html/         Transcript HTML renderer
  meetingnote-paperwork/   Research meeting notes

agents/
  paper-ref-hunter         Reference search
  paper-section-drafter    Section drafting
  paper-scientific-critic  Scientific critique
  paper-style-enforcer     Style enforcement

commands/
  /paper                   Paper team umbrella
  /paper-ref               Reference hunting
  /paper-draft             Section draft
  /paper-critic            Critique
  /paper-humanize          AI-ism removal
  /paper-plan              Writing plan
```

---

## Subagent Token Warning

Subagents dispatched by the paper team each open their own context window, so **token usage scales fast**. Use only when needed.

---

## Dependencies

| Skill | Requirement |
|---|---|
| `slide-audit` | `cd skills/slide-audit && npm install && npx playwright install chromium` |
| `youtube`, `youtube2mp4` | `brew install yt-dlp ffmpeg` |
| `blender-atom-render` | `brew install --cask blender` |
| `docx-scientific-formatting` | `pip install python-docx lxml` |
| `design2html` | Built-in specs included. `--full` mode needs [impeccable](https://github.com/pbakaus/impeccable) |

---

## License

Seokhyun Choung. Free to use and modify. Contributions welcome.
