---
name: paper
description: 영어 과학 논문 글쓰기의 단일 진입점. (1) 자연어 요청을 plan / ref / draft / critic / humanize로 분류해 해당 subagent로 보내는 router, (2) 저자 문체 프로필과 압축 규칙(references/style.md), 영어 산문 다듬기(references/fluent-english.md), IMRAD 섹션과 인용 포맷(references/sections.md)을 담는다. 예전 paper-style, fluent_english, paper-sections 스킬과 /paper 커맨드를 2026-10-21 합쳤다. Triggers - /paper, paper style, 저자 문체, style profile, 논문 스타일, 논문 humanize, AI 흔적 제거, paper humanize, 장황, 두루뭉실, 문장 줄여, tighten, fluent english, 영어 산문 다듬기, 콜론 세미콜론, 캡션 축약, paper draft, IMRAD, introduction draft, results 작성, discussion 섹션, 섹션 초안, manuscript section, citation format, 인용 포맷, bibliography, superscript citation.
argument-hint: "<what you want in natural language>"
allowed-tools: Read, Edit, Grep, Glob, Write, Task
---

# paper: 영어 논문 글쓰기

규칙 본문은 `references/`에 있고, 이 파일은 어떤 파일을 언제 읽는지와 router 절차만 정한다.
원본 스킬은 `~/.archive/2026-10-21/skills-merge/`에 있다.

| 파일 | 내용 | 읽는 때 |
|---|---|---|
| `references/style.md` | STYLE_PROFILE 로딩(Mode 1), 문단 압축(Mode 2), 가벼운 AI체 정리(Mode 3) | 원고 문단을 쓰거나 고칠 때 항상 |
| `references/fluent-english.md` | 콜론과 세미콜론 연결문 해체, 괄호 참조 단순화, 캡션 축약, 군더더기 절 삭제 | .tex/.md 영어 산문을 다듬거나 압축할 때 style.md와 함께 |
| `references/sections.md` | IMRAD 섹션별 템플릿, 숫자 위첨자 인용 포맷 | 특정 섹션을 새로 쓰거나 인용을 넣을 때 |

계산 파트(MD, DFT, MLIP)의 Results와 Methods는 별도 스킬 `computational-section-writing`을 쓴다.
한국어 글에는 이 스킬을 쓰지 않는다 (`ko-writing`).

## 직접 적용 (사용자가 문단을 주고 다듬어 달라고 할 때)

1. `references/style.md`를 읽고 Mode를 고른다. 압축은 Mode 2, 마지막 정리는 Mode 3.
2. 문장 단위 교정은 `references/fluent-english.md`를 함께 적용한다.
3. 섹션 구조를 바꾸는 요청이면 `references/sections.md`의 해당 섹션 템플릿을 따른다.

## Router (`/paper <자연어>`)

`/paper`로 부르면 요청을 분류해 subagent로 보낸다. router는 글을 직접 쓰지 않는다.
먼저 확인할 것: 작업 폴더의 `Manuscript_*.docx`, `Supporting_Information*.docx`,
`.claude/paper-team/project-context.md`, `~/.claude/paper-team/STYLE_PROFILE.md` 존재 여부.

### 의도 분류

키워드와 의미로 맞춘다. 애매하면 질문 하나만 하고 멈춘다.

1. **PLAN**: 계획, 플랜, 뭐부터, 순서, 로드맵 / plan, roadmap, where to start
   - main context에서 3~7단계 번호 계획과 첫 명령을 낸다. subagent 없음.
     (예전에는 writing-plans 스킬을 불렀지만 그 스킬은 은퇴했다.)
2. **REF**: 인용, 레퍼런스, 논문 찾, 참고문헌, 관련 논문 / reference, citation, prior work
   - `paper-ref-hunter` subagent, query는 요청에서 라우팅 키워드를 뺀 말.
3. **DRAFT**: 써줘, 초안, 작성, 문단, 섹션, intro 써, results 써 / draft, write, new section
   - `paper-section-drafter` subagent. 대상 섹션이 불분명하면 "어떤 섹션?" 하나만 묻는다.
4. **CRITIC**: 검증, 크리틱, 체크, 논리, 과장, 근거, 리뷰어 / critique, review, rigor
   - `paper-scientific-critic` subagent.
5. **HUMANIZE**: 다듬, 휴머나이즈, AI 티, 스타일, 문체, 깔끔하게 / humanize, polish, style
   - `paper-style-enforcer` subagent, `fix` mode.

### 실행 규칙

1. 인자가 없으면 다섯 동작과 예시를 메뉴로 보여주고 멈춘다.
2. 두 분류가 비슷하게 맞으면 짧은 질문 하나: "draft 새로 쓰라는 거야, 기존 문단 다듬으라는 거야?"
3. 하나가 분명하면 바로 보낸다. 재확인하지 않는다.
4. 대상 문단은 요청에 붙은 텍스트를 쓰고, 위치(`para:12`, `results exsolution`)로 주면 원고를 읽어 찾는다.
5. 보내기 전에 한 줄로 알린다: `Routing: HUMANIZE -> paper-style-enforcer`.
6. 결과를 전하고 다음 단계를 한 줄 제안한다.
   - plan -> 계획의 첫 `/paper-*` 명령
   - ref -> 고른 ref로 `/paper-draft`
   - draft -> `/paper-critic para:drafted`
   - critic -> blocker가 있으면 `/paper-draft revise:blocker1`, 없으면 `/paper-humanize`
   - humanize -> 사용자 검토
7. 어느 분류에도 안 맞으면 PLAN으로 처리한다.
8. 한 번 호출에 subagent는 하나만 보낸다. 연쇄는 사용자가 다음 호출로 정한다.
9. project-context.md가 없고 주제 맥락이 도움이 되는 작업이면 한 번 언급하되 막지 않는다.
