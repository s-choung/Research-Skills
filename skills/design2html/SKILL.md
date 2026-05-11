---
name: design2html
description: "Design spec MD 파일을 읽어 해당 디자인 시스템의 토큰·컴포넌트·레이아웃을 충실히 반영한 single-file HTML 쇼케이스 페이지를 생성한다. Triggers: /design2html, 디자인 HTML 만들어, design to html, 디자인 스펙 페이지, showcase page, design spec to webpage"
user-invocable: true
argument-hint: "<name or path> [--content <topic>] [--lang ko|en]"
---

# Design2HTML — Design Spec to Showcase HTML

Design spec MD 파일 하나를 입력받아, 해당 디자인 시스템을 **충실히** 반영한 single-file HTML 페이지를 생성하는 스킬.

## CRITICAL RULE: No Left Accent Borders

**카드, callout, 인용, 강조 요소에 `border-left` 스타일의 세로 강조선(accent line)을 절대 사용하지 말 것.**

- `border-left: Npx solid <color>` 형태의 왼쪽 강조 라인은 **전면 금지**
- 카드 강조가 필요하면 `background`, `box-shadow`, `border`(전체), 또는 `outline`을 사용
- callout/blockquote 강조는 배경색 변경이나 아이콘으로 대체
- 이 규칙은 모든 spec에 공통 적용되며, spec 자체에 border-left가 명시되어 있어도 무시한다
- 생성 후 self-check 시 `border-left` grep으로 위반 여부를 반드시 확인

## CRITICAL RULE: No Invented Styles

**`specs/` 폴더에 있는 built-in 스펙 또는 사용자가 직접 제공한 MD 파일만 사용할 것.**

- "dark mode", "brutalist", "glassmorphism", "terminal", "swiss" 등 임의 스타일을 발명하여 생성하는 것은 **금지**
- 사용자가 스타일을 지정하지 않으면 반드시 리스트를 보여주고 선택을 받을 것
- specs/ 폴더에 없는 스타일명을 사용자가 말하면 "해당 스펙이 없습니다. 아래 중 선택하세요"로 안내
- 여러 스타일을 동시에 생성할 때도 각각 built-in spec 기반이어야 함

## No-Argument Mode (인자 없이 호출 시)

인자 없이 `/design2html`만 호출하면, 아래 리스트를 보여주고 사용자에게 선택을 요청한다:

```
Available design styles:

  1. ease-health    — Calm clinical, green-blue
  2. look-inc       — Editorial, black-white serif
  3. parker-studio  — Scrapbook-chic, sage green
  4. panxo          — Data terminal, warm ink
  5. attio          — Precision toolkit, serif-sans
  6. ui             — Monochromatic blueprint
  7. openai         — Blank canvas, pure white

Pick a number or name (or pass a custom .md path):
```

사용자가 번호, 이름, 또는 경로를 응답하면 해당 스펙으로 Workflow를 시작한다.
추가로 콘텐츠 주제(`--content`)와 언어(`--lang`)도 이 시점에 물어본다:
- "어떤 내용으로 만들까? (예: AI 연구자 소개, SaaS 랜딩페이지, 포트폴리오)"
- 답변 없으면 기본값: 디자인 시스템 소개 페이지, 한국어

## Built-in Design Specs

`~/.claude/skills/design2html/specs/`에 7개 디자인 스펙이 번들되어 있다.
이름만으로 바로 사용 가능 (경로 불필요):

| 이름 | 스타일 | 파일 |
|------|--------|------|
| `ease-health` | Calm clinical, green-blue | `specs/ease-health.md` |
| `look-inc` | Editorial, black-white serif | `specs/look-inc.md` |
| `parker-studio` | Scrapbook-chic, sage green | `specs/parker-studio.md` |
| `panxo` | Data terminal, warm ink | `specs/panxo.md` |
| `attio` | Precision toolkit, serif-sans | `specs/attio.md` |
| `ui` | Monochromatic blueprint | `specs/ui.md` |
| `openai` | Blank canvas, pure white | `specs/openai.md` |

### Spec Resolution 순서

1. Built-in 이름 매칭: `ease-health` -> `~/.claude/skills/design2html/specs/ease-health.md`
2. 절대 경로: `/path/to/custom-spec.md`
3. 현재 디렉토리 상대 경로: `./my-spec.md`

새 스펙 추가: `specs/` 폴더에 MD 파일 복사하면 자동으로 이름 사용 가능.

## Workflow

### 1. Design Spec 파싱

MD 파일에서 다음 섹션을 추출:

