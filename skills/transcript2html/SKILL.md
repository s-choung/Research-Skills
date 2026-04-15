---
name: transcript2html
description: Use when the user wants to convert a YouTube transcript.md (produced by /youtube or /youtube2script) into a readable Korean dark-mode HTML document, with frames embedded and a cleaned-up transcript_formatted.md. Triggers - /transcript2html, 트랜스크립트 HTML, 스크립트 읽기모드, transcript 읽기, 유튜브 스크립트 한국어, transcript 한국어 변환.
---

# Transcript -> Readable Korean HTML

`/youtube2script` 또는 `/youtube` 가 만든 `transcript.md` 를 받아서 두 개의 파일을 만든다:

1. **`transcript_formatted.md`** -- 원본 영어 raw transcript을 정리해서 오타/전사오류를 고치고, 2~3 어절 단위 chunk을 문단으로 합치고, 섹션 헤더를 붙이고, 프레임을 본문 사이에 끼운 **한국어** 읽기용 Markdown.
2. **`transcript.html`** -- dark mode + Stripe 스타일 + Pretendard 기반 읽기용 HTML. 프레임 카드 + 본문 카드 + pullquote + verdict 블록.

둘 다 원본 `transcript.md` 가 있는 디렉토리에 저장한다.

## Input

유저가 경로를 줄 수도 있고 (파일 또는 디렉토리), 안 주면 현재 cwd 아래 가장 최근 `output/*/transcript.md` 를 찾는다.

```
/transcript2html [path/to/transcript.md or output/dir/]
```

## Step 1. Read

- `transcript.md` 읽기 (Read tool)
- 같은 디렉토리의 `metadata.json` 읽기 (있으면) -- title, channel, duration, url, upload_date
- 같은 디렉토리의 `frames/` 디렉토리 스캔 -- `frame_NNN_MMSS.jpg` 형식
- `transcript.md` 상단의 `Frame source` 필드 확인: `heatmap` 이면 조회수 피크, `even` 이면 균등 간격 fallback -- 이건 hero eyebrow에 반영 ("YouTube 트랜스크립트 &middot; Mo Bitar &middot; 조회수 피크 10컷" 또는 "균등 10컷")
- 각 프레임마다 `### @ MM:SS` 아래 `> **대사**: <원문>` 블록이 있다. 이게 그 시점에 영상에서 실제로 언급되는 대사 원문. 이걸 **한국어로 번역해서** 프레임 바로 아래 `.frame-caption` 블록에 넣는다. (원문도 `<span class="raw">` 로 작게 병기)

## Step 2. Clean & Segment (영어 원본)

raw transcript에서:
- 2~3 어절 chunk을 문단으로 합친다
- 전사 오류 교정: 고유명사(회사명, 사람이름, 제품명), 자막 자동생성이 흔히 틀리는 스펠링, `[ __ ]` 같은 마스킹을 맥락상 자연스러운 단어로 복원 (억지로 욕설 넣지 말 것 -- 문맥에 맞는 표현 선택)
- 내용상 자연스러운 구분점 3~6개로 섹션 분할
- 각 섹션에 짧은 한국어 제목 부여
- 프레임 타임스탬프를 각 섹션 경계에 매핑

## Step 3. Translate to Korean

영어 원본 -> 자연스러운 **한국어 정중체 (~요체)** 번역.

### 스타일 규칙 (paper-style 원칙 차용)

**금지**:
- 번역어투 ("~이다", "~것이다", "~함에 있어서", "~을 통하여", "~에 대한 것이다")
- AI slop: "중요한 것은", "주목할 만한", "핵심은", "~에 다름 아니다", 과잉 병렬 "A, B, 그리고 C"
- 격식체 (~합니다, ~입니다) -- 이건 뉴스 아님
- 반말 (~해, ~야) -- 문서 읽기 용도
- 의미 부풀리기: "혁신적인", "놀라운", "획기적인"
- em dash (U+2014) -- 쉼표나 괄호 또는 줄바꿈으로
- 볼드+콜론 리스트 ("**속도:** 빨라요")
- 과잉 hedging ("~일 수도 있을 것 같습니다만")
- 세 개 나열 패턴 반복
- 이모지

**권장**:
- 해요체 (~요, ~어요, ~네요) 유지, 톤 일관성
- 짧은 문장 + 긴 문장 섞기. 균일한 리듬은 기계 느낌
- 원저자의 냉소/유머는 살리되 과장하지 말 것
- 영어 고유명사/제품명/기술용어는 그대로: ChatGPT, GPT-5, Claude, Gemini, Reddit, LinkedIn, Substack, Subnautica, PUBG, Krafton, Shark Tank, Mr. Wonderful, Delaware, Harvard Business School, Steam, IKEA, Grammarly, Slack, Iron Dome, Labradoodle, Roomba 등
- 단, 의역으로 더 자연스러운 것: "prompt engineering" -> "프롬프트 엔지니어링" (음차), "Inc. magazine" -> "Inc. 매거진", "CEO" -> "CEO" 그대로
- 의미가 한국어에 없는 표현은 의역 + 필요시 영어 원문 `<span class="en">original</span>` 병기 (남용 금지, 문서 전체 5회 이하)

### 억지해석 금지

원문이 과장이면 과장 그대로, 비꼬기면 비꼬기 그대로. 번역자가 "실은 이런 의미입니다"라고 풀이하지 말 것. 원문에 없는 맥락 추가 금지. 원문이 모호하면 모호한 대로 번역.

## Step 4. Write `transcript_formatted.md`

Markdown 구조:

