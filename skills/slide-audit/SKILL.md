---
name: slide-audit
description: Render HTML slide decks to per-slide PNGs and verify layout by (1) deterministic Playwright bounding-rect diagnostic and (2) parallel subagents that visually review the screenshots. Catches text overlap, clipping, overflow, layout bugs. Triggers - 글자 겹침, 슬라이드 스크린샷, 슬라이드 검수, 슬라이드 검증, deck 리뷰, slide audit, slide overlap, slide verify, HTML 슬라이드 점검.
---

# slide-audit

HTML 슬라이드 덱 (1920×1080, `.slide` + `.is-active` 토글 방식)의 레이아웃을 두 단계로 검증:

1. **Rect diagnostic (deterministic)** — Playwright 로 `.slide-content`, `.card`, `.two-col > .col`, `.hero`, `.timeline` 의 `getBoundingClientRect()` 를 측정해 content 경계/캔버스 초과를 탐지. 서브에이전트보다 정확하고 재현성 있음.
2. **Visual audit (subagent)** — 각 슬라이드 PNG 를 병렬 서브에이전트가 이미지로 열어 텍스트 겹침·잘림을 확인.

메인 에이전트는 **절대 PNG 를 직접 Read 하지 말 것**. 컨텍스트 낭비. 모든 이미지 판독은 서브에이전트로 위임.

## 핵심 원칙 — 순서 엄수

```
1. measure.mjs     → rect 로 구조 버그부터 잡는다 (덱 1회 실행, ~10초)
2. screenshot.mjs  → PNG 생성
3. 서브에이전트 dispatch (병렬) → 시각 품질 확인
```

**2025-04-14 교훈 (스킬 존재 이유):** 서브에이전트가 "카드 하단이 footer 에 겹친다" 를 persistently 보고했는데, 표면 처리 (padding 조정) 로 2라운드 실패. Rect 측정으로 카드가 실제로 1033~1213px 까지 부풀어 캔버스 밖까지 튀어나왔다는 걸 확인 → 구조 CSS 버그 (grid auto-row + aspect-ratio + min-height 미설정) → 정확한 수정. **서브에이전트는 증상을 보고, measure.mjs 는 원인을 보여준다. 둘 다 돌려라.**

## 트리거

- 사용자가 슬라이드/덱/HTML 프레젠테이션의 글자 겹침·레이아웃 이슈·검증을 요청할 때
- 예: "슬라이드 겹침 확인", "deck 검증", "HTML 슬라이드 점검", "14페이지 잘린다"

## 전제 조건

대상 HTML 규약:

- 슬라이드는 `<section class="slide" data-index="NN">` 구조
- `.slide { opacity: 0 }`, `.slide.is-active { opacity: 1 }`
- 1920×1080 캔버스, center-anchored

## 설치 (최초 1회)

```bash
cd ~/.claude/skills/slide-audit
[ -d node_modules/playwright ] || npm install
npx playwright install chromium
```

**중요 (Claude Code 환경)**: Bash 샌드박스가 Chromium 서브프로세스를 killEPERM 으로 죽입니다. Playwright 실행 Bash 호출은 `dangerouslyDisableSandbox: true` 로.

## 워크플로

### 1. Rect diagnostic

```bash
node ~/.claude/skills/slide-audit/measure.mjs <html-path>
```

출력:
```
✓ slide 01  ok
✗ slide 14  col[0] bottom=1041 exceeds content bottom=860 by 181
...
30/30 slides clean, 0 with issues
```

- 문제 있는 슬라이드 있으면 exit 2
- **ISSUE 발견 시 즉시 CSS 수정 후 재측정. 다음 단계로 넘어가지 말 것.**
- rect 가 모두 clean 이면 구조는 안전. 다음으로.

### 2. Screenshot 생성

```bash
node ~/.claude/skills/slide-audit/screenshot.mjs <html-path> [outdir]
```

- `outdir` 생략 시 `<html디렉토리>/_screenshots/<파일명>/` 에 저장
- 각 슬라이드 → `slide_NN.png`
- `manifest.json` 에 목록 기록
- `.progress` 오버레이는 자동 숨김 (스크린샷에 "keys to navigate" 힌트 안 들어감)

### 3. 서브에이전트 병렬 dispatch (필수)

