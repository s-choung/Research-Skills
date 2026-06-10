---
name: ccel_slide_skill
description: CCEL 연구과제 발표자료 스타일로 슬라이드 덱을 생성. 어떤 주제/기존 PPT든 받아서 네이비-골드-오렌지 + 나눔스퀘어 + 탭칩 패널 스타일의 HTML과 PPTX를 동일하게 만들고 fade 애니메이션을 양쪽에 똑같이 주입. Triggers - /ccel_slide_skill, ccel 슬라이드, ccel 스타일, CCEL slide, 과제 스타일 슬라이드, 과제 발표자료 ppt, 그 네이비골드 과제 스타일.
---

# ccel_slide_skill — CCEL 과제 스타일 슬라이드 생성

어떤 주제·어떤 원본 PPT가 와도 **항상 동일한 CCEL 과제 스타일**로 HTML 덱과 PPTX를
**둘 다, 같은 모습으로** 생성한다. 스타일 수치는 원본에서 실측한 값으로
`references/style-spec.md`(SSOT)에 고정되어 있다. **임의 변경 절대 금지.**

## 철칙 (무슨 일이 있어도)

1. **HTML과 PPTX는 같은 레이아웃·같은 색·같은 텍스트**로 나와야 한다. 한쪽만 만들지 말 것 (사용자가 명시적으로 한쪽만 요청한 경우 제외).
2. **fade 애니메이션 필수**: 슬라이드 전환 fade 700ms + 콘텐츠 블록 fade-in 500ms/300ms stagger (자동 시작). 양쪽 동일.
3. **겹침(layering)은 시그니처**: 탭 칩은 컨테이너 상단 모서리에 반드시 겹치게, 텍스트는 도형 위에 올린다. z순서: 그림자 스트립 → 컨테이너 → 칩 → 텍스트.
4. **alpha·라운딩 실측값 고수**: 그림자 스트립 #324A88@10% / #DCDAB2@31%, 라운딩 adj 6386(컨테이너)·12808(카드)·23741(요약밴드)·39062(칩)·50000(알약) 등. 전부 spec 참조.
5. 폰트는 나눔스퀘어 ExtraBold(제목/강조) + 나눔스퀘어 Bold(본문) 고정.

## 워크플로

### 0. 준비
- `references/style-spec.md`를 **반드시 먼저 Read** (토큰·수치 SSOT).
- 입력이 기존 PPT/문서면 내용(텍스트·구조)만 추출하고 스타일은 전부 버린다.

### 1. 콘텐츠 플랜
- 슬라이드 구성: 타이틀 → 콘텐츠 N장 → (선택) 클로징.
- 각 콘텐츠 슬라이드를 패널 단위로 설계: 1패널(전폭) / 2패널(좌우 대비: 기존=gray·gold vs 제안=navy) / 패널+요약밴드 / 푸터밴드.
- 강조 런 계획: 본문 속 핵심 단어만 오렌지(#FA901E) 또는 네이비(#0F0F70) ExtraBold.

### 2. HTML 생성
- `templates/deck.html`을 베이스로 콘텐츠 슬라이드 작성 (컴포넌트 클래스: `.header .panel .tab-chip .card .grad-card .chip .pill .summary-band .navy-footer .divider-v .em-o/.em-n/.em-g`).
- 등장 순서대로 콘텐츠 블록을 `.fade-block`으로 감싼다 (헤더는 fade-block 아님).
- 마지막에 에셋 인라인:
  `conda run -n base python ~/.claude/skills/ccel_slide_skill/scripts/inline_assets.py <out.html>`

### 3. PPTX 생성
- 빌드 스크립트를 작성해 `scripts/ccel_pptx.py`를 import (sys.path에 scripts 추가).
- HTML과 같은 좌표 체계: **px ÷ 37.795 = cm**. HTML에서 잡은 레이아웃을 cm로 환산해 그대로 배치.
- 각 슬라이드 끝에 `deck.add_fade_animation(slide, [도형들 등장순서])` 호출 — HTML의 `.fade-block` 순서와 동일하게.
- `deck.save()`가 fade 전환을 전 슬라이드에 자동 주입.
- 실행: `conda run -n base python <build.py>`

### 4. 검증 (필수 — verification-before-completion)
1. PPTX 무결성: `soffice --headless --convert-to pdf` 성공 + `pdftoppm`으로 PNG 렌더.
2. HTML 스크린샷과 PPTX 렌더를 나란히 비교 — 색/레이아웃/겹침 불일치 시 수정.
3. 글자 겹침/overflow 검사: 큰 덱이면 `slide-audit` 스킬 활용.
4. 애니메이션 XML 확인: 생성된 pptx에서 `grep -c 'animEffect' ppt/slides/slide*.xml` ≥ 1 per content slide.

## 컴포넌트 치트시트 (상세는 style-spec.md)

| 컴포넌트 | PPTX (ccel_pptx) | HTML 클래스 |
|---|---|---|
| 헤더 밴드 | `add_content_slide(title, subtitle, page=(n,total))` | `.header` + `.title` + `.pagenum` |
| 메인 패널+탭칩 | `panel(s,x,y,w,h,color,tab=...)` | `.shadow-strip` + `.panel` + `.tab-chip` |
| 내부 카드 | `card(...)` | `.card` |
| 그라데이션 카드 | `grad_card(...)` | `.grad-card` |
| 칩/알약 | `chip(...)` / `pill(...)` | `.chip` / `.pill` |
| 요약 밴드 | `summary_band(s,y,runs)` | `.summary-band` |
| 네이비 푸터 | `navy_footer(s,runs)` | `.navy-footer` |
| 세로 구분선 | `divider_v(...)` | `.divider-v` |
| 타이틀 슬라이드 | `add_title_slide(...)` | `.slide.dark` + `.title-*` |
| 클로징 | `add_closing_slide(...)` | `.closing-msg` |

섹션색 사용 규칙: **navy=제안/핵심, gold=성과/파급효과, gray=기존/한계, orange=포인트 강조**.

## 파일

- `references/style-spec.md` — 실측 스타일 SSOT (필독)
- `scripts/ccel_pptx.py` — PPTX 빌더 (fade 타이밍 XML 포함)
- `scripts/inline_assets.py` — HTML 에셋 base64 인라인
- `templates/deck.html` — HTML 덱 템플릿 (전 컴포넌트 데모)
- `assets/header_band.png` — 헤더 웨이브 스트립 (원본 크롭)
- `assets/wave_bg.jpg` — 타이틀/클로징 풀블리드 배경
