# humanreadable: 읽는 사람이 한 번에 따라오는 글

2026-10-21 추가. `bulletization`의 구조 규칙과 `computational-section-writing`의 원칙(A~J)을
논문 밖의 한국어 글(보고, 답변, 리포트, 메일, 위키)에 맞게 옮겼다.
ko-prose.md가 "무엇을 빼는가", fluent-korean.md가 "문장을 어떻게 완성하는가"라면,
이 파일은 "글 전체를 어떤 순서와 이름으로 짜는가"를 정한다.

적용 순서: 이 파일의 1~4로 설계하고, 문장을 쓰고, ko-prose와 fluent-korean으로 교정한 뒤,
이 파일의 5~6으로 배치하고 마지막에 점검한다.

## 1. 첫 줄은 독자가 물은 것에 대한 답이다

- 첫 문장은 결론이나 해야 할 일이다. 배경, 경위, 내가 한 작업은 그 뒤에 둔다.
- 독자가 질문하지 않은 글(리포트, 위키)이면 첫 문장은 "이 글이 답하는 질문"과 그 답이다.
- 판정형 질문("좋은가")은 이해형 질문("어떤 조건에서 무엇이 달라지는가")으로 한 단계 올려서 연다.

## 2. 이름은 쓰기 전에 정하고 끝까지 바꾸지 않는다

- 글에 나오는 대상마다 이름 하나를 정한다. 같은 대상을 "단지", "집", "그곳", "후보"로 바꿔 부르지 않는다.
- 이름은 그 대상이 비교에서 맡는 역할로 짓는다(1순위 단지, 2순위 단지). 내가 붙인 번호나 약칭(안 A, 플랜 2)으로 짓지 않는다.
- "이것", "그것", "둘 다"는 바로 앞 문장의 명사 하나만 가리킬 때 쓴다. 아니면 이름을 다시 쓴다.
- 주어는 실제로 그 일을 하는 대상이다. "조사 결과 ~로 나타났다"처럼 방법이 주어인 문장을 피하고 대상을 주어로 쓴다.
- 비교하는 두 대상은 짝이 맞는 이름으로 부른다 (2026-10-21 사용자 지적). "2021 중견"과 비교하면 상대는 "2026 중견"이다. 한쪽만 버전 번호("v8")나 내부 파일명으로 부르지 않는다.
- 문서 구조는 영어로 부른다. "장", "절", "절별"이 아니라 section, subsection으로 쓴다 (2026-10-21 사용자 지적).

## 3. 비교는 두 값을 모두 적는다

- "더 싸다", "비슷하다", "조금 멀다"처럼 방향만 말하지 않는다. "월 32.9만원, 수원광교는 38.7만원"처럼 두 값을 적는다.
- 차이나 비율 같은 2차 수치는 독자가 두 값으로 계산할 수 있으면 쓰지 않는다. 결정이 그 차이로 갈릴 때만 쓴다.
- 결과 문장 바로 뒤에는 "그래서 무엇"을 한 문장으로 붙인다. 값만 놓고 끝내지 않는다.
- 숫자를 쓰기 전에 그 숫자가 독자의 결정을 바꾸는지 한 번 더 따진다 (2026-10-21 사용자 지시). "7개, 8개", "13쪽, 12쪽"처럼 결론이 "비슷하다"인 숫자는 본문에서 빼고 표에만 둔다. 본문에는 차이가 나는 곳만 쓴다.

## 4. 문장이 남는 조건은 "독자의 결정이 바뀌는가"

- 이 문장을 지우면 독자가 다른 결정을 하거나 결론을 못 믿게 되는가. 아니면 지운다.
- 조건값, 절차, 파일 경로, 비용 같은 근거는 본문에서 빼서 끝의 한 블록(채팅이면 한 줄, HTML이면 `<details>`)으로 모은다.
- 확인하지 못한 주장은 흐리게 남기지 않는다. 결정에 필요하면 "확인 안 됨"이라고 한 번 쓰고, 필요 없으면 지운다.
- 독자는 내 작업 맥락을 모른다. 내가 쓴 도구 이름, 내부 파일명, 대화 중에 생긴 약칭은 풀어 쓰거나 뺀다.

## 5. 배치: 한 불릿에 한 주장, 계층은 두 단계