| 섹션 | 추출 대상 |
|------|----------|
| `## Tokens — Colors` | 색상명, hex, CSS token, role |
| `## Tokens — Typography` | 폰트명, substitute, weights, sizes, line-height, letter-spacing, OpenType features |
| `### Type Scale` | role별 size/leading/tracking/token |
| `## Tokens — Spacing & Shapes` | spacing scale, border-radius, shadows, layout values |
| `## Components` | 컴포넌트명, role, 구체적 스타일 설명 |
| `## Surfaces` | surface level별 색상·용도 |
| `## Do's and Don'ts` | 필수/금지 규칙 |
| `## Layout` | 레이아웃 패턴 (max-width, section gap, hero 구조 등) |
| `## Agent Prompt Guide` | Quick Color Reference, Example Component Prompts |
| `### CSS Custom Properties` | `:root` 블록 전체 |
| `## Imagery` | 이미지 스타일 가이드 |

### 2. Font Resolution

MD의 각 폰트에서 **Substitute** 필드를 확인:
- Google Fonts에서 무료로 사용 가능한 substitute가 있으면 → Google Fonts `<link>` 태그로 로드
- substitute가 system font면 → system font stack 사용
- substitute 없으면 → 원본 폰트명 + generic fallback

```html
<!-- 예: Suisseintl → Inter, Faire Octave → Playfair Display -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Playfair+Display:wght@300&display=swap" rel="stylesheet">
```

**중요**: CSS에서 font-family 선언 시 substitute 폰트를 먼저, 원본을 뒤에:
```css
--font-suisseintl: 'Inter', 'Suisseintl', sans-serif;
```

### 3. HTML 생성 규칙

#### 구조

```
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Brand Name} — Design Showcase</title>
  <!-- Google Fonts -->
  <!-- CSS Custom Properties from spec -->
  <style>...</style>
</head>
<body>
  <nav>...</nav>
  <section class="hero">...</section>
  <section class="colors">...</section>
  <section class="typography">...</section>
  <section class="components">...</section>
  <section class="surfaces">...</section>
  <footer>...</footer>
</body>
</html>
```

#### 필수 섹션

1. **Navigation Bar** — MD의 Layout 섹션에 기술된 nav 스타일 반영. 브랜드명 + 샘플 링크 2-3개 + primary CTA 버튼
2. **Hero Section** — MD의 Layout/Agent Prompt Guide에 기술된 hero 패턴. 대형 헤드라인(display font) + 서브텍스트(body font) + CTA 버튼(들)
3. **Color Palette** — 모든 토큰 색상을 swatches로 표시. 각 swatch에 이름, hex, token명 표기
4. **Typography Showcase** — 각 폰트 패밀리를 Type Scale의 모든 단계로 표시. 실제 텍스트 샘플 포함
5. **Component Gallery** — MD의 Components 섹션에 정의된 모든 컴포넌트를 실제 렌더링. 각 컴포넌트 옆에 이름과 role 표기
6. **Surfaces** — surface level별 카드를 중첩하여 depth 표현
7. **Footer** — 브랜드명 + "Design System Showcase" + 생성 날짜

#### CSS 규칙

- MD의 `### CSS Custom Properties` 블록을 **그대로** `:root`에 삽입
- 모든 스타일링은 CSS custom properties를 통해 적용 (하드코딩 금지)
- `Do's and Don'ts`의 규칙을 엄격히 준수
- Spacing, border-radius, shadow 값은 반드시 토큰 사용
- 반응형: 모바일 (< 768px)에서 1-column, 데스크탑에서 spec대로

#### 컨텐츠 규칙

- `--content` 옵션이 있으면 해당 주제로 샘플 텍스트 생성 (e.g., `--content "AI SaaS product"`)
- 없으면 디자인 시스템 자체를 소개하는 텍스트 사용
- `--lang ko`면 한국어, `en`이면 영어 (기본: ko)
- 텍스트는 자연스럽고 실제 사이트같아야 함 — lorem ipsum 금지

### 4. Quality Checklist (생성 후 자체 검증)

생성된 HTML을 다음 체크리스트로 검증:

- [ ] 모든 색상이 CSS custom property로 참조되는가 (하드코딩 없음)
- [ ] 모든 폰트가 로드되고 적용되는가
- [ ] Type Scale의 모든 단계가 showcase에 포함되었는가
- [ ] Components 섹션의 모든 컴포넌트가 렌더링되었는가
- [ ] Do's 규칙을 모두 따르는가
- [ ] Don'ts 규칙을 하나도 위반하지 않는가
- [ ] Border-radius 값이 spec과 일치하는가
- [ ] Spacing 값이 spec과 일치하는가
- [ ] Shadow 값이 spec과 일치하는가 (있는 경우)
- [ ] Hero 레이아웃이 spec의 Layout 섹션과 일치하는가
- [ ] 반응형 동작하는가

