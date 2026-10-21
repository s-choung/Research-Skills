---
name: computational-section-writing
description: Use when writing or revising the computational part (MD, DFT, MLIP) of a manuscript - Results paragraphs, Methods, SI numbering, Word versioning. Triggers - 계산 파트 써줘, 시뮬레이션 파트 원고, computational section, computational writing, 계산 결과 writing, 실험 논문에 계산 넣기, MD 결과 원고, DFT 결과 원고, Results 흐름, Methods 서술, SI 번호, 지칭 대상, in order to, 왜 했는지.
---

# computational-section-writing

계산 Results 문단을 쓰는 원칙 6개(A~F)와, 원칙에서 이름과 문장을 끌어내는 절차. 이 파일이 전부다.
예시는 설명용이다. 판정은 예시가 아니라 원칙으로 한다. 어떤 연구를 만나도 절차가 같아야 한다.

필요할 때만 읽는 보조 파일 (`references/`):
- `section-level-rules.md`: 소제목, 문단 순서, 인용 밀도, 캡션.
- `workflow-methods-si-word.md`: Intro, Methods 서술, 검증 그림 위치, SI 번호, Word 버전 관리, 호출 순서.
- `author-comments-2026-10.txt`: 원칙의 출처가 된 사용자 코멘트 원문.
문체 세부는 `paper` 스킬(references/style.md, fluent-english.md), 그림은 `figure_construction`, Word 서식은 `docx-scientific-formatting`.

## 원칙 A. 이름은 역할로 짓고, 쓰기 전에 고정한다

이름은 그 대상이 이 문단의 비교에서 맡는 **역할**(대조 변수의 어느 쪽인가)로 짓는다.
대상을 만든 **조건값**(개수, 크기, 온도, 조성비)이나 **방법**으로 짓지 않는다. 조건값은
그림과 Methods가 들고 있다.

절차:
1. 문단의 대조 변수를 한 단어로 적는다 (예: hydroxylation, nuclearity, solvent).
2. 대조 변수의 각 쪽에 형용사 하나짜리 이름을 준다 (hydroxylated / bare, monomer / dimer /
   trimer, aqueous / vacuum).
3. 한 쪽에 대상이 여럿이면 본문의 비교에 쓰는 대표 하나만 그 이름을 받고, 나머지는
   `the other <name>s`로 묶거나 그림에 넘긴다. 구분이 꼭 필요하면 역할을 더 세분한 형용사
   (fully / partially)를 쓰되, 숫자를 이름에 넣지 않는다.
4. 종(species)은 이름 + 첫 등장 화학식 괄호.
5. 위 표를 적어 두고, 본문에 표에 없는 이름이 나오면 표의 이름으로 바꾼다.

판정 기준: 이름 안에 숫자나 단위가 있으면 조건값 이름이다. 괄호 안에 별명이나 정의가 있으면
새 이름을 꺼낸 것이다. 둘 다 원칙 A 위반.

## 원칙 B. 괄호는 측정값과 화학식만 담는다

괄호는 바로 앞 명사의 값(수치 + 단위), 화학식, 그림 번호를 담는다. 설명, 약칭, 조건, 방법을
괄호에 넣지 않는다. 괄호 안에 쉼표로 두 종류가 섞이면 하나는 밖으로 빼거나 지운다.

## 원칙 C. 첫 문장은 계산 한 단계 위의 질문이다

첫 문장은 "우리가 몰랐던 것"을 말한다. 계산이 아니라 그 계산이 답하는 질문이다.

절차:
1. 이 문단의 결론을 한 줄로 쓴다.
2. 그 결론이 답이 되는 질문을 한 줄로 쓴다. 질문은 **판정**(yes/no, better or not)이 아니라
   **이해**(how, what, which, why)의 형태여야 한다. 판정형이면 한 단계 위로 올린다:
   "hydroxylation이 좋은가" → "hydroxylation이 어떤 step을 어떻게 바꾸는가".
3. 질문을 목적절로, 계산을 주절로 쓴다. **형태는 고정이다: 문단의 첫 단어는 `To`
   (또는 `In order to`)다.** 다른 형태(질문 제시, 미지 서술, 가설 제시, Having established)로
   시작하지 않는다. 다양성은 형태가 아니라 **동사와 질문의 내용**에서 나온다.

   `To <동사> <질문>, we <계산> (Fig. X).`

   동사는 질문의 종류에 맞춰 고른다. 같은 절에서 같은 동사를 연속으로 쓰지 않는다.

| 질문의 종류 | 동사 |
|---|---|
| 원인이나 메커니즘 (why, how) | understand, reveal, clarify, elucidate, rationalize, trace |
| 어느 것인지 (which, what) | identify, locate, pinpoint, isolate, distinguish |
| 변화의 방향과 크기 (how much, how does X change Y) | examine, quantify, resolve, follow, map |
| 경쟁 경로나 가설 사이의 선택 | discriminate between, separate, test (대상은 가설) |
| 앞 결과의 원인을 더 파고듦 | explain, account for, trace the origin of |

   예: `To trace the origin of the stronger acetate binding on the hydroxylated surface, we ...`,
   `To identify which step limits the pathway to acetone, we ...`, `To resolve how surface OH
   changes the C-C coupling barrier, we ...`.