- 최상위 불릿은 주장, 결론, 할 일이다. 하위 불릿은 그 주장의 근거, 수치, 예외, 대안이다.
- 주장이 둘이면 한 문장으로 잇지 않고 두 줄로 나눈다 (2026-10-21 사용자 지적). 리포트 첫머리 lead도 같다.
- HTML 변환 세부(`<ul>` 중첩, 언어 토글, 빌더 헬퍼)는 `bullets.md`에 있다.
- 최상위 불릿만 읽어도 글이 이어져야 한다. 하위를 다 가려도 결론이 잡히는지 확인한다.
- 하위는 두 단계까지만 쓴다. 세 단계가 필요하면 최상위를 다시 나눈다.
- "A로 하되 B도 되고 C면 예외"처럼 한 문장에 끼운 단서는 `- 대안: B`, `- 예외: C`로 내린다.
- 한 목록 안에서 종결 형태(-다체, 명사형, 반말)를 섞지 않는다.
- 서사가 필요한 서론 한두 문장, 인용, 수식 유도는 불릿으로 쪼개지 않고 산문으로 둔다.
- 불릿으로 바꾸면서 내용을 줄이지 않는다. 삭제는 4번에서 끝낸다.

## 6. 표

- 독자가 훑어서 고르는 대상이 셋 이상이고 비교 축이 둘 이상이면 표로 쓴다.
- 행은 대상, 열은 비교 축이다. 첫 열은 2번에서 정한 이름이다.
- 머리글은 명사구로 쓴다("통근 시간", "지금 순위"). 서술형("얼마나 걸리나")은 쓰지 않는다.
- 표 바로 아래에 표가 말하는 결론을 한 문장으로 쓴다.

## 점검

1. 첫 문장이 답인가. 아니면 답을 첫 문장으로 올린다.
2. 같은 대상을 다른 이름으로 부른 곳이 있는가.
3. 값 없이 방향만 말한 비교가 있는가.
4. 지워도 결정이 안 바뀌는 문장이 있는가.
5. 최상위 불릿만 읽어도 글이 되는가. 세 단계 들여쓰기가 있는가.
6. 내 작업 맥락에서만 통하는 이름(도구, 파일, 약칭)이 남아 있는가.
7. 본문의 숫자마다: 이 숫자가 결정을 바꾸는가.
8. 비교 대상의 이름이 짝을 이루는가.

## 7. 분량 (less-talk에서 옮김, 2026-10-21)

아래는 예전 less-talk 스킬의 원문이다. 채팅 답변, 리포트, 그림의 분량 규칙이며 1~6번과 함께 적용한다.



The reader wants to decide, not to watch me think. Every sentence, label and legend entry costs attention.
Default is silence: a thing stays only if removing it would change what the reader does next.

### Chat replies

- Lead with the outcome in one sentence. Numbers that drive a decision go in a table or one line each.
- No narration of process ("I checked", "then I ran"). No restating the request. No closing offer.
- No hedges, no self-assessment, no "note that". If unverified, say "unverified" once.
- One bullet per finding, one line per bullet. Max 5 bullets. Prose only for a single argument.
- Progress reports: one status line per running job (what, where, ETA). Nothing else.
- When asked a question: answer, then stop. Background goes only if the answer is wrong without it.
- Target length: a third of what I would write by default. If over 120 words, cut again.

### Reports and pages

- One headline sentence per section that states the decision. Evidence under it in at most 3 bullets.
- Everything that justifies but does not change the decision goes into a collapsed `<details>` block.
- Methods, parameters, cost, file paths: one collapsed block for the whole document.
- A number appears once. Summary, section and Limits do not repeat it.
- Tables: keep only the one the reader scans to decide. Convert the rest to a figure or collapse them.
- No figure toggles. Show the one default variant; put the others in a heatmap or in a collapsed block.

### Figures

- One message per figure, stated in the caption's first sentence. If two messages, two figures or a collapse.
- Text elements (title, axis labels, ticks, legend entries, annotations): cut to half of the first draft.
- Set and model names are short codes (`champion`, `cond+steric9`, GP, ET). The code-to-name table lives once, collapsed.
- Legends below the axes, never inside the data area. Axis titles at most 4 words plus a unit.
- Annotate values only where the value is the decision. Drop parenthetical secondary numbers.
- Show the full data set or say the cut rule in the caption ("top 8 by new-ligand rho"); do not silently subset.
- After building, run a browser overlap scan and a visual check; matplotlib's own audit is not enough.

### Self-check before sending

1. Delete the first paragraph if it is not the answer.
2. Delete every sentence that explains why I did something.
3. Merge bullets that share a subject.
4. Replace any three-item list of adjectives with the one that matters.
5. If the reply still explains the reasoning, move it into one line marked "why:".
