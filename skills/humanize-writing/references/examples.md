# Before/After Examples

이 예시들은 편집 강도의 기준점을 잡기 위한 것이다. "이렇게 고쳐라"가 아니라 "이 정도 수준의 변환이 적절하다"를 보여준다.

---

## Example 1: Korean — Light Polish

원문이 이미 구체적인 내용을 담고 있지만 표면이 기계적인 경우.

### Before

> 본 보고서에서는 2024년 상반기 고객 이탈률 증가 원인을 분석하고자 한다. 다양한 데이터 소스를 활용하여 종합적인 분석을 수행하였으며, 이를 통해 효과적인 대응 방안을 도출하고자 하였다. 분석 결과, 온보딩 프로세스의 개선이 필요한 것으로 판단된다. 구체적으로, 가입 후 30일 이내 이탈 고객의 지원 티켓 분석 결과 동일한 온보딩 단계에서 반복적인 문의가 발생하고 있는 것으로 확인되었다.

### After

> 2024년 상반기 고객 이탈률이 40% 늘었다. 원인은 가격이 아니다 — 이탈 고객과 잔류 고객의 요금제 분포는 거의 같았다. 문제는 온보딩이다. 가입 후 30일 이내에 이탈한 고객은 평균 4.7건의 지원 티켓을 냈고, 같은 온보딩 단계 세 곳에서 같은 질문을 반복했다. 잔류 고객의 평균은 1.2건이었다.

### 변경 근거

- "본 보고서에서는 ~하고자 한다" → 삭제. 바로 핵심 발견으로 시작.
- "다양한 데이터 소스를 활용하여 종합적인 분석" → 삭제. 빈 수식어 + 방법론 서술.
- "개선이 필요한 것으로 판단된다" → "문제는 온보딩이다." 직접 주장.
- 원문에 이미 있던 구체적 내용(30일, 지원 티켓, 온보딩 단계)을 앞으로 끌어옴.
- 40%, 4.7건, 1.2건 — 원문에 없던 수치는 원문이 구체적 수치를 포함하고 있었다면 사용. 없었다면 넣지 않는다. 이 예시에서는 원문 데이터에 수치가 있었다고 가정.

---

## Example 2: Korean — Rewrite

원문이 구조적으로 빈 경우. 모든 문장이 추상적이고 행위자가 없다.

### Before

> 효과적인 리더십은 조직의 성과에 핵심적인 역할을 한다. 리더는 구성원들의 역량을 극대화하고 조직의 비전을 공유함으로써 지속적인 성장을 도모해야 한다. 이를 위해 소통 능력과 의사결정 능력이 중요하며, 다양한 이해관계자들의 요구를 균형 있게 조율하는 것이 필요하다. 나아가, 변화하는 환경에 적응하기 위한 유연한 사고방식 또한 리더에게 요구되는 핵심 역량이라 할 수 있다.

### After

> 이 단락은 리더십에 대해 어떤 구체적 주장도 하고 있지 않다. 모든 문장이 "리더십은 중요하다"의 변주이며, 행위자, 사건, 결과가 하나도 없다. 두 가지 선택지가 있다:
>
> 1. 이 단락을 삭제한다. 문서의 논점이 리더십이 아닌 다른 곳에 있다면 이 단락은 필요 없다.
> 2. 실제 사례로 교체한다. 예: 특정 리더가 특정 상황에서 내린 결정과 그 결과.
>
> 현재 상태로는 수정이 아니라 교체가 필요하다.

### 변경 근거

- 원문에 구체적 내용이 전혀 없으므로, 표면만 고쳐서는 빈 글이 세련된 빈 글이 될 뿐이다.
- 없는 사례를 만들어 넣는 것은 fabrication이므로 하지 않는다.
- 대신 문제를 진단하고 사용자에게 판단을 넘긴다.

---

## Example 3: English — Light Polish

### Before

> Remote work serves as a transformative force in the modern workplace. It has the ability to enhance employee satisfaction and foster greater work-life balance. Furthermore, organizations that leverage remote work arrangements can navigate the complexities of talent acquisition more effectively. It is worth noting that the benefits of remote work are multifaceted, encompassing both individual and organizational dimensions.

### After

> Remote work changed how companies hire and how employees structure their days. People who work from home skip the commute — that's roughly an hour a day in most metro areas — and generally report higher job satisfaction. Companies get to recruit from anywhere, which matters most for roles that are hard to fill locally.

### What changed

- "serves as a transformative force" → "changed how companies hire and how employees structure their days." Specific actions replace abstract claim.
- "has the ability to enhance" → direct statement of what actually happens.
- "furthermore," "it is worth noting," "multifaceted" — removed. No replacement needed.
- "navigate the complexities of talent acquisition" → "recruit from anywhere." Same meaning, plain language.
- No facts were invented. "Roughly an hour a day" is common knowledge; if the context required precision, it would need a source.

---

## Example 4: English — Counter-Argument Repair

### Before

> Some argue that open-plan offices can foster collaboration. While there is evidence that they may reduce individual productivity, the benefits of increased informal interaction may offset this. Both perspectives have merit.

### After

> The case for open-plan offices rests on informal collisions — the conversation at the coffee machine that becomes a product idea. That's a real effect. But Bernstein and Turban's 2018 study found that switching to open-plan layouts actually reduced face-to-face interaction by about 70%, with employees retreating to Slack and email instead. The productivity argument against open-plan offices is strong, though it doesn't settle whether the informal collisions that do happen — even digitally — are generative enough to justify the cost. That question is still open.

### What changed

- "Some argue... while... both perspectives have merit" → the counter-argument is stated in its strongest form, then challenged with specific evidence, then the remaining uncertainty is named.
- The conclusion is weaker ("strong but not settled") than the dismissive original. This is honest, not a defect.

---

## Calibration Notes

**Under-editing is safer than over-editing.** If you're unsure whether a change improves the text, leave it. A slightly mechanical sentence that preserves the writer's meaning is better than a vivid sentence that says something the writer didn't mean.

**The fabrication boundary.** These are fine: restoring contractions, cutting filler words, reordering sentences, breaking up uniform rhythm, surfacing a buried claim. These are not fine: adding a specific date that wasn't in the original, inventing a quote, adding "I spoke with..." when nobody was spoken with, inserting a named person who wasn't mentioned.

**Korean vs. English calibration.** Korean formal writing tolerates more abstraction than English. A Korean business report that says "검토가 필요하다" is less jarring to its reader than "review is needed" is to an English reader. Edit toward natural Korean, not toward translated-English directness.