판정 기준: 첫 단어가 To 또는 In order to가 아니면 C 위반. 동사가 judge, assess, determine
whether, evaluate whether, check if처럼 판정을 뜻하면 질문이 판정형인 것이다. 목적절을
"어떻게, 무엇이, 왜"로 다시 쓴다.

## 원칙 D. 비교 문장은 두 값을 모두 쓴다 (2026-10-16 사용자 지시, nanomace 논문 구성)

비교를 말로만 하면 두루뭉실해진다 (`sinks less`, `a similar area`, `within the spread`). 비교
문장은 nanomace 논문(Choung et al., Nat. Commun. 2026)의 형태로 쓴다.

`<모델> exhibited/showed/produced/reached <분석량> of <값>, compared to <값> for <다른 모델> (Fig. X).`

절차:
1. 비교마다 두 값을 다 적는다. 방향만 말하는 문장(`less`, `similar`, `part of`)은 값이 없으면
   쓰지 않는다. 평균이면 `on average`, 시작과 끝이면 `from <값> to <값>`.
2. 값을 빼거나 나눠 만든 2차 수치(차이, 비율)는 쓰지 않는다. 독자가 두 값을 보면 안다.
3. 한 비교에는 한 분석량. 같은 방향을 가리키는 두 번째 분석량은 SI 그림으로 넘긴다.
4. 결과 문장 바로 뒤에 판독 문장을 붙인다 (원칙 J).

## 원칙 E. 절이 Results에 남는 조건은 "결론이 바뀌는가"

문장의 각 절에 묻는다. **이 절을 지우면 문단의 결론이 달라지거나 독자가 결론을 못 믿게
되는가.** 아니면 Methods로 보낸다. 조건값(셀 크기, 층수, 개수, 온도), 생성 절차, 수렴 조건,
seed 수, 기준 상태 정의, 모델 이름과 약어는 거의 항상 "아니오"다.

## 원칙 F. 독자는 이 논문의 Methods를 읽지 않았다

본문의 모든 용어는 해당 저널 독자의 상식이거나, 그 자리에서 독자의 말로 풀려 있어야 한다.
방법 이름(water MD, GA, NEB, umbrella sampling)과 내부 약칭은 상식이 아니다. 꼭 필요하면 한
절로 풀고(`surfaces hydroxylated by adsorbed water`), 필요 없으면 뺀다 (원칙 E).

## 원칙 G. 분석량은 표준 이름 + which 절 하나로 정의한다 (2026-10-16 개정)

분석량을 독자의 말로 풀어 쓰면(`the Pt area open to water`, `how far the Pt atoms move`) 이름이
사라지고 글이 두루뭉실해진다. 표준 이름(accessible surface area, mean-squared displacement,
E_vac)을 쓰고, 처음 나올 때만 which 절 하나로 정의한다. nanomace 논문의 형태:

`Voronoi analysis, which quantifies the effective volume occupied by each atom, revealed the mean
cell volumes of 8.03 Å3 at interface sites, compared to 6.98 Å3 at rod sites.`

값의 읽는 법이 자명하지 않으면(E_vac) 한 문장 추가: `A low E_vac means that CO removes that O
atom at little cost.` 두 번째부터는 이름만 쓴다. 같은 수치를 두 문단에서 반복하지 않는다.

## 원칙 J. 결과 뒤에는 판독 문장을 붙인다 (2026-10-16 사용자 지시)

결과 문장(값 두 개)만 두고 끝내지 않는다. 바로 뒤에 `, indicating that <주장>`,
`, confirming that <주장>`, 또는 `These results indicate that <주장>.`를 붙인다.
`consistent with`는 실험 결과와 잇는 자리에만 쓴다. 주장은 데이터가 직접 보여주는 범위까지만
(원칙 I). 문단의 마지막 문장은 "그래서 무엇"이다.

## 원칙 H. 지칭어 표를 먼저 쓰고, 그 표의 말만 끝까지 쓴다 (2026-10-16 사용자 메모 반영)

쓰기 전에 지칭어 표를 만든다. 층위마다 이름 하나다.
- 촉매 시스템 (셀 전체) = main figure 라벨 (LFPt-Exs, Pt/LFPt). 일반명은 `model surface`.
  `cell`, `system`, `catalyst`, `the two particles`로 바꿔 부르지 않는다.
- 그 안의 금속 입자 = `the Pt NP` (첫 등장 `Pt nanoparticle (NP)`). 두 입자를 구분할 때는 역할
  형용사 + 같은 명사 (`the exsolved Pt NP` / `the loaded Pt NP`). `the particle`, `the embedded one`,
  `the counterpart`는 금지. 독자는 Pt인 줄 모르므로 Pt를 매번 붙인다.
