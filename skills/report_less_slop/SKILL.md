---
name: report_less_slop
description: 결과나 자료를 읽는 사람이 바로 결정할 수 있는 단일 파일 한국어 HTML 리포트로 만든다. 상단 nav, 큰 제목과 한 줄씩 끊은 lead, 요약 박스, 색으로 칠한 핵심 표 하나, 대조표, 접힌 부록으로 된 고정 레이아웃(templates/build_minimal.py)에, AI체와 군더더기를 빼는 글쓰기 규칙(writing/)과 정적 검사(templates/check_html.py)를 한 폴더에 묶었다. report, ko-writing, design2html 스킬을 공유용으로 합친 자급자족 버전. Triggers - report_less_slop, 리포트 만들어, html 리포트, 결과 정리 리포트, 비교 리포트, less slop, 군더더기 없는 리포트, 읽기 쉬운 리포트.
---

# report_less_slop

이 폴더 하나로 리포트를 만든다. 다른 스킬이 없어도 된다.

| 파일 | 역할 |
|---|---|
| `templates/build_minimal.py` | 레이아웃 고정 빌더. 상수(LEAD, SUMMARY, KING, CMP_ROWS, BODY)만 고친다 |
| `templates/build_report_example.py` | STYLE 원본과 그림 토글, svg 인라인까지 쓰는 큰 예제 |
| `templates/check_html.py` | 정적 검사 (가운뎃점, 엠대시, keep-all, 외부 리소스, 제목 형태, 금지어) |
| `templates/pw_check.py` | Playwright 검사 (가로 스크롤, 폰트, 이미지, JS 에러) |
| `templates/fig_common.py` | matplotlib 그림 공통 설정과 겹침 검사 |
| `writing/humanreadable.md` | 설계 규칙: 결론 먼저, 이름 고정, 두 값 비교, 숫자 중요도, 분량 |
| `writing/ko-prose.md` | 삭제 규칙: 자평, 직역, 비유, 3개 나열, 가운뎃점, 줄표, 부연 (MIT, `writing/LICENSE`) |
| `writing/fluent-korean-not-coding.md` | 완결 문장 규칙: 조사와 어미, 전보문 금지 |
| `writing/domain-terms.md` | 억지 번역어와 어려운 한자어 사전 |
| `redundancy-remove.md` | 결과를 추가한 뒤 밀려난 중복 절을 걷어내는 절차 |

## 완성 모습

- 상단 nav: 왼쪽에 프로젝트와 주제, 오른쪽에 날짜.
- hero: 큰 제목(명사구) 아래 lead. **주장 하나에 한 줄**이고, 주장이 둘이면 두 줄로 나눈다.
- 요약: 회색 박스 안 계층 불릿. 최상위만 읽어도 결론이 이어진다. 그 아래 핵심 표 하나(수치 셀은 색으로 칠함)와 캡션.
- 본문 section: 제목(명사구) + 결론 한 문장 + 표나 그림 하나.
- 부록: 직접 비교하지 않는 대상, 원자료, 집계 방법은 전부 `<details>`로 접는다.
- 끝줄 footer: 원자료 경로와 비용 한 줄.

## 절차

1. **질문과 결론을 먼저 쓴다.** 독자가 이 리포트로 무엇을 정하는지 한 줄, 그 답 한 줄. 이 두 줄이 hero lead가 된다.
2. **비교 대상의 이름을 정한다.** 짝을 맞춘다("2021안"과 "2026안"). 한쪽만 버전 번호나 파일명으로 부르지 않는다. 이후 끝까지 이 이름만 쓴다.
3. **숫자를 전부 뽑고, 하나씩 묻는다: 이 숫자가 결정을 바꾸는가.** 바꾸면 본문, "비슷하다"가 결론이면 표에만 둔다. 손으로 옮긴 숫자는 원자료에서 다시 계산해 확인한다. 확인 안 된 주장은 지운다.
4. **`templates/build_minimal.py`를 복사해 상수를 채운다.** section 하나는 제목, 결론 한 문장, 불릿 3개 이하, 펼친 표 1개 이하. 나머지는 `details()`로 접는다.
5. **빌드하고 검사한다.** `python build_minimal.py out.html` 뒤 `python check_html.py out.html`. 가운뎃점, 엠대시, 외부 리소스가 0이고 keep-all이 있어야 한다. 가능하면 `pw_check.py`로 가로 스크롤 0을 확인한다.
6. **문체를 점검한다.** `writing/humanreadable.md`의 점검 8개와 `writing/ko-prose.md`의 빠른 점검을 돈다. 입니다체로 통일한다.
7. 기존 리포트에 결과를 추가했으면 `redundancy-remove.md`로 밀려난 절을 걷어낸다.

## 하드 규칙 (어기면 다시 만든다)

**글**
- 첫 문장은 답이다. 배경과 경위는 뒤나 부록으로.
- 주장이 둘이면 두 줄. 한 불릿에 주장 하나. 계층은 두 단계까지.
- 비교는 두 값을 다 적는다("12분, B안은 7분"). 방향만 말하지 않는다. 차이나 비율 같은 2차 수치는 쓰지 않는다.
- 결정을 바꾸지 않는 문장과 숫자는 지운다.
- 자평 수식어(핵심, 흥미로운, 중요한), 비유와 은유, 영어 직역, 가운뎃점(·), 엠대시(—), 물결표 자리 표시를 쓰지 않는다.
- 제목과 표 머리글은 명사구. 질문형과 서술형("무엇이 바뀌나")은 쓰지 않는다. 문서 구조는 section, subsection으로 부른다("장", "절" 금지).
- 내가 만든 약칭(안 A/B, ①/②)과 내부 파일명은 풀어 쓰거나 뺀다.
- 분야에서 영어로 부르는 용어는 영어로 쓴다(`writing/domain-terms.md`).

**레이아웃**
- 외부 리소스 0 (폰트는 base64 내장). 단일 HTML 파일.
- `body`에 `word-break:keep-all; line-break:strict; overflow-wrap:break-word`.
- 방향성 border 강조(border-left 등) 금지. 강조는 배경 틴트나 색 글자.
- 표: 첫 열(라벨)은 왼쪽, 나머지는 가운데, 머리글과 셀 정렬을 맞춘다. 수치 열은 셀 배경색으로 크기를 보인다.
- 펼친 표는 section당 1개. 나머지는 접는다.
- 글자 크기 13.5px 이상, 회색 글씨는 #555보다 연하지 않게.
- 캡션은 그림이나 표에 무엇이 있는지와 읽는 법만. 수치와 해석은 본문에.

## 하지 말 것

- 대상 넷을 카드로 가로로 늘어놓기. 비교 대상이 둘이면 한 표에 나란히 놓고, 나머지는 접는다.
- 같은 숫자를 요약, 본문, 부록에 반복하기.
- 검사를 통과하지 않은 상태로 완성이라고 말하기.
