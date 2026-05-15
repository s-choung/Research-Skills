<p align="center">
  <a href="README.md">한국어</a> | <b>English</b>
</p>

<h1 align="center">Research-Skills</h1>

<p align="center">
  One line in Claude Code / Codex for paper writing, figures, document automation, and AI text humanization
</p>

<p align="center">
  <a href="https://s-choung.github.io/Research-Skills/"><b>Dashboard</b></a> &middot;
  <a href="#skills">Skills</a> &middot;
  <a href="#benchmark">Benchmark</a>
</p>

---

## Quick Start

```
Clone https://github.com/s-choung/Research-Skills.git and install the skills
```

## Skills

| Category | Skill | Description |
|:--|:--|:--|
| **Writing** | [humanizer_kor](skills/humanizer_kor) | Humanize AI-generated Korean text |
| | [humanizer_eng](skills/humanizer_eng) | Humanize AI-generated English text |
| | [paper](commands/paper.md) | Paper writing umbrella (ref, draft, critic, humanize) |
| **Visualization** | [matplotlib-scientific](skills/matplotlib-scientific) | Publication-quality matplotlib figures |
| | [blender-atom-render](skills/blender-atom-render) | Structure files to Blender atom renders |
| | [slide-audit](skills/slide-audit) | Detect layout bugs in HTML slide decks |
| **Document** | [design2html](skills/design2html) | Design spec to single-file HTML showcase |
| | [docx-scientific-formatting](skills/docx-scientific-formatting) | Auto-fix subscripts and superscripts in .docx |
| | [html-minimal](skills/html-minimal) | Self-contained HTML reports, no dependencies |
| | [meetingnote-paperwork](skills/meetingnote-paperwork) | Korean research meeting note template |
| **Media** | [youtube](skills/youtube) | YouTube to transcript markdown |
| | [youtube2mp4](skills/youtube2mp4) | YouTube to mp4 download |
| | [transcript2html](skills/transcript2html) | Transcript to Korean dark-mode HTML |
| **Computing** | [ase](skills/ase) | ASE code generation (9-LLM benchmark included) |
| **Utility** | [pptx-too-heavy](skills/pptx-too-heavy) | Analyze heavy images in PPTX files |
| | [smart-compact](skills/smart-compact) | Save session state for auto-recovery |

## Benchmark

<p align="center">
  <img src="assets/ase_bench_overview.png" width="90%" alt="ASE Benchmark Overview"/>
</p>

| Skill | Key Result | Dashboard |
|:--|:--|:--|
| **humanizer_kor** | AI-Tell 54.9 &rarr; **1.0** (-98%) &middot; Naturalness 2.9 &rarr; **9.2** | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/humanizer_kor/benchmark/benchmark_report.html) |
| **humanizer_eng** | AI-Tell 89.8 &rarr; **3.6** (-96%) &middot; Naturalness 1.2 &rarr; **9.4** | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/humanizer_eng/benchmark/benchmark_report.html) |
| **ase** | 9 LLMs &times; 50 tasks code generation benchmark | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/ase/benchmark/benchmark_report_v6.html) |
| **matplotlib-scientific** | Before/After: scatter, bar, line | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/matplotlib-scientific/benchmark/benchmark_report.html) |
| **design2html** | Same content &times; 6 design systems | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/design2html/benchmark/benchmark_report.html) |
| **blender-atom-render** | POSCAR/CIF Blender render gallery | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/blender-atom-render/benchmark/benchmark_report.html) |
| **transcript2html** | Raw subtitles to dark-mode HTML | [**Dashboard**](https://s-choung.github.io/Research-Skills/skills/transcript2html/benchmark/benchmark_report.html) |

## Dependencies

| Skill | Requirement |
|:--|:--|
| `slide-audit` | `cd skills/slide-audit && npm install && npx playwright install chromium` |
| `youtube`, `youtube2mp4` | `brew install yt-dlp ffmpeg` |
| `blender-atom-render` | `brew install --cask blender` |
| `docx-scientific-formatting` | `pip install python-docx lxml` |
| `design2html` | Built-in specs included. `--full` mode needs [impeccable](https://github.com/pbakaus/impeccable) |

## License

Seokhyun Choung. Free to use and modify. Contributions welcome.
