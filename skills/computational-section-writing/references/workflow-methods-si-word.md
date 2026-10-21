# computational-section-writing: workflow, Intro, Methods, SI, Word (reference)

보조 파일. 본체는 ../SKILL.md (원칙 A~F). 아래 2a절은 본체로 흡수되었으니 본체를 따른다.


2026-09-14~15 DMF|hexane 계면 원고(emulsion, 이동현 공동)에서 사용자가 문장 단위로 교정한 내용과,
2026-10-06 PdSnO2 계산 파트 및 Sn/SnO2 bi-phase 원고의 사용자 코멘트(2a절)를 일반화한 규칙.
문체 세부는 `paper` 스킬(references/style.md, fluent-english.md), 그림은 `figure_construction`, Word 서식은 `docx-scientific-formatting`을 따른다.
이 스킬은 그 넷을 어떤 순서로, 어떤 판단 기준으로 쓰는지 정한다.

## 0. 시작 전에 확인 (질문 하나)

- 단독 논문인가, 기존 실험 논문에 들어가는 계산 파트인가.
  - 계산 파트면 Abstract는 3문장 안팎, Introduction은 계산이 답하는 질문의 배경만. 합성법이나 응용 일반론은 실험 저자가 쓴다. 이번에 이걸 안 물어서 Intro 2문단과 인용 6개를 다시 지웠다.
- 그 원고의 기존 초안이나 템플릿 경로, 저자, 제1목적(누구의 가설을 지지하는가).

## 1. Introduction

- 해당 현상에 대한 선행 연구(계면, 용매화, 핵생성 등)와 공백만 쓴다. 우리 계의 공정 맥락(액적, 에멀젼 조건)은 Results 첫 문단으로 보낸다.
- 마지막 문단은 "Here we ... to determine whether ..." 다음에 이 연구가 이해한 내용을 한 문장으로. "결과를 액적에 적용한다" 같은 절차 문장으로 끝내지 않는다.
- 인용 논문마다 그 결론이 우리 결과와 같은 방향인지 한 줄로 확인한다. 예: Jungwirth-Tobias는 Br⁻가 공기/물 계면에 농축된다고 보고했으므로 "Br⁻ 결핍이 선행 연구와 같다"고 쓰면 틀린다.
- 인용 수는 Methods 제외 10개 이하가 기본.

## 2. Results

- 한 절, 한 제목. 제목은 계산 분석임이 드러나는 짧은 명사구 ("Atomistic view of precursor ions at the DMF|hexane interface").
- 문단 틀: 왜 이 계산을 했나 → 무엇을 했나 → 결과 (Fig. X) → 의미. 결과 문장부터 던지지 않는다.
- 서술 순서 = Fig. 1a, 1b, 1c ... 순서. Supplementary는 그 흐름 중간에 결과를 뒷받침할 때만.
- 무거운 별도 계산(umbrella sampling, NEB 등)은 자기 문단을 갖고, 그 계산이 필요한 이유(구속 없는 계산으로는 알 수 없는 것)와 방법 한 문장을 먼저 준다.
- 수치는 문단마다 결론을 싣는 1~2개. 표준오차, seed 수, 층 깊이, 개별 이온 값 나열은 SI 표로.
- 뭉갠 표현 금지, 측정량으로:

| 쓰지 말 것 | 쓸 것 |
|---|---|
| fall off, gather, pile up | are depleted, are enriched |
| grow ahead of the bulk | more X form than in the bulk |
| holds 0.6 of the bulk | is 0.6 times the bulk value |
| a short distance inside | about 1 nm inside |
| binds more Br⁻ | is coordinated by more Br⁻ |
| moves the excess into, sits | the enriched layer lies |
| transient spikes | larger local density fluctuations |
| carries the same environment | has the same subsurface layer |

## 2a. 문단 설계 규칙 (필수, 2026-10 사용자 코멘트에서 추출)

**계산 Results 문단은 `../SKILL.md`의 원칙 A~F와 절차를 그대로 따른다.** 금지 목록이 아니라
원칙으로 판정한다. 요약:
- A. 이름은 대조 변수에서 맡는 역할로 짓고(hydroxylated / bare), 조건값과 방법으로 짓지 않는다. 쓰기 전 용어표 고정.
- B. 괄호는 측정값, 화학식, 그림 번호만. 약칭 정의와 설명은 넣지 않는다.
- C. 첫 문장은 `To <동사> <질문>, we <계산> (Fig. X)`로 고정. 질문은 판정형(judge, whether)이 아니라 이해형(how, what, why). 다양성은 동사(understand, reveal, identify, resolve, trace ...)와 질문 내용에서만.
- D. 본문 수치는 그 문장의 주장을 증명하는 값만(비교 1~2개). 2차 수치 금지. 핵심 수치 뒤 because 절.
- E. 절을 지워도 결론이 안 바뀌면 Methods로.
- F. 독자는 Methods를 안 읽었다. 방법 이름과 내부 약칭은 풀거나 뺀다.

