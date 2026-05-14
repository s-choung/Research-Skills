<p align="center">
  <b>한국어</b> | <a href="README.en.md">English</a>
</p>

<h1 align="center">Research-Skills</h1>

<p align="center">
  <b>Claude Code에 한 줄이면 논문 작성, 피규어, 문서 자동화, AI 윤문까지</b>
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

Claude Code에서 이렇게 말하세요:

```
https://github.com/s-choung/Research-Skills.git 클론하고 스킬 설치해줘
```

끝.

---

## Skills

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>humanize-writing</h3>
      AI가 쓴 글의 기계적 신호를 제거하고 사람이 쓴 것처럼 다듬는다. 한국어/영어 모두 지원.<br><br>
      <code>이 글 humanize 해줘</code><br><br>
      <a href="skills/humanize-writing">README</a> · <a href="skills/humanize-writing/benchmark/benchmark_report.html">Benchmark</a>
    </td>
    <td width="50%" valign="top">
      <h3>paper (team)</h3>
      논문 작성 전 과정을 subagent 팀으로 처리. ref 검색, 섹션 초안, 비평, humanize까지.<br><br>
      <code>/paper introduction 레퍼런스 찾아줘</code><br><br>
      <a href="commands/paper.md">paper</a> · <a href="commands/paper-ref.md">ref</a> · <a href="commands/paper-draft.md">draft</a> · <a href="commands/paper-critic.md">critic</a> · <a href="commands/paper-humanize.md">humanize</a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>youtube / youtube2mp4</h3>
      YouTube URL에서 transcript + metadata + key frame을 markdown으로 추출. 영상 다운로드도 가능.<br><br>
      <code>/youtube https://youtu.be/... 무슨 내용이야?</code>
    </td>
    <td width="50%" valign="top">
      <h3>design2html</h3>
      디자인 스펙 MD를 읽어 single-file HTML showcase 페이지 생성. 7개 built-in 스펙 포함.<br><br>
      <code>/design2html ease-health</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>docx-scientific-formatting</h3>
      논문 .docx proof reading 자동화. 화학식 아래첨자, italic, superscript 검수/수정.<br><br>
      <code>manuscript.docx 화학식이랑 italic 수정해</code>
    </td>
    <td width="50%" valign="top">
      <h3>matplotlib-scientific</h3>
      출판용 matplotlib figure. rcParams, colormap, subplot, legend/axis 포맷.<br><br>
      <code>data.csv 그래프로 그려줘</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>blender-atom-render</h3>
      Structure 파일(XYZ, CIF, POSCAR)을 Blender sphere model + per-system legend으로 렌더링.<br><br>
      <code>/blender-atom-render structure.xyz</code>
    </td>
    <td width="50%" valign="top">
      <h3>slide-audit</h3>
      HTML slide의 글자 겹침/overflow 등 layout bug를 Playwright + 시각 검수로 탐지.<br><br>
      <code>/slide-audit deck.html</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>html-minimal</h3>
      외부 JS framework 없는 self-contained HTML 리포트/briefing 생성.<br><br>
      <code>분석 결과 HTML 리포트로 만들어줘</code>
    </td>
    <td width="50%" valign="top">
      <h3>smart-compact</h3>
      /clear 직전에 세션 상태를 저장. 다음 세션이 자동으로 이어받는다.<br><br>
      <code>/smart-compact</code>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>transcript2html</h3>
      YouTube transcript markdown을 한국어 dark-mode HTML로 렌더.<br><br>
      <code>/transcript2html transcript.md</code>
    </td>
    <td width="50%" valign="top">
      <h3>meetingnote-paperwork</h3>
      한국 연구과제 회의록 draft. 계산화학/소재 설계 voice로 작성.<br><br>
      <code>/meetingnote-paperwork 나노소재 과제 회의록 써줘</code>
    </td>
  </tr>
</table>

---

## Benchmark

### humanize-writing

100개 AI 생성 한국어 단락(20개 장르)에 대한 윤문 벤치마크.

<p align="center">
  <img src="assets/humanize_bench_overview.png" width="90%" alt="Humanize Benchmark Overview"/>
</p>

| Metric | Original (AI) | Humanized |
|---|---|---|
| AI-Tell Score (lower = better) | 54.9 | **1.0** (-98.1%) |
| Naturalness (1-10) | 2.9 | **9.2** |
| Fidelity (1-10) | 10.0 | 8.8 |
| Change Rate | 0% | 27.9% |

> 인터랙티브 대시보드: [`skills/humanize-writing/benchmark/benchmark_report.html`](skills/humanize-writing/benchmark/benchmark_report.html)

### transcript2html

YouTube transcript를 dark-mode 한국어 읽기 뷰로 렌더링한 예시.

<p align="center">
  <img src="assets/transcript2html_example.png" width="90%" alt="transcript2html example"/>
</p>

---

## Tree

```
skills/
  humanize-writing/       AI 글 humanize (한/영)
  paper-sections/          IMRAD 섹션 드래프팅
  paper-style/             저자 문체 프로파일
  docx-scientific-formatting/  .docx 논문 교정
  matplotlib-scientific/   출판용 figure
  blender-atom-render/     원자 구조 렌더링
  slide-audit/             슬라이드 레이아웃 검수
  html-minimal/            미니멀 HTML 리포트
  design2html/             디자인 스펙 -> HTML
  smart-compact/           세션 상태 저장
  youtube/                 YouTube transcript 추출
  youtube2mp4/             YouTube 영상 다운로드
  transcript2html/         transcript HTML 렌더
  meetingnote-paperwork/   연구과제 회의록

agents/
  paper-ref-hunter         논문 레퍼런스 검색
  paper-section-drafter    섹션 초안 작성
  paper-scientific-critic  과학적 비평
  paper-style-enforcer     문체 강제

commands/
  /paper                   논문팀 umbrella
  /paper-ref               레퍼런스 헌팅
  /paper-draft             섹션 드래프트
  /paper-critic            비평
  /paper-humanize          AI 흔적 제거
  /paper-plan              작성 계획
```

---

## Subagent 토큰 주의

Paper team이 dispatch하는 subagent는 각자 context window를 띄우므로 **토큰 사용량이 빠르게 커집니다**. 필요한 순간에만 쓰세요.

---

## Dependencies

| Skill | Requirement |
|---|---|
| `slide-audit` | `cd skills/slide-audit && npm install && npx playwright install chromium` |
| `youtube`, `youtube2mp4` | `brew install yt-dlp ffmpeg` |
| `blender-atom-render` | `brew install --cask blender` |
| `docx-scientific-formatting` | `pip install python-docx lxml` |
| `design2html` | Built-in specs 포함. `--full` 모드는 [impeccable](https://github.com/pbakaus/impeccable) 필요 |

---

## License

Seokhyun Choung. 자유롭게 쓰시고, contribution 환영합니다.
