# Research-Skills

과학 연구용 Claude Code 스킬, subagent, slash command 모음입니다. 논문 작성, scientific figure, 문서 자동화, 한국 연구과제 행정 문서까지 다룹니다.

**저자: Seokhyun Choung (정석현)** | https://schoung.com

[English README](README.en.md)

---

## 주의: subagent 토큰

Paper team이 dispatch하는 subagent (`paper-ref-hunter`, `paper-section-drafter`, `paper-scientific-critic`, `paper-style-enforcer`)는 각자 context window를 띄우기 때문에 **토큰 사용량이 빠르게 커집니다**. 습관적으로 돌리지 마시고 필요한 순간에만 쓰세요.

---

## 설치

Claude Code(또는 Codex)에 이렇게 말씀하세요.

> https://github.com/s-choung/Research-Skills.git 이거 클론하고 "`~/Research-Skills`에 있는 skill들 설치해줘"

끝입니다.

---

## Tree view

```text
/smart-compact                      세션 상태 저장 후 /clear 대비

/paper                              논문관련 스킬 묶음
├── /paper-ref <citation|topic>     citation 확정 or 주제 발견
├── /paper-plan <goal>              multi-step 작성|수정 plan
├── /paper-draft <section>          IMRAD 섹션 draft
├── /paper-critic <paragraph>       rigor 비평
└── /paper-humanize <paragraph>     저자 voice 최종 pass

/youtube <URL> [--frames N]         transcript + metadata + key frame -> md
/youtube2mp4 <URL> [--audio]        영상 다운로드
/transcript2html <path>             dark-mode HTML 렌더링

/blender-atom-render <xyz|cif>      atom sphere render + legend
/slide-audit <html>                 slide layout bug 자동 탐지
/meetingnote-paperwork <과제명>     한국 연구과제 회의록 draft
```

자연어로도 호출됩니다. 예: "이 docx 표 정리해줘", "data.csv 그래프 그려줘", "분석 리포트 HTML 하나".

---

## Skills

### 자주 쓰는 것들

- **`smart-compact`** -- `/clear` 직전에 세션 상태를 `.claude/session-state.md`에 저장. 다음 세션이 자동으로 읽어옵니다.
  예: `/smart-compact` -> `saved: 12 tasks, 3 open questions, focus "manuscript revision"`

- **`docx-scientific-formatting`** -- 논문 `.docx` proof reading 자동화. 화학식 아래첨자(H2O -> H₂O, CO2 -> CO₂), italic(*in situ*, *operando*), superscript, 수식 서식을 검수|수정합니다.
  예: `"manuscript.docx 화학식 정리해줘"` -> `14 fixes: H2O -> H₂O ×8, in situ -> *in situ* ×3, CO2 -> CO₂ ×3`

- **`html-minimal`** -- 외부 JS framework 없는 self-contained HTML 리포트|briefing 생성.
  예: `"오늘 분석 결과 HTML 리포트로"` -> `output/2026-04-15_analysis.html (single file, 23 KB)`

- **`youtube`** -- YouTube URL에서 transcript + metadata + key frame screenshot을 한 번에 markdown으로 추출. Smart frame capture는 heatmap peak -> chapter -> uniform interval 순으로 fallback.
  예: `/youtube https://youtu.be/ID --frames 8` -> `transcript.md + frames/frame_000_0020.jpg ×8`

- **`paper-humanize`** -- Draft paragraph를 사용자 검토 직전에 저자 voice로 마지막 pass. 2-pass (global humanize -> `STYLE_PROFILE.md` enforcement).
  예: `/paper-humanize <paragraph>` -> `pass 1: 6 AI-tells 제거 | pass 2: 3 voice fix + sentence length 재조정`

### 필요할 때 꺼내 쓰는 것들

- **`paper`** -- umbrella. 자연어 의도를 파싱해서 sub-command로 dispatch.
  예: `/paper introduction 논문 레퍼런스 찾아줘` -> `dispatched to /paper-ref (discovery mode)`

