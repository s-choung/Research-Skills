<p align="center">
  <b>한국어</b> | <a href="README.en.md">English</a>
</p>

<h1 align="center">Research-Skills</h1>

<p align="center">
  <b>Claude Code에 한 줄이면 논문 작성, 피규어, 문서 자동화, AI 윤문까지</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skills-8A2BE2?style=flat" alt="Claude Code">
  <img src="https://img.shields.io/badge/Skills-17-blue?style=flat" alt="Skills">
  <img src="https://img.shields.io/badge/Benchmarks-7-green?style=flat" alt="Benchmarks">
  <img src="https://img.shields.io/badge/Codex_%2B_Claude_Code-compatible-orange?style=flat" alt="Compatible">
  <a href="https://schoung.com"><img src="https://img.shields.io/badge/Author-Seokhyun_Choung-black?style=flat" alt="Author"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> &middot;
  <a href="#-skills">Skills</a> &middot;
  <a href="#-benchmark">Benchmark</a> &middot;
  <a href="#-dependencies">Dependencies</a> &middot;
  <a href="#-license">License</a>
</p>

> **살아있는 skills입니다.** 지속적으로 관리되며, Claude Code와 Codex 모두에 적용 가능합니다.
>
> **Live page:** [s-choung.github.io/Research-Skills](https://s-choung.github.io/Research-Skills/)

---

## Quick Start

Claude Code에서 이렇게 말하세요:

```
https://github.com/s-choung/Research-Skills.git 클론하고 스킬 설치해줘
```

끝.

---

## Skills

### Humanizer

- **[humanizer_kor](skills/humanizer_kor)** -- AI가 쓴 한국어 글의 기계적 신호를 제거하고 사람이 쓴 것처럼 다듬는다.
- **[humanizer_eng](skills/humanizer_eng)** -- AI가 쓴 영어 글의 기계적 신호를 제거하고 사람이 쓴 것처럼 다듬는다.

### Paper Team

- **[paper](commands/paper.md)** -- 논문 작성 전 과정을 subagent 팀으로 처리하는 umbrella 명령어.
- **[paper-ref](commands/paper-ref.md)** -- 주장/주제에 맞는 후보 레퍼런스를 검색한다.
- **[paper-draft](commands/paper-draft.md)** -- IMRAD 섹션 초안을 저자 문체로 작성한다.
- **[paper-critic](commands/paper-critic.md)** -- 단락/섹션의 과학적 엄밀성을 비평한다.
- **[paper-humanize](commands/paper-humanize.md)** -- 논문 텍스트에서 AI 흔적을 제거한다.

### Media

- **[youtube](skills/youtube)** -- YouTube URL에서 transcript + metadata를 markdown으로 추출한다.
- **[youtube2mp4](skills/youtube2mp4)** -- YouTube 영상을 mp4로 다운로드한다.
- **[transcript2html](skills/transcript2html)** -- YouTube transcript markdown을 한국어 dark-mode HTML로 렌더한다.

### Document

- **[docx-scientific-formatting](skills/docx-scientific-formatting)** -- 논문 .docx의 화학식 아래첨자, italic, superscript를 자동 교정한다.
- **[html-minimal](skills/html-minimal)** -- 외부 JS framework 없는 self-contained HTML 리포트를 생성한다.
- **[design2html](skills/design2html)** -- 디자인 스펙 MD를 읽어 single-file HTML showcase 페이지를 생성한다.
- **[meetingnote-paperwork](skills/meetingnote-paperwork)** -- 한국 연구과제 회의록을 계산화학/소재 설계 voice로 draft한다.

### Visualization

- **[matplotlib-scientific](skills/matplotlib-scientific)** -- 출판용 matplotlib figure를 rcParams, colormap, legend/axis 포맷으로 생성한다.
- **[blender-atom-render](skills/blender-atom-render)** -- Structure 파일(XYZ, CIF, POSCAR)을 Blender sphere model + legend으로 렌더링한다.
- **[slide-audit](skills/slide-audit)** -- HTML slide의 글자 겹침/overflow 등 layout bug를 Playwright + 시각 검수로 탐지한다.

### Scientific Computing

- **[ase](skills/ase)** -- ASE(Atomic Simulation Environment) 코드 생성 스킬. 9개 LLM 벤치마크 포함.

### Utility

- **[pptx-too-heavy](skills/pptx-too-heavy)** -- PPTX 내 무거운 이미지를 찾아 용량순 HTML 리포트로 보여준다.
- **[smart-compact](skills/smart-compact)** -- /clear 직전에 세션 상태를 저장. 다음 세션이 자동으로 이어받는다.

---

## Benchmark

### humanize-writing

100개 AI 생성 한국어 단락(20개 장르)에 대한 윤문 벤치마크.

<p align="center">
  <img src="assets/humanize_bench_overview.png" width="90%" alt="Humanize Benchmark Overview"/>
</p>

| Metric | Original (AI) | Humanized |
| :---: | :---: | :---: |
| AI-Tell Score (lower = better) | 54.9 | **1.0** (-98.1%) |
| Naturalness (1-10) | 2.9 | **9.2** |
| Fidelity (1-10) | 10.0 | 8.8 |
| Change Rate | 0% | 27.9% |

> 인터랙티브 대시보드: [`humanizer_kor`](https://s-choung.github.io/Research-Skills/skills/humanizer_kor/benchmark/benchmark_report.html)

### humanize-writing (English)

100개 AI 생성 영어 단락(20개 장르)에 대한 윤문 벤치마크.

| Metric | Original (AI) | Humanized |
| :---: | :---: | :---: |
| AI-Tell Score | 89.8 | **3.6** (-96.0%) |
| Naturalness (1-10) | 1.2 | **9.4** |

> 인터랙티브 대시보드: [`humanizer_eng`](https://s-choung.github.io/Research-Skills/skills/humanizer_eng/benchmark/benchmark_report.html)

### ASE Skill

9개 LLM에 ASE 스킬을 주입한 50-task 코드 생성 벤치마크. 성공률만 표시.

<p align="center">
  <img src="assets/ase_bench_overview.png" width="90%" alt="ASE Benchmark Overview"/>
</p>

> 인터랙티브 대시보드: [`ase`](https://s-choung.github.io/Research-Skills/skills/ase/benchmark/benchmark_report_v6.html)

### matplotlib-scientific

기본 matplotlib vs 스킬 적용 Before/After. Scatter, Bar, Line 3종.

> 인터랙티브 대시보드: [`matplotlib-scientific`](https://s-choung.github.io/Research-Skills/skills/matplotlib-scientific/benchmark/benchmark_report.html)

### design2html

동일 콘텐츠(schoung.com)를 6개 디자인 시스템으로 생성한 결과물 비교.

> 인터랙티브 대시보드: [`design2html`](https://s-choung.github.io/Research-Skills/skills/design2html/benchmark/benchmark_report.html)

### blender-atom-render

POSCAR/CIF 구조 파일에서 Blender 레이트레이싱으로 렌더한 원자 구조 갤러리.

> 갤러리: [`blender-atom-render`](https://s-choung.github.io/Research-Skills/skills/blender-atom-render/benchmark/benchmark_report.html)

### transcript2html

/youtube + /transcript2html 워크플로우 데모. raw 자막 → 한국어 다크모드 HTML.

> 데모: [`transcript2html`](https://s-choung.github.io/Research-Skills/skills/transcript2html/benchmark/benchmark_report.html)

---

## Dependencies

| Skill | Requirement |
| :---: | :---: |
| `slide-audit` | `cd skills/slide-audit && npm install && npx playwright install chromium` |
| `youtube`, `youtube2mp4` | `brew install yt-dlp ffmpeg` |
| `blender-atom-render` | `brew install --cask blender` |
| `docx-scientific-formatting` | `pip install python-docx lxml` |
| `design2html` | Built-in specs 포함. `--full` 모드는 [impeccable](https://github.com/pbakaus/impeccable) 필요 |

---

## License

Seokhyun Choung. 자유롭게 쓰시고, contribution 환영합니다.
