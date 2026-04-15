---
name: html-minimal
description: Use when creating HTML reports, analysis documents, briefing materials, or any standalone HTML document. Triggers - HTML 리포트, 분석 문서, 브리핑, HTML 만들어, 리포트 작성, report, html document, 문서 만들어
---

# HTML Minimal

따뜻한 뉴트럴 색상, 엄격한 타이포그래피, 선과 여백만으로 구조를 잡는 미니멀 HTML 문서 스타일.

## 메타 정보

모든 문서 상단에 반드시 표기:

```html
<h1>제목</h1>
<p class="date">YYYY.MM.DD · 정석현</p>
```

날짜는 문서 생성 당일 실제 날짜. 하드코딩 금지.

## 색상 (5가지만)

| 변수 | 값 | 용도 |
|---|---|---|
| `--ink` | `#1a1a17` | 본문 텍스트 |
| `--paper` | `#fafaf7` | 배경 |
| `--muted` | `#6b6b63` | 보조 텍스트, 라벨 |
| `--rule` | `#d4d4cd` | 구분선 |
| `--mark` | `#ffe14d` | 노란 하이라이트 |

순수 검정(#000000), 순수 흰색(#ffffff) 금지. 차트는 `--ink`와 `--mark` 두 색만.

## 폰트 (3가지만)

| 역할 | 폰트 | 사용처 |
|---|---|---|
| 제목 전용 | DM Serif Display | h1만 |
| 본문 전용 | IBM Plex Sans KR | h2, h3, p, li, td 전부 |
| 숫자/코드 전용 | JetBrains Mono | 통계, 금액, %, 코드 |

Inter, Arial, Roboto, system-ui 금지. 반드시 Google Fonts 로드:

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=IBM+Plex+Sans+KR:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

## 타이포그래피 상세

| 요소 | 크기 | 웨이트 | 행간 | 비고 |
|---|---|---|---|---|
| h1 | 2.8rem | 400 (DM Serif) | 1.15 | letter-spacing: -1px |
| h2 | 0.75rem | 600 | 1.4 | 대문자 변환, letter-spacing: 3px |
| h3 | 0.7rem | 600 | 1.4 | 대문자 변환, letter-spacing: 2px |
| 본문 p | 15px | 300 | 1.75 | body 기본 |
| strong | 본문 동일 | 600 | 본문 동일 | |
| 보조 텍스트 | 0.82rem | 300 | 1.6 | 캡션, 설명 |
| 라벨 | 0.7rem | 600 | 1.4 | 대문자, letter-spacing: 1~3px |
| 숫자 대형 | 1.6rem | 400 (JetBrains) | 1.2 | 핵심 수치 |
| 숫자 인라인 | 0.82rem | 400 (JetBrains) | 본문 | 표, 리스트 내 수치 |

700, 800, 900 웨이트 금지. 300, 400, 600만 사용.

## 레이아웃

```css
body { max-width: 920px; margin: 0 auto; padding: 3rem; }
```

여백 규칙:
- h1 아래: 0.25rem (날짜와 붙임)
- 날짜 아래: 2.5rem
- h2 위: 2.5rem / 아래: 1rem
- p 아래: 1rem
- 섹션 간: 2~2.5rem

그리드만 사용. Flexbox 금지.

```css
/* 숫자 요약 행 4단 */
grid-template-columns: repeat(4, 1fr);
/* 비교 2단 */
grid-template-columns: 1fr 1fr; gap: 2rem;
/* 니치 카드 3단 */
grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--rule);
```

## 금지 요소

- 카드 UI (border-radius, box-shadow, 배경색 구분) 금지
- 이모지 금지
- Flexbox 금지
- 구조는 선(border)과 여백(padding)으로만

## 구성 요소

### 구분선

- 주요: `1px solid var(--ink)` (숫자 행 상하)
- 보조: `1px solid var(--rule)` (항목 사이, 표 행)
- 섹션 제목: `1px solid var(--rule)` (밑줄)
- 판정(verdict): `2px solid var(--ink)` (상하)

### 숫자 요약 행

문서 상단 핵심 수치 3~4개.

```html
<div class="num-row">
  <div class="num-cell">
    <div class="v">13.3조</div>
    <div class="l">장기요양보험 '23</div>
  </div>
</div>
```

- 상하 `--ink` 1px 선, 셀 사이 `--rule` 세로선
- 숫자: JetBrains Mono 1.6rem / 라벨: 대문자 0.7rem, `--muted`

### 순위 리스트

```html
<div class="entry">
  <span class="rank">01</span>
  <span class="name">이름</span>
  <span class="figure">수치</span>
  <span class="desc">설명</span>
</div>
```

3단 그리드: 순위(2rem) | 이름+설명(1fr) | 수치(auto). 순위는 JetBrains Mono, `--muted`. 항목 사이 `--rule` 하단선.

### 비교 표

- th: 대문자, 0.7rem, `--muted`, 하단 `--ink` 1px
- td: 하단 `--rule` 1px
- 첫 열 25%, 나머지 균등

### 판정(verdict) 블록

문서에서 가장 중요한 결론. 문서당 1번만.

```html
<div class="verdict"><p>결론 텍스트</p></div>
```

상하 `--ink` 2px, 패딩 1.25rem, 1.05rem.

### 니치 블록

3단 그리드. `--rule` 배경 + 각 셀 `--paper`로 1px 간격 구분선 효과.

```css
.niche { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--rule); }
.niche div { background: var(--paper); padding: .75rem .8rem; }
```

## 노란 하이라이트

`<mark>` 태그 사용. 문서 전체 5~8개 이하. 10초 훑기에 핵심 파악 가능해야 함. 숫자, 결론, 경고에만.

```css
mark { background: var(--mark); padding: 0 2px; font-weight: 400; }
```

## 문체 규칙

### 금지

- 의미 부풀리기: "a pivotal moment", "testament to"
- 홍보 문체: "vibrant", "groundbreaking", "nestled"
- -ing 분석체: "highlighting the importance of"
- 모호한 출처: "experts argue"
- 3개 나열: "innovation, inspiration, and insights"
- 부정 병렬: "It's not just X; it's Y"
- em dash 남용
- 볼드+콜론 리스트: "**Speed:** faster"
- 이모지
- 서비스 문체: "I hope this helps!"
- 과잉 헤징: "could potentially possibly"
- 밝은 전망 맺음: "the future looks bright"

### 권장

- 짧은 문장과 긴 문장 섞기. 균일한 리듬은 기계 느낌.
- 의견 넣기. "솔직히", "문제는", "이건 좀".
- 1인칭 가능하면 사용. "내가 보기에" > "it could be argued that".
- 복잡한 감정 인정. "좋아 보이지만 불안한 구석이 있다" > 장단점 나열.
- "is", "are", "has" 사용. "serves as", "stands as" 금지.

## 푸터

```html
<div class="foot">
  <span>출처 표기</span>
  <span>YYYY.MM</span>
</div>
```

상단 `--rule` 1px, 0.7rem, `--muted`, 좌: 출처 / 우: 연월.

## 전체 CSS 템플릿

모든 문서에 반드시 포함:

```css
:root {
  --ink: #1a1a17;
  --paper: #fafaf7;
  --muted: #6b6b63;
  --rule: #d4d4cd;
  --mark: #ffe14d;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'IBM Plex Sans KR', sans-serif;
  font-weight: 300;
  font-size: 15px;
  line-height: 1.75;
  padding: 3rem;
  max-width: 920px;
  margin: 0 auto;
}
mark { background: var(--mark); padding: 0 2px; font-weight: 400; }
h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2.8rem;
  font-weight: 400;
  line-height: 1.15;
  letter-spacing: -1px;
  margin-bottom: .25rem;
}
.date { font-size: .8rem; color: var(--muted); margin-bottom: 2.5rem; }
h2 {
  font-size: .75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--muted);
  margin: 2.5rem 0 1rem;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--rule);
}
h3 {
  font-size: .7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--muted);
  margin-bottom: .5rem;
}
p { margin-bottom: 1rem; }
strong { font-weight: 600; }

/* 숫자 요약 행 */
.num-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  margin: 1.5rem 0;
}
.num-cell {
  padding: .75rem 1rem;
  border-right: 1px solid var(--rule);
}
.num-cell:last-child { border-right: none; }
.num-cell .v {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.6rem;
  line-height: 1.2;
}
.num-cell .l {
  font-size: .7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--muted);
  margin-top: .25rem;
}

/* 순위 리스트 */
.entry {
  display: grid;
  grid-template-columns: 2rem 1fr auto;
  align-items: baseline;
  padding: .5rem 0;
  border-bottom: 1px solid var(--rule);
}
.entry .rank {
  font-family: 'JetBrains Mono', monospace;
  font-size: .82rem;
  color: var(--muted);
}
.entry .figure {
  font-family: 'JetBrains Mono', monospace;
  font-size: .82rem;
}
.entry .desc {
  font-size: .82rem;
  color: var(--muted);
}

/* 비교 표 */
table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
th {
  font-size: .7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--muted);
  text-align: left;
  padding: .5rem 0;
  border-bottom: 1px solid var(--ink);
}
td {
  padding: .5rem 0;
  border-bottom: 1px solid var(--rule);
  font-size: .82rem;
}
td:first-child, th:first-child { width: 25%; }

/* 판정 블록 (문서당 1회) */
.verdict {
  border-top: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  padding: 1.25rem 0;
  margin: 2rem 0;
}
.verdict p { font-size: 1.05rem; margin-bottom: 0; }

/* 니치 블록 */
.niche {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--rule);
  margin: 1rem 0;
}
.niche div {
  background: var(--paper);
  padding: .75rem .8rem;
}

/* 푸터 */
.foot {
  display: grid;
  grid-template-columns: 1fr auto;
  border-top: 1px solid var(--rule);
  padding-top: .75rem;
  margin-top: 3rem;
  font-size: .7rem;
  color: var(--muted);
}
```

## 완성 체크리스트

문서 작성 후 반드시 확인:

- 작성자(정석현)와 당일 날짜가 제목 아래에 있는가
- 색상 5가지만 사용했는가
- 폰트 3가지만 사용했는가
- 카드 UI, border-radius, box-shadow 없는가
- 노란 하이라이트 8개 이하인가
- 이모지 없는가
- AI 문체("groundbreaking", "vibrant", "nestled", "testament") 없는가
- em dash 없는가
- 볼드+콜론 리스트 패턴 없는가
- 3개 나열 패턴 없는가
- verdict 블록 1회만인가
- 푸터에 출처와 연월 있는가
