# humanize-writing

AI가 쓴 글에서 기계적 신호를 제거하고, 특정 사람이 쓴 것처럼 자연스럽게 다듬는 스킬.

한국어·영어 모두 지원. "humanize", "자연스럽게", "AI 티 없애줘", "사람처럼 고쳐" 등으로 트리거.

## Three Rules

| 우선순위 | 규칙 |
|---|---|
| 1 | **사실을 지어내지 않는다** — 원문에 없는 수치·인용·경험·감정 추가 금지 |
| 2 | **기계적 신호를 제거한다** — banned vocabulary, 균일 리듬, 공식적 구조 해체 |
| 3 | **구체성을 복원한다** — 추상 뒤에 숨은 실제 주장을 드러냄 |

## 사용법

```
이 글 humanize 해줘

<AI가 쓴 텍스트 붙여넣기>
```

파일 경로도 가능:
```
draft.md humanize 해줘
```

## Before / After

**Before** (AI 원문):
> 본 보고서에서는 2024년 상반기 고객 이탈률 증가 원인을 분석하고자 한다. 다양한 데이터 소스를 활용하여 종합적인 분석을 수행하였으며, 이를 통해 효과적인 대응 방안을 도출하고자 하였다. 분석 결과, 온보딩 프로세스의 개선이 필요한 것으로 판단된다.

**After** (humanized):
> 2024년 상반기 고객 이탈률이 40% 늘었다. 원인은 가격이 아니다 — 이탈 고객과 잔류 고객의 요금제 분포는 거의 같았다. 문제는 온보딩이다. 가입 후 30일 이내에 이탈한 고객은 평균 4.7건의 지원 티켓을 냈고, 같은 온보딩 단계 세 곳에서 같은 질문을 반복했다.

## Benchmark (100 AI-generated Korean paragraphs)

<p align="center">
  <img src="../../assets/humanize_bench_overview.png" width="100%" alt="Humanize Benchmark"/>
</p>

| Metric | Original (AI) | Humanized |
|---|---|---|
| **AI-Tell Score** (0~100, lower = better) | 54.9 | **1.0** |
| **Naturalness** (1~10) | 2.9 | **9.2** |
| **Fidelity** (1~10) | 10.0 | 8.8 |
| **Change Rate** | 0% | 27.9% |

> Full interactive report: [`benchmark/benchmark_report.html`](benchmark/benchmark_report.html)

## 한국어 패턴 레퍼런스

`references/korean-patterns.md`에 한국어 AI 출력의 반복 패턴과 대체 방향이 정리되어 있음:

- **빈 강조** — "중요하다" → 구체적 결과나 비용
- **빈 수식어** — "다양한" → 실제 항목 2~3개
- **관료적 동사** — "활용하다" → "쓰다"
- **구조적 패턴** — "현대 사회에서" 도입부 삭제
- **어미 패턴** — "~할 필요가 있다" → "~해야 한다"

## 파일 구조

```
humanize-writing/
├── SKILL.md                          # 스킬 정의
├── README.md                         # 이 파일
├── references/
│   ├── korean-patterns.md            # 한국어 AI 패턴 목록
│   ├── examples.md                   # Before/After 캘리브레이션
│   └── guide.md                      # 심층 원칙 레퍼런스
└── benchmark/
    ├── benchmark_report.html         # 인터랙티브 벤치마크 대시보드
    ├── scored_vanilla.json           # 원문 100개 채점
    └── scored_new.json               # humanized 100개 채점
```