- 상태 서술은 정확한 물리량으로: `embedded`가 아니라 `the lower part of the Pt NP is buried in the oxide
  below the surface plane`.
문장을 쓴 뒤 반성한다: 주어와 동사(행위)가 맞는가 (`the two particles dissociate water`는 틀림, 물은
model surface 위에서 분해된다), 지칭 대상이 표에 있는가. 주어가 방법(`Simulations show`)인 문장을
금지한다. 서술 순서는 패널 a → g 순서를 따르고, 패널을 건너뛰지 않는다.

비유 동사 금지: `start`, `sink`, `anchor`, `ahead`, `open`, `hold in place`. 대신 위치와 이동을
그대로 쓴다 (`is located above the surface plane at 0 ps`, `moves into the oxide`, `moves less`).
Intro에서 `First, Second, Third` 나열은 쓰지 않고 `Furthermore`, `In addition`으로 잇는다.

## 원칙 K. Results 전체는 결론 목록에서 시작한다 (2026-10-21, Mensh & Kording 2017 Rule 1, 4, 7, 9)

문단을 쓰기 전에 Results의 뼈대를 먼저 정한다.
1. 계산 파트가 논문에 보태는 기여를 한 문장으로 적는다. 모든 subsection은 이 문장을 지지해야 한다.
2. subsection마다 결론을 담은 명사구 소제목을 적는다(section-level-rules.md). 목록만 읽어도
   1번 문장까지 논리가 이어져야 한다. 순서는 논리 순서다: 모델과 방법이 믿을 만하다 → 관측 → 원인.
   그림 패널 순서는 이 논리 순서에 맞춰 짠다.
3. 첫 Results 문단은 예외로, 계산 접근법의 요지를 한두 문장으로 준다. 독자 대부분이 Methods를
   읽지 않기 때문이다. 세부 조건값은 여전히 Methods로 보낸다(원칙 E).
4. 한 주제는 한 곳에서만 다룬다. 같은 관측을 두 subsection에서 나눠 말하지 않고, 같은 결론을
   지지하는 두 근거는 바로 이어서 쓴다.

## 원칙 I. 못 지키는 주장은 [CHECK]로 남기지 않고 지운다

데이터가 직접 보여주지 않는 주장은 hedge하거나 [CHECK]를 달지 않고 문장을 지운다. 남기는 노란
표시는 인용 자리 `[ref]`뿐이다. 패널이 없는 수치(예: 6 Å 근처/먼 곳 평균)는 본문에 쓰지 않는다.

## 문장 운용

- 동사는 직접 동사만. `we turned to simulation`, `we posit`, `we sought to`, `we set out to` 같은 간접
  표현 대신 `we performed`, `we computed`, `we followed`로 쓴다 (2026-10-16 사용자 지시).
- 18~25단어로 이어 쓴다. 25단어를 넘는 문장은 스크립트로 세어 쪼갠다. 12단어 미만 단독 문장은 whereas, while, because로 앞에 붙인다.
- 주어는 찾은 대상이다. 방법, 수식, 기호는 주어가 아니다.
- this, it, they, both는 바로 앞 문장의 명사 하나만 가리킬 때 쓴다. 아니면 원칙 A의 이름을
  다시 쓴다.
- 마지막 문장은 "그래서 무엇"을 한 문장으로.

## 출력 전 검사 (원칙 순서대로)

A. 이름에 숫자나 단위가 있는가. 괄호 안에 별명이나 정의가 있는가. 용어표에 없는 이름이 있는가.
B. 괄호에 수치, 화학식, 그림 번호 외의 것이 있는가.
C. 첫 단어가 To 또는 In order to인가. 질문이 판정형인가. 같은 절에서 같은 동사가 연속인가.
D. 값 없이 방향만 말한 비교(`less`, `similar`, `part of`)가 있는가. 2차 수치가 있는가.
J. 결과 문장 뒤에 indicating/confirming 판독 문장이 있는가.
E. 지워도 결론이 안 바뀌는 절이 있는가.
F. 독자가 처음 보는 이름이 설명 없이 있는가.
G. 분석량이 표준 이름으로 불리는가. 첫 등장에 which 절 정의가 있는가. 같은 수치가 두 번 나오는가.
H. 주어가 라벨(LFPt-Exs 등)이 아니라 방법이나 새 지칭어인 문장이 있는가. 패널 순서를 지키는가.
K. 기여 문장 하나가 있는가. 소제목 목록만 읽어도 그 문장까지 이어지는가. 주제만 말하는 소제목이 있는가. 같은 주제가 두 곳에 나오는가.
I. [CHECK], [MECHANISM NEEDED]가 남아 있는가. 있으면 그 문장을 지우거나 데이터로 바꾼다.