```markdown
# {한국어 제목}

- **Channel**: ...
- **URL**: ...
- **Duration**: ...
- **Upload Date**: ...

---

## 1. {섹션1 제목}

![frame at MM:SS](frames/frame_NNN_MMSS.jpg)

{번역된 문단}

{번역된 문단}

---

## 2. {섹션2 제목}
...
```

프레임은 각 섹션 상단 또는 중간에 (섹션 길이에 따라). em dash 사용 금지 -- `--` 또는 쉼표로.

## Step 5. Write `transcript.html` (dark mode)

템플릿: `~/.claude/skills/transcript2html/template_dark.html`

Read로 템플릿 읽고, 다음 placeholder들을 치환:

| Placeholder | 내용 |
|---|---|
| `{{TITLE}}` | `<title>` 태그용 -- 한국어 제목 |
| `{{EYEBROW}}` | "YouTube 트랜스크립트 &middot; {channel}" |
| `{{TITLE_HTML}}` | h1용 HTML -- 두 줄 분리 가능, `<br>` 와 `<span class="dim">` 활용 |
| `{{LEDE}}` | 한 문단 요약 (2~3 문장, 낚시 말고 담백하게) |
| `{{HERO_STATS}}` | 4개 `<span class="stat-chip"><b>값</b> 라벨</span>` -- duration, 엔트리 수, 핵심 수치 2개 |
| `{{SECTIONS}}` | 전체 섹션 블록 |
| `{{URL}}` | 원본 URL |
| `{{URL_LABEL}}` | URL 축약 라벨 (e.g., `youtube.com/watch?v=...`) |
| `{{DATE}}` | `YYYY.MM.DD` -- 오늘 날짜 |

### 섹션 블록 구조

각 섹션:

```html
  <section>
    <p class="sect-kicker">Act 01</p>
    <h2 class="sect-title">{섹션 제목}</h2>

    <figure>
      <img src="frames/frame_NNN_MMSS.jpg" alt="frame at MM:SS">
      <figcaption>MM:SS</figcaption>
    </figure>
    <div class="frame-caption">
      <span class="label">이 시점 대사 &middot; MM:SS</span>
      <p class="ko">{해당 초의 대사 한국어 번역, 짧게 1~2문장. 핵심 키워드는 <strong>bold</strong>}</p>
      <span class="raw">{원문 영어, 너무 길면 말줄임}</span>
    </div>

    <div class="card">
      <p>{한국어 본문 문단, <u>키워드 밑줄</u>, <strong>핵심 단어 bold</strong>, <span class="key">중요 개념은 key class</span> 적극 사용}</p>
      <p>{문단}</p>
    </div>

    <figure>...</figure>
    <div class="frame-caption">...</div>
    <div class="card">...</div>
  </section>
```

### 강조 규칙 (필수)

본문 카드 문단은 시각적으로 뚜렷해야 한다. 한 문단당 최소 1~2회 강조.

- **`<strong>`**: 숫자, 금액, 핵심 명사. 섹션당 3~5회.
- **`<u>`**: 중요 서술어/개념. 섹션당 2~4회. accent 컬러 언더라인.
- **`<span class="key">`**: 개념 용어 (밑줄 + accent 컬러 + bold). 문서 전체 6~10회.
- **`<span class="hl">`**: 핵심 구문 강조 (accent-soft bg 배지). 문서 전체 5~8회.
- **`<span class="mark-y">`**: 노란 형광펜. 결정적 한 문장/핵심 수치에만. 문서 전체 3~6회.
- **`<em>`**: 인용된 대사 또는 톤이 다른 부분.

같은 단어를 4종 강조 다 입히지 말 것. 한 문장에 한 강조가 기본.

### 특수 블록

- **`.frame-caption`**: 모든 figure 바로 아래에 배치. 그 시점에 영상에서 실제로 나오는 대사를 한국어 번역 + 원문 병기. `<span class="label">이 시점 대사 &middot; MM:SS</span>` + `<p class="ko">` + `<span class="raw">`.
- **`.pullquote`**: 섹션 내 1회, 핵심 한 문장 강조용 -- 다크 gradient 카드, `<p class="kicker">핵심</p>` + `<p>인용문</p>`. 문서 전체 0~2회.
- **`.verdict`**: 문서 말미 1회. 원문의 결론/핵심 통찰 1문단. `.kicker`는 "결론" 또는 "핵심".

### Hero stats

4개 고정. 예시:
- duration: `07:52`
- 엔트리 수 or 섹션 수: `5 섹션`
- 핵심 수치1: `30K` + 라벨 "연구 데이터"
- 핵심 수치2: `$250M` + 라벨 "소송 규모"

값은 `<b>` 로, 라벨은 `<b>` 뒤 텍스트로.

## Step 6. Open

둘 다 연다:

```bash
open "path/to/transcript.html"
open -a MarkText "path/to/transcript_formatted.md"
```

## Output summary

완료 후 유저에게:
- 생성된 파일 2개의 상대경로
- 대략적인 섹션 수
- 한 줄: "전체 읽는 데 ~분"

## Notes

- 템플릿은 `~/.claude/skills/transcript2html/template_dark.html` 하나만 있음 (dark + Stripe 스타일 기본). 유저가 "light 모드" 또는 "minimal 스타일"을 명시하면 거절하지 말고 임시로 CSS를 수정해서 만들어도 됨 (대신 기본은 dark).
- **프레임 경로는 상대경로** (`frames/frame_NNN_MMSS.jpg`) -- HTML이 transcript.md 옆에 저장되므로 그대로 작동.
- 원본 `transcript.md` 건드리지 말 것. 새 파일만 만든다.
- 요약&middot;의역 수준은 전체 문장의 15% 이내. 원문 내용 누락 금지 (광고/구독 요청 아웃트로는 짧게 처리 가능).