### 5. Output

- 파일명: `{brand-name}-showcase.html` (MD 파일의 `# Title`에서 추출, kebab-case)
- 위치: design spec MD와 같은 디렉토리
- 단일 파일 (external dependencies는 CDN link만)

## 사용 예시

```
/design2html ease-health.md
/design2html panxo.md --content "AI analytics platform"
/design2html attio.md --content "CRM product" --lang en
```

## Post-Generation Pipeline (기존 스킬 연계)

HTML 생성 후, 기존 스킬들을 순서대로 호출해서 품질을 올린다.

### Step A: `/impeccable audit` — 기술 품질 점검

생성된 HTML 파일을 대상으로 `/impeccable audit` 호출.
- a11y (접근성), 반응형, 성능, anti-pattern 체크
- 점수화된 기술 리포트 수령
- CRITICAL/HIGH 이슈가 있으면 즉시 수정

### Step B: `/impeccable critique` — UX 디자인 평가

`/impeccable critique` 호출.
- Nielsen 10 heuristics 기반 UX 점수
- 5 persona 테스트 (power user, first-timer, a11y, stress, mobile)
- AI slop 탐지 (generic 느낌 제거)
- 디자인 피드백에 따라 수정

### Step C: `/impeccable polish` — 마감 디테일

`/impeccable polish` 호출.
- 정렬, 간격, 미세 디테일 최종 점검
- hover transition, cursor style, focus indicator
- orphan/widow 텍스트, 아이콘 정렬

### Step D: Self-audit — Spec Compliance 최종 확인

`/impeccable`과 별개로, design spec MD 대비 자체 검증 수행:

| 검사 항목 | 방법 |
|----------|------|
| Colors | CSS `:root`의 모든 color token이 spec과 일치하는지, 하드코딩 hex 없는지 |
| Typography | font-family, weight, size, line-height, letter-spacing, OpenType features 일치 |
| Spacing | border-radius, padding, gap, section-gap 값 일치 |
| Components | spec에 정의된 모든 컴포넌트가 HTML에 렌더링됐는지 |
| Do's/Don'ts | spec의 Do 항목 준수, Don't 항목 미위반 |
| Surfaces | surface level별 색상 일치 |

불일치 발견 시 수정 후 재검증.

### Step E: Playwright Screenshot + Visual Verification

HTML 완성 후 Playwright로 스크린샷을 찍어 시각적으로 확인한다.

**Desktop 캡처:**
```bash
npx playwright screenshot --viewport-size="1280,800" --full-page "file://<absolute-path-url-encoded>" "<output>.png"
```

**Mobile 캡처 (선택):**
```bash
npx playwright screenshot --viewport-size="375,812" --full-page "file://<absolute-path-url-encoded>" "<output>-mobile.png"
```

- URL의 공백은 `%20`으로 인코딩할 것
- output 파일명은 HTML과 동일하게 `.png` 확장자
- 캡처 후 `Read` 도구로 PNG를 열어 시각 검증 수행
- 검증 항목: 레이아웃 깨짐, 폰트 미로드, 색상 이상, overflow, 요소 겹침
- 문제 발견 시 HTML 수정 후 재캡처

## Full Pipeline 요약

```
/design2html spec.md
  1. Spec 파싱 + Font resolution
  2. HTML 생성
  3. Self-checklist 검증
  4. /impeccable audit    → 기술 품질
  5. /impeccable critique → UX 디자인
  6. /impeccable polish   → 마감 디테일
  7. Self-audit           → Spec compliance 최종 확인
  8. Playwright screenshot → 시각 검증 (desktop + optional mobile)
```

`--quick` 플래그: step 4-7 생략, self-checklist + screenshot만 수행.
`--full` 플래그 (기본): 전체 파이프라인 실행.
`--no-screenshot` 플래그: step 8 생략.

## 사용 가능한 기존 스킬 맵

| 상황 | 호출할 스킬 |
|------|-----------|
| 기술 감사 (a11y, perf, responsive) | `/impeccable audit` |
| UX 디자인 평가 | `/impeccable critique` |
| 마감 디테일 점검 | `/impeccable polish` |
| 색상 문제 | `/impeccable colorize` |
| 타이포 문제 | `/impeccable typeset` |
| 레이아웃/정렬 문제 | `/impeccable arrange` |
| 애니메이션 추가 | `/impeccable animate` |
| AI 슬롭 제거 | `/impeccable critique` (AI slop test 포함) |
| 반응형 문제 | `/impeccable adapt` |
| 전체 디자인 리뷰 | `/impeccable audit` + `/impeccable critique` |