절 단위 규칙(소제목, 문단 순서, 주어와 주장, 인용과 캡션)은 `section-level-rules.md`.
원본 코멘트는 `references/author-comments-2026-10.txt` (PdSnO2 33개, Sn/SnO2 21개).

## 3. 검증 그림은 Methods로

- 수렴(온도, 에너지, RDF 블록, 시간 변화), 상자 크기, 통계적 안정성 중 "계산을 믿어도 되는가"에 답하는 그림은 Methods에서 인용한다. Results 흐름에 한 문장씩 끼워 넣지 않는다.
- 결과를 보여 주는 그림만 Results에서 인용한다.
- 서로 다른 발견을 한 괄호에 묶지 않는다 ("Supplementary Figs. 1-4" 금지). 같은 이야기(수렴 진단 셋)만 묶는다. 쪼갤 때는 그림이 어느 섹션 소속인지부터 다시 정한다.

## 4. Methods

- 따라 할 수 있는 절차형: 계 구성 → 힘장 → MD → 추가 샘플링 → 분석. 각 단계는 "무엇을 어떻게 했다".
- 분자 수, 상자 크기 같은 목록은 SI 표로 보내고 본문에는 조성의 원리(실험 농도, 전하 균형)만.
- 판단 기준이 있는 수치는 근거와 함께 ("4.3 Å, the first minimum of the Pb-Br RDF").
- 파라미터 출처는 원 논문 표와 숫자를 대조한다. 빌드 스크립트 주석을 믿지 않는다. 다르면 "started from X-type parameters, production values differ, listed in Table S#"로 쓰고 "fitted"는 실제로 fitting한 경우만.
- Methods에 쓴 수치(상자, seed, 시간 창, 층 경계, 정의식)는 캡션, Results, Conclusions에서 반복하지 않는다. 초안 뒤 한 번 grep한다.

## 5. 캡션

- 무엇을 그렸고 어떻게 읽는지만. 상자 크기, 시점, seed, 평균 구간, 층 깊이, 정의식은 Methods에 있으면 넣지 않는다.
- 콜론, 세미콜론으로 이어 쓰지 않는다.

## 6. SI 번호

- Supplementary Fig.와 Table은 본문 첫 언급 순서(Results, 그다음 Methods)로 번호를 매긴다.
- 위치를 옮기면 번호, SI 파일 순서, SI 캡션 안 교차 참조를 함께 고친다.

## 7. Word 버전 관리 (사고 방지)

- 사용자가 docx를 한 번이라도 열어 고친 뒤에는 조립 스크립트로 다시 만들지 않는다. 새 버전 파일(v(n+1))에 필요한 문장만 교체한다. `scripts/replace_sentences.py`.
  - 2026-09-14에 조립 스크립트를 import만 해도 실행되게 짜서 사용자가 고친 제목을 덮어썼다. 조립 스크립트에는 `if __name__ != "__main__": raise` 가드를 넣는다.
- 작업 전 최신 버전의 텍스트를 읽어 사용자 수정 여부를 확인한다. 사용자 문장은 요청 없이 고치지 않는다.
- 문장 이동이나 삭제 뒤에는 인용 번호를 첫 등장 순서로 재정렬한다. `scripts/renumber_refs.py <docx>`.
- SI 순서 변경은 블록(그림, 캡션, 빈 줄)을 옮겨서 한다. 새로 조립하면 사용자 SI 수정이 날아간다.

## 8. 호출 순서 (다음 원고)

1. 이 스킬 → 0번 질문.
2. `/paper plan: ...` 로 claim과 그림 대응.
3. `figure_construction` 으로 본문 그림, SI 그림.
4. `/paper-ref` + `codex-research` 로 인용과 DOI.
5. `/paper-draft methods` → results → intro → abstract. 이 스킬 1~6번을 기준으로. Results 문단은 2a.1 순서(왜 → 어떻게 → 결과 → 의미)로.
5a. 초안 직후 2a.6 재검토를 문단마다 돌린다. 지칭어(this, it, they, both)와 주어가 방법인 문장을 grep한다.
6. `/paper-critic` 으로 "Methods 반복, 수치 과다, 뭉갠 표현, 인용 방향, 지칭 대상, 목적 문장 누락" 여섯 가지를 명시해 검수.
7. `paper` 스킬의 fluent-english.md와 style.md로 문장 단위 교정.
8. `docx-scientific-formatting` 과 7번 규칙으로 Word 버전 관리.
