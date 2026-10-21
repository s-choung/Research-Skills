
# fluent-english (예전 fluent_english)

영어 과학 산문 윤문 규칙. 2026-08 ai4mat_neurips2026 4페이지 압축 세션에서 사용자가 문장 단위로 지시한 수정들을 일반화한 것. 저자의 실제 선호가 반영된 규칙이므로 기계적으로 적용해도 안전하다.

## 0. 비유, 의인화, 분야 밖 jargon 금지 (2026-08-31 추가)

과학 산문에서 은유적 표현과 좁은 분야의 jargon을 평이한 서술로 바꾼다. 한국어판
번역 시 직역 비유("사는 곳", "어깨")가 그대로 옮겨지는 것도 이 규칙으로 막는다.

| 전 (비유/jargon) | 후 (평이 서술) |
|---|---|
| the hypervolume drawn where it lives | the hypervolume drawn on the plane where it is defined |
| conquers the corner | reaches the best-Z region |
| pushes the high-TOF shoulder highest | raises the high-TOF section of the front the most |
| the baselines split the job | each baseline does well on only one of the two scores |
| assembled from lucky singles | comes from isolated chance picks |
| arm (bandit 용어를 일반 비교에 사용) | method / condition (문맥에 맞게) |
| X and Y are different jobs | X and Y require different behavior |
| My work sits between A and B | 삭제하거나, 사람이 하는 행위로 재작성 (I study A and build B) |
| lies at the intersection of A and B | combines A and B / uses A to do B |
| bridges the gap between A and B | connects A and B (구체 행위로) 또는 삭제 |

특히 "work/research/approach"를 주어로 세워 공간에 배치하는 LLM 자기서술 패턴
(sits between, lies at, spans, bridges, is positioned at)은 CV, profile, 자기소개
산문에서 거의 항상 요약 반복이므로 1순위 삭제 후보. 남겨야 하면 사람(I)을
주어로 하고 실제 행위 동사(study, build, measure)로 다시 쓴다.

판단 기준: 그 표현을 처음 보는 독자가 그림이나 수식 없이 뜻을 복원할 수 있는가.
없으면 평이 서술로 바꾼다. 정착된 표준 용어(Pareto front, hypervolume, surrogate)는
유지한다.

## 1. 콜론/세미콜론 연결문 금지 (최우선)

본문 산문에서 `:` 와 `;` 로 절을 이어붙이지 말 것. 완전한 문장으로 풀어라.

| 패턴 | 수정 |
|---|---|
| `two conditions: vanilla, and skill` | `a vanilla condition and a skill condition` |
| `recurring steps: building X, computing Y` | `the recurring steps of building X and computing Y` |
| `not uniformly positive, however: gpt drops...` | `not uniformly positive, however. With the skill, gpt drops...` |
| `can coexist with accuracy: model reaches 76%` | `can coexist with accuracy, as model reaches 76%` |
| `A holds; B follows` | `A holds, so B follows` 또는 두 문장으로 분리 |
| `Thermodynamic metrics per pathway: highest X and largest Y` (캡션) | `Per-pathway thermodynamic metrics, comparing the highest X and the largest Y` |
| `is the route (pathway 1): on the surface an enolate attacks...` | `is the route (pathway 1), in which an enolate ... attacks...` |
| `activated in three ways: A, B, or C` | `activated by A, by B, or by C` (전치사 반복으로 해체) |
| `Request 1 (...): complete, at three levels` (상태 목록) | `Request 1 (...) is complete at three levels` |
| `Structures of pathway 2 (relax): X → Y → Z` (캡션 시퀀스) | `Structures of pathway 2, in the order X → Y → Z.` |

**예외**: 괄호 안 그림/표 참조의 세미콜론은 관례라 유지 — `(Fig. 1; Table S1)` OK.
**제목/헤딩의 콜론도 해체**: `Conclusions: comparison with X` → `Conclusions and comparison with X`.
한국어판도 동일 (2026-09 추가): `요약입니다: ...` → `기준으로는 ...`, `판정입니다: A는 B다` →
`A는 B라고 판정합니다`, `방법입니다: ...` → 주어를 세워 `NEB는 ...합니다`, `결론: X와 비교` → `결론 및 X와 비교`.

## 2. 괄호 참조는 참조만

괄호 안에 설명을 넣지 말고 레퍼런스만 남긴다.

- `(vertical bars in Fig. 2; per-model detail in Fig. S2)` → `(Figs. 2 and S2)`
- `(levels in Table S2; full prompts in Tables S3 and S4)` → `(Tables S2, S3, and S4)`
- `(rendered structures in Fig. S5; worked examples in Fig. S6)` → `(Figs. S5 and S6)`
- `(Fig. 1; per-model scores in Table S1)` → `(Fig. 1; Table S1)`

"vertical bars in", "per-model detail in", "labelled points are" 같은 시각 요소 묘사는 독자가 그림에서 스스로 보게 두고 지운다.

## 3. 캡션은 뼈대만

캡션에서 그림을 다시 설명하는 꼬리절을 자른다.

- `..., log scale; labelled points are Pareto-optimal or reference models.` → `..., log scale.`
- 조건 정의가 본문/다른 캡션에 이미 있으면 반복하지 않는다: `without (Vanilla) and with (Skill) the ASE skill` 반복 → 두 번째 캡션에선 삭제.

## 4. 군더더기 수치와 나열 삭제

- 같은 정보의 이중 표기 금지: `$0.025 over all 50 tasks, about $0.0005 per task` → `about $0.0005 per task` (하나만 남긴다).
- 주장에 필수적이지 않은 보조 수치 나열은 삭제 후보: `and the next eight models cluster between 20% and 47%`, `and it is negative for A (−3) and B (−4)`.
- 나열이 3개 이상이고 "such as"로 시작 가능하면 2개로 줄인다: `including wrong space groups, wrong terminations, and wrong reference states` → `such as wrong space groups and terminations`.

## 5. 문장 압축 원칙

- 부연 형용사/부사 삭제: `already handle most easy simulation tasks` → `handle most easy tasks`; `released publicly upon publication` → `released upon publication`.
- 판단성 수식어구(`but appear within reach of upcoming releases`)는 주장 유지에 필요 없으면 삭제.
- 2줄(원고 기준) 넘는 문장은 분할 후보.
- 관계절 중첩(`knowledge the frontier already holds`)이 모호하면 능동 구문으로 재작성: `The skill file supplies ASE documentation that frontier models already know, so it cannot repair the remaining failures`.

## 6. 적용 절차

1. `grep -n "; \|: "` 로 대상 파일의 콜론/세미콜론 전수 조사 (라벨, 캡션, 코드, URL 제외).
2. 규칙 1~5 순서로 적용. 숫자, 인용 마커, 화학식, 기술적 주장은 절대 변경 금지.
3. 수정 후 반드시 재컴파일/렌더 확인.
4. 과학 산문이면 references/style.md의 banned words 검사도 병행.
