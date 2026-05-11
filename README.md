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

/design2html <spec|name>            디자인 스펙 MD -> showcase HTML
/blender-atom-render <xyz|cif>      atom sphere render + legend
/slide-audit <html>                 slide layout bug 자동 탐지
/meetingnote-paperwork <과제명>     한국 연구과제 회의록 draft
```

자연어로도 호출됩니다. 예: "이 docx 표 정리해줘", "data.csv 그래프 그려줘", "분석 리포트 HTML 하나".

---

## Skills

### 자주 쓰는 것들

- **`smart-compact`** -- `/clear` 직전에 세션 상태를 `.claude/session-state.md`에 저장. 다음 세션이 자동으로 읽어옵니다.
  
  ```
  지금까지 얘기한 내용을 다음세션에 넘길래. /smart-compact
  ```

- **`docx-scientific-formatting`** -- 논문 `.docx` proof reading 자동화. 화학식 아래첨자(H2O -> H₂O), italic(*in situ*, *operando*), superscript, 수식 서식을 검수|수정합니다.
  
  ```
  manuscript.docx 논문 proof reading중인데 화학식하고 italic 안된거 수정해 
  ```

- **`html-minimal`** -- 외부 JS framework 없는 self-contained HTML 리포트|briefing 생성.
  
  ```
  오늘 분석 결과 HTML 리포트로 미니멀하게 만들어줘 
  ```

- **`youtube`** -- YouTube URL에서 transcript + metadata + key frame screenshot을 한 번에 markdown으로 추출. Smart frame capture는 heatmap peak -> chapter -> uniform interval 순으로 fallback.
  
  ```
  /youtube https://youtu.be/유튜브 링크 무슨내용인지 나랑 얘기좀하자. 
  ```

- **`paper-humanize`** -- Draft paragraph를 사용자 검토 직전에 저자 voice로 마지막 pass. 2-pass (global humanize -> `STYLE_PROFILE.md` enforcement).
  
  ```
  /paper-humanize <paragraph> 좀 사람같이써. em dash조심. 
  ```

- **`design2html`** -- 디자인 스펙 MD 파일을 읽어 해당 디자인 시스템의 토큰/컴포넌트/레이아웃을 충실히 반영한 single-file HTML showcase 페이지를 생성. 7개 built-in 스펙 포함 (ease-health, look-inc, parker-studio, panxo, attio, ui, openai). `--quick`으로 빠르게, `--full`로 impeccable 품질 파이프라인까지.
  
  ```
  /design2html ease-health
  /design2html panxo --content "AI analytics platform" --lang en
  ```

### 필요할 때 꺼내 쓰는 것들

- **`paper`** -- umbrella. 자연어 의도를 파싱해서 sub-command로 dispatch.
  
  ```
  /paper introduction 논문 레퍼런스 찾아줘 > paper-ref 알아서 호출. 
  ```

- **`paper-ref`** -- Hunt mode (특정 citation -> Crossref verified DOI) + Discovery mode (주제 -> OpenAlex shortlist). Mode는 input 모양으로 자동 판단.
  
  ```
  /paper-ref Tanaka 2021 grain boundary zirconia JACS 논문 찾아봐.
  /paper-ref 최근 transition metal oxide 리뷰 논문있었는데 찾아봐. 
  ```

- **`paper-plan`** -- Multi-step 작성|수정 계획 (reviewer response, 새 섹션 outline, rebuttal 구조).
  
  ```
  /paper-plan ~~내 데이터가 충분히 쌓였어 이거읽고 계획 outline 해
  ```

- **`paper-draft`** -- IMRAD 섹션을 저자 voice로 draft.
  
  ```
  /paper-draft Introduction 부분에 계산이 왜 필요한지 논의가 약해. 
  ```

- **`paper-critic`** -- Paragraph|섹션 과학적 비평 (unsupported claim, overclaim, logical gap, missing control).
  
  ```
  /paper-critic 이부분 비난좀 해줘
  <paragraph>
  ```

- **`paper-sections`, `paper-style`** -- 내부 reference. 직접 호출할 일 없음.

- **`matplotlib-scientific`** -- 출판용 matplotlib figure (rcParams, colormap, subplot, legend/axis 포맷).
  
  ```
  data.csv 그래프로 그려줘matplotlib-scientific 이 포맷을 준수해.
  ```

- **`blender-atom-render`** -- Claude가 blender rendering도함. Structure 파일(XYZ, CIF, POSCAR) -> Blender sphere model + per-system legend.
  
  ```
  /blender-atom-render structure.xyz 이거 bird eye view로 렌더링해
  ```

- **`slide-audit`** -- HTML slide의 글자 겹침 등 잘잡아냄. layout bug(overlap, clipping, overflow)을 Playwright + 시각 검수로 탐지.
  
  ```
  /slide-audit deck.html
  ```

- **`meetingnote-paperwork`** -- 연구 회의록 draft해줌. 
  
  ```
  /meetingnote-paperwork 나노소재 뭐시기 과제이름 회의록 3개써
  ```

- **`youtube2mp4`** -- YouTube 영상 mp4 다운로드 (audio-only, 해상도 제한, 구간 trim).
  
  ```
  /youtube2mp4 <URL> --audio
  ```

- **`transcript2html`** -- `/youtube` 결과 markdown을 한국어 dark-mode HTML로 렌더.
  
  ```
  /transcript2html output/ID/transcript.md
  ```

---

## Dependencies

- `design2html` -- 7개 built-in 디자인 스펙이 `skills/design2html/specs/`에 포함됨. 추가 스펙은 [getdesign.md](https://getdesign.md/)에서 생성 가능. `--full` 모드(audit/critique/polish)를 쓰려면 [impeccable](https://github.com/pbakaus/impeccable) 플러그인 필요 (`/install-plugin pbakaus/impeccable`). `--quick` 모드는 impeccable 없이 동작.
- `slide-audit` -- Playwright. `cd skills/slide-audit && npm install && npx playwright install chromium`
- `youtube`, `youtube2mp4` -- `brew install yt-dlp ffmpeg`
- `blender-atom-render` -- `brew install --cask blender`
- `docx-scientific-formatting` -- `pip install python-docx lxml`

---

## License

Seokhyun Choung 씀. 자유롭게 바꾸시고, contribution해주세요. 유용하셨다면 **더랩 커피 아이스** 한 잔 부탁드립니다.