- **`paper-ref`** -- Hunt mode (특정 citation -> Crossref verified DOI) + Discovery mode (주제 -> OpenAlex shortlist). Mode는 input 모양으로 자동 판단.
  
  - Hunt: `/paper-ref Tanaka 2021 grain boundary zirconia JACS` -> `DOI verified, no field discrepancies`
  - Discovery: `/paper-ref 최근 transition metal oxide 리뷰 논문` -> `top 5 candidates with title, authors, journal, year`

- **`paper-plan`** -- Multi-step 작성|수정 계획 (reviewer response, 새 섹션 outline, rebuttal 구조).
  예: `/paper-plan 논문 revision, reviewer comment 4개 대응` -> `8-step plan with subagent 배정 (triage -> ref hunt -> draft -> critic -> humanize)`

- **`paper-draft`** -- IMRAD 섹션을 저자 voice로 draft.
  예: `/paper-draft Introduction -- computational screening motivation` -> `4-paragraph draft with numeric-superscript citations`

- **`paper-critic`** -- Paragraph|섹션 과학적 비평 (unsupported claim, overclaim, logical gap, missing control).
  예: `/paper-critic <paragraph>` -> `3 issues: unsupported claim (L4), missing control (L7), overclaim (L9)`

- **`paper-sections`, `paper-style`** -- 내부 reference. 직접 호출할 일 없음.

- **`matplotlib-scientific`** -- 출판용 matplotlib figure (rcParams, colormap, subplot, legend/axis 포맷).
  예: `"data.csv 그래프로 그려줘"` -> `figures/plot.png (300 DPI, publication rcParams)`

- **`blender-atom-render`** -- Structure 파일(XYZ, CIF, POSCAR) -> Blender sphere model + per-system legend.
  예: `/blender-atom-render structure.xyz` -> `render/structure.png + legend.png (4K)`

- **`slide-audit`** -- HTML slide deck의 layout bug(overlap, clipping, overflow)을 Playwright + 시각 검수로 탐지.
  예: `/slide-audit deck.html` -> `23 slides, 4 issues: slide 5 text clipped / slide 12 title-chart overlap / ...`

- **`meetingnote-paperwork`** -- 한국 연구과제 회의록을 computational chemistry / materials design voice로 템플릿 draft.
  예: `/meetingnote-paperwork <과제명> 2개` -> `note 2개, bullet 3-4개씩, template format 유지`

- **`youtube2mp4`** -- YouTube 영상 mp4 다운로드 (audio-only, 해상도 제한, 구간 trim).
  예: `/youtube2mp4 <URL> --audio` -> `VIDEO_ID.m4a (audio-only, 4:32)`

- **`transcript2html`** -- `/youtube` 결과 markdown을 한국어 dark-mode HTML로 렌더.
  예: `/transcript2html output/ID/transcript.md` -> `transcript.html (dark mode, frames embedded)`

---

## Paper team 준비

`paper-style`과 `paper-style-enforcer`는 `~/.claude/paper-team/STYLE_PROFILE.md`를 읽습니다. 저자 voice profile은 개인적이라 **repo에 포함되지 않습니다**. 사용하시려면:

1. `~/.claude/paper-team/STYLE_PROFILE.md` 생성
2. 선호 voice, 금지 단어|패턴, sentence rhythm, citation format을 짧은 단락으로 작성
3. Enforcer가 뭔가 놓칠 때마다 rule을 추가하며 iteratively 확장

`paper-ref-hunter`는 Crossref와 OpenAlex를 `Bash` + `curl`로 호출합니다. API key 필요 없음.

---

## Dependencies

- `slide-audit` -- Playwright. `cd skills/slide-audit && npm install && npx playwright install chromium`
- `youtube`, `youtube2mp4` -- `brew install yt-dlp ffmpeg`
- `blender-atom-render` -- `brew install --cask blender`
- `docx-scientific-formatting` -- `pip install python-docx lxml`

---

## License

Seokhyun Choung 씀. 자유롭게 바꾸시고, contribution해주세요. 유용하셨다면 **더랩 커피 아이스** 한 잔 부탁드립니다.
