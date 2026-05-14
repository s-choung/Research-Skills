# Reference Guide: Human Writing Principles

SKILL.md의 규칙으로 판단이 어려울 때 참조한다. 원문 12-level 프롬프트의 핵심 원칙만 압축한 것.

---

## Banned Vocabulary (English)

무조건 제거 또는 교체:

delve, tapestry, nuanced, multifaceted, pivotal, robust, foster, enhance, leverage (동사), navigate (비유적), underscore, serves as, holistic, comprehensive, empower, impactful, innovative, transformative, groundbreaking, revolutionary

기계적 전환어 (대부분 삭제, 실제 논리 관계로 교체):
furthermore, moreover, additionally, it is worth noting, not just X but also Y

빈 강조어 (증거 없이 쓰일 때):
crucial, vital, paramount, essential, critical

AI 도입/종결 표현 (전부 삭제):
absolutely, certainly, great question, I hope this helps, feel free to ask, moving forward, going forward, at this juncture, in conclusion, key takeaways

## Inflated Phrases → Plain Replacements

- due to the fact that → because
- has the ability to → can
- in order to → to
- in the event that → if
- with regard to → about
- is in the process of → (직접 동사)
- make a decision → decide
- conduct an investigation → investigate
- provide assistance to → help
- in spite of the fact that → although
- for the purpose of → to

## Sentence Diagnostics

세 가지 테스트를 순서대로:

1. **행위자 테스트**: 누가 무엇을 하는가? 수동태("improvements were made")면 능동태로.
2. **사건 테스트**: 구체적으로 무엇이 일어났는가? 범주("faced challenges")면 사건으로.
3. **삭제 테스트**: 이 문장을 빼도 단락이 성립하는가? 성립하면 삭제.

세 테스트 모두 실패하면 → 가장 순수한 AI 필러. 정보를 만들어서 채우지 말고 삭제하거나 빈 자리를 남긴다.

## Paragraph Repair vs. Replacement

단락 내 절반 이상의 문장이 세 테스트를 모두 실패하면 → 문장을 고치지 말고 단락을 교체한다. 단락이 말하려던 주장을 한 문장으로 쓰고 거기서부터 새로 쓴다.

문서 내 절반 이상의 단락이 교체 대상이면 → 문서 전체를 다시 쓴다. 원문은 참고자료.

## Opening Patterns

AI 도입부의 공통 실패: "이 글에서는 ~을 살펴보겠습니다", "X는 현대 사회에서 중요한 주제입니다."

테스트: 이 문장이 같은 주제의 아무 글에나 쓰일 수 있는가? → AI 도입부. 교체.

작동하는 도입부 유형:
- 구체적 장면 (날짜, 장소, 사람)
- 모순 (두 사실이 충돌)
- 프레임을 깨는 사실
- 직접 주장 (틀릴 수 있는 문장)

보고서/제안서: 발견→방법론 순서. "이 보고서는 ~를 분석합니다"가 아니라 "이탈률이 40% 증가했다. 원인은 가격이 아니라 온보딩이다."

## Second Paragraph Rule

강한 도입부 뒤에 맥락/배경으로 후퇴하는 것이 AI의 가장 일관된 구조 패턴. 두 번째 단락은 도입부의 주장을 전진시켜야 한다. 맥락은 세 번째 이후에.

## Counter-Arguments

AI 패턴: "일부는 X라고 주장한다. 그러나 Y도 중요하다. 양쪽 모두 일리가 있다."

올바른 방식: 가장 강한 반론을 가장 강한 형태로 제시 → 구체적 증거로 응답 → 증거가 해결하지 못하는 부분을 명시. 결론은 원래 주장보다 약해져야 한다 — 약해진 만큼 정직해진 것.

## Register Modulation

같은 내용을 전문가/일반인/당사자에게 쓸 때 달라져야 하는 것:
- 전문가: 용어를 정의 없이 사용, 맥락 생략
- 일반인: 용어를 설명, 불확실성을 명시
- 당사자: "you"를 사용, 추상적 결정을 개인적 결과로 번역

독자가 명시되지 않았으면 텍스트에서 추론한다 (정의 없이 쓰인 용어, 설명 없이 전제된 결과, 대명사 패턴).

## Pacing

AI 문서는 모든 부분에 동일한 깊이를 준다. 인간 글쓰기는 가속과 감속이 있다.

- 가장 중요한 지점에서 느려진다 (더 긴 단락, 더 많은 증거)
- 명확한 결론은 짧게 도착한다
- 중요한 것을 말한 직후 짧은 문장으로 멈춘다

## Adversarial Self-Check

최종 점검 질문:

1. 문서에서 가장 약한 주장은? 증거가 충분한가?
2. 가장 많은 무게를 지는 예시는? 실제로 주장을 뒷받침하는가?
3. 가장 무거운 전환은? 논리적 비약을 숨기고 있지 않은가?
4. 가장 확신에 찬 부분은? 적대적 독자가 뭘 가져올 수 있는가?
5. 첫 문장과 마지막 문장만 읽었을 때 같은 논점에 속하는가?

## Certainty Gradient

- 직접 관찰에 기반 → 직접 진술
- 추론에 기반 → 추론 과정을 보여줌
- 불완전한 정보에 기반 → 부족한 정보를 명시
- 논쟁 중 → 알려진 것, 논쟁인 것, 이유를 각각 명시

"모르겠다"는 가장 인간적인 문장 중 하나이고, AI 출력에서 가장 드문 문장 중 하나다.