슬라이드를 **8장 이하씩 배치**로 나눠서 **병렬** 호출. 단일 메시지에 multi `Agent` tool_use.

**배치 크기 규칙:**
- 30장 → 4 배치 (8+8+7+7)
- 20장 → 3 배치 (7+7+6)
- 10장 이하 → 1 배치

각 서브에이전트에 다음 프롬프트 템플릿을 그대로 전달 (경로만 치환):

```
You are visually auditing screenshots of N slides from an HTML presentation deck.
Each PNG is a 1920×1080 render of one slide. Read each image using the Read tool
(it handles PNGs as images) and inspect it visually.

Target files:
1. <abs path>/slide_NN.png
...

Background: <1-2 lines about the deck — palette, structure, layout components>.

For EVERY slide, apply this checklist:
- Does the h1 title overlap or touch the pagenum on the right?
- Does text inside any card/container overflow its boundary (visible cut or extending past edge)?
- In 2-column or 3-column grids, do left/right contents encroach on each other?
- In hero layouts, does text overlap the image?
- Timeline nodes: do connector lines align with nodes?
- Does the slide-footer overlap any body content above it?
- Any element extending past the 1920×1080 canvas (clipped at edges)?
- Bullet lists visibly cut at card bottom?

RESPOND in this exact Markdown format, ONE SECTION PER SLIDE, no prose outside:

## Slide NN
- status: OK | ISSUE
- issues:
  - <short description — suspected cause>
- suggested-fix: <one-line CSS hint, or "none">

Rules:
- If OK, write `- status: OK`, `- issues:` (empty), `- suggested-fix: none`.
- Keep each issue to one line.
- Do NOT open any file other than the N PNGs listed.
- Do NOT provide a summary at the end.
- Do NOT echo the checklist.
```

### 4. 리포트 취합 + 의심스러우면 rect 재측정

서브에이전트 응답을 병합해 사용자에게 제시. 이슈가 보고됐는데 수정했는데도 "persistent" 가 반복되면 **measure.mjs 로 돌아가서 실제 bounding rect 확인**. 서브에이전트 vision 판단은 hallucination 가능 (없는 텍스트 "수석/차석" 을 보고한 실제 사례 있음). **Rect 는 거짓말 안 한다.**

## 파일

- `screenshot.mjs` — 슬라이드 PNG 렌더러
- `measure.mjs` — rect diagnostic
- `package.json` — Playwright 의존성
- `SKILL.md` — 이 문서

## 공통 CSS 버그 카탈로그 (경험 축적)

이 카탈로그는 rect diagnostic 이 실패했을 때 체크할 구조적 원인.

| 증상 (rect) | 원인 | 수정 |
|---|---|---|
| `card` bottom > content bottom | `.slide-content` grid auto-row + `.card-img { aspect-ratio }` | `.slide-content { grid-auto-rows: 100%; overflow: hidden }` + `.card { min-height: 0 }` + `.card-img { flex: 1 1 auto; min-height: 0; }` (aspect-ratio 제거) + `.card-body { flex: 0 0 auto }` |
| `col` bottom > content bottom | `.two-col > .col { flex column }` 에 min-height 없음, 내부 img intrinsic size | `.two-col { min-height: 0 }` + `.two-col > .col { min-height: 0; overflow: hidden }` + `.two-col > .col > img { flex: 0 1 auto; min-height: 0; max-height: 50%; object-fit: contain }` |
| `timeline::before` 선이 끝 node 밖으로 | 노드 개수 ≠ 5 (기본 설계) | 노드 개수별 left/right % 재설정 (4노드 = 12.5%, 3노드 = 16.6%) |
| footer overlap | `--content-h` 가 가용 높이 초과 | `240 (content-top) + content-h + gap + 60 (footer) + 80 (safe-y) ≤ 1080` 만족하는 content-h. 80px gap 권장 → `content-h: 620` |

## 주의

- 수정은 항상 **별도 턴**에서 사용자 승인 후 (검수만 이 스킬의 역할)
- 외부 리소스 (폰트·이미지 CDN) 의존 시 `networkidle` 대기로 충분
- measure.mjs 는 30 슬라이드 ≈ 8초, screenshot.mjs 는 ≈ 12초. 검수 1회 1분 이내에 완료됨
