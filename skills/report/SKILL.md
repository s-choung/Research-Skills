---
name: report
description: 연구 결과(csv, json, 로그, 구조 파일, 기존 그림)를 여러 스킬(design2html, matplotlib-scientific, blender-atom-render, ko-writing, bulletization)로 조합해 단일 파일 HTML 리포트 하나로 만드는 오케스트레이션 스킬. 계획 > 툴 리스팅 > 재료 리스팅 > 분석 > 생산 > 합체 > audit > 문체 정제 순서로 가고, 재료 생산과 이미지 검수는 sonnet subagent에 맡긴다. Triggers - /report, html 리포트 만들어, 결과 정리해서 리포트, report html, 벤치 결과 리포트, 실험 결과 html로.
user-invocable: true
argument-hint: "<결과 폴더 또는 질문> [--style openai|apple|...] [--out <path.html>]"
---

# report: 결과 폴더에서 HTML 리포트 하나로

여러 스킬을 순서대로 묶어 **단일 파일 HTML 리포트** 하나를 만든다. 메인 세션은
계획과 판단만 하고, 시간이 드는 생산(그림 스크립트, 렌더, 이미지 검수, 문체 교정)은
sonnet subagent에 나눠 준다. 실전 원형은 `165_SDL_현황/002_feature_bench`
(scripts/build_report.py, fig_*.py, render_ligands.sh)이다.

## 단계 (순서 고정, 건너뛰기 금지)

| 단계 | 누가 | 산출물 |
|---|---|---|
| 0 계획 | main | `report_plan.md` (질문, 메시지 계층, figure 목록, 토글 설계) |
| 1 툴 리스팅 | main | 쓸 스킬과 스크립트 목록, 각 스킬의 하드 룰 요약 |
| 2 재료 리스팅 | main + subagent(조사) | `materials.md` (데이터 파일, 열, 행 수, 기존 그림, 구조 파일, 수치 출처) |
| 3 분석 | main | 찾을 수치를 전부 표로 뽑고, 본문 불릿 초안(데이터셋별, 모델별, feature별 등)을 쓴다 |
| 4 생산 | subagent x N (sonnet) | 그림 svg, 렌더 png, 표 csv. 각 산출물은 audit 결과와 함께 반환 |
| 5 합체 | main | `scripts/build_report.py` -> `<name>_report.html` |
| 6 audit | main + subagent(이미지 읽기) | 정적 검사 + Playwright + 스크린샷 검수 |
| 7 문체 정제 | subagent(ko-writing) -> main 반영 | 입니다체 통일, AI체 제거, 캡션과 본문 분리 재확인 |

각 단계가 끝나면 한 줄로 사용자에게 보고한다. 단계 4의 subagent 배치는 띄우기 전에
"무엇을 몇 개" 한 줄 보고 (글로벌 background 보고 규칙).

## less-talk 규칙 (2026-09-17 사용자 지시, 모든 리포트에 기본 적용)

독자는 결정하려고 읽는다. 문장, 라벨, 범례 항목 하나하나가 주의력을 쓴다. 지우면 독자의
다음 행동이 바뀌는 것만 남긴다. `~/.claude/skills/less-talk/SKILL.md`의 Reports와 Figures
절이 원문이며, 여기서는 build_report.py에 박아 넣을 형태로 적는다.

- **섹션 = 헤드라인 1문장 + 불릿 최대 3개 + 그림 1개.** 헤드라인은 결정(채택, 폐기, 통과)을
  말한다. 불릿은 그 결정을 바꿀 수 있는 수치만. 그 아래는 전부 `<details>`.
- **`<details>` 기본 세 종류**: `방법`(그 절의 절차 문단), `근거와 해석`(ok/warn/neg 판정
  블록), `표 펼치기`(표). 문서 전체의 방법, 파라미터, 비용, 파일 경로는 문서 끝 `방법, 비용,
  파일 경로` 블록 하나에만.
- **숫자는 한 번만.** 요약, 절, 한계에 같은 수치를 반복하지 않는다. 헤드라인에 쓴 수치는
  불릿에서 빼고, 불릿에 쓴 수치는 해석 블록에서 뺀다.
- **표는 기본 heatmap + 접힘.** 수치 열은 열별 min/max로 셀 배경(좋음 초록 #a8dbb5, 나쁨
  붉음 #f4b6b6). "낮을수록 좋음"이 기본, Spearman/AUROC/coverage/이득/엔트로피 열은 반대.
  독자가 결정에 쓰는 표(king 표) 하나만 펼쳐 둔다. 나머지는 그림으로 바꾸거나 접는다.
- **표마다 그림 하나.** 표가 있는 절에는 같은 데이터의 그림이 표 위에 먼저 온다. 그리드
  스윕은 heatmap(imshow + 셀 숫자), 조건 비교는 막대, 스케일과 곡선은 log-x 선, 보정은
  reliability curve. 그림 토글은 쓰지 않는다. 변형은 heatmap 한 장이나 접힌 블록으로.
- **그림 텍스트는 초안의 절반.** 축 제목 4단어 + 단위, 범례는 축 밖(오른쪽 또는 아래),
  데이터 영역 안 금지. 값 주석은 그 값이 결정일 때만. 세트와 모델 이름은 짧은 코드로 쓰고
  코드 대조표는 접힌 블록 하나에.
- **캡션 첫 문장 = 그림의 메시지 하나.** 메시지가 둘이면 그림을 나누거나 하나를 접는다.
- **검사**: matplotlib audit 통과 후 PNG를 Read로 열어 눈으로 확인(Playwright가 `@` 경로에서
  멈추면 `fig.savefig(png)`로 대체). HTML은 절마다 `ul.lead li` 3개 이하, 펼쳐진 `<table>`
  1개 이하를 정적 검사에 넣는다.
- 구현 예: `168_MLIP_Router/report/build_v4_section.py`의 `table()`(heatmap + details),
  `fig()`(svg 인라인), `HEAD` dict(절별 헤드라인과 불릿) + 끝의 less-talk 후처리 regex.

## 0. 계획: 메시지 계층 먼저

리포트는 질문에서 시작한다. 코드 짜기 전에 `report_plan.md`에 다음을 적는다.

- 주질문 하나와 하위 질문 2~3개. 001/002 리포트 형식: "무엇을 가장 잘 보는 feature와 모델은 무엇인가".
- 섹션 계층 (기본 골격, 필요하면 줄이되 순서는 유지):
  1. 요약 (불릿 4~6개, 각 불릿 아래 근거 수치) + 표 1 (king 표)
  2. 질문과 설계 (데이터 표, 대상 구조 렌더 Figure 1, 세트와 모델)
  3. 결과 (하위 질문 순서대로. figure 하나 + 그 아래 본문 불릿 하나)
  4. 흥미로운 결과 (축별 계층 불릿: 데이터셋별, 모델별, feature별)
  5. Methods (볼드 라벨. 산문)
  6. 한계와 다음 단계
  7. 부록 (전체 표는 details 접기)
- figure 목록: Figure 1~n, 각 figure의 토글 차원(예: 모델 x 지표, 패널 x 분할 x 모델)과
  변형 파일 개수. 변형은 `<stem>__<dim1>__<dim2>.svg`로 이름 짓는다.
- 각 figure 아래에 올 본문 불릿의 주장(수치는 3단계에서 채움).

## 1. 툴 리스팅

쓸 스킬을 이름과 하드 룰 한 줄씩으로 적는다. 기본 세트:

| 스킬 | 역할 | 잊기 쉬운 하드 룰 |
|---|---|---|
| design2html | 페이지 토큰, 레이아웃, self-check | 장식 border 금지, `word-break:keep-all`, 텍스트 max-width 금지, 최소 13.5px, 회색 글씨 #5a6573보다 연하게 금지, 외부 리소스 0, 가로 스크롤 0, 화학식 `<sub>` |
| matplotlib-scientific | svg 그림 | FontProperties 전부, legend 밖, `audit()` 겹침과 프레임 밖 검사, `svg.fonttype='none'` |
| blender-atom-render | 구조 렌더 | 프로세스당 파일 1개, 순차, 원소 범례 256px, ballradius 1.0 |
| ko-writing | 한국어 문체 | 입니다체 통일, 가운뎃점과 엠대시 금지, 자평 수식어 금지, "절 n" 대신 "section n" |
| bulletization | 본문 계층 불릿 | 한 불릿 한 주장, 2단계까지, 최상위만 읽어도 논지 |
| paper (캡션 규칙) | 캡션 | 캡션은 그림 설명만, 수치와 해석은 본문 불릿, 방법은 Methods |

스타일 스펙은 design2html의 built-in 이름 하나로 고른다(기본 openai). 사용자가 스타일을
말하지 않았으면 이전 리포트와 같은 것을 쓴다.

## 2. 재료 리스팅

`materials.md`에 표로 적는다. 열: 파일, 종류(csv/json/npy/xyz/png), 크기(행, 열 또는 픽셀),
핵심 열 이름, 어느 figure와 표에 쓰이는지. 이 표에 없는 파일은 리포트에 못 들어간다.

- 큰 폴더 조사는 Explore subagent 하나에 맡긴다 (읽기 전용, 30초 내).
- 수치의 단일 소스는 master csv 하나로 고정한다. 리포트의 모든 표와 그림은 그 파일에서
  다시 계산한다. 손으로 옮긴 수치는 금지.
- 다른 폴더의 대조 수치(예: 이전 캠페인 결과)는 파일 경로와 행 조건을 스크립트 주석에 적는다.
- **기존 그림은 그대로 쓴다 (2026-09-17 사용자 결정).** 이전 리포트나 분석 폴더에 이미 있는
  svg/png가 메시지를 담고 있으면 다시 그리지 않고 `materials.md`에 등록해 인라인한다.
  다시 그리는 경우는 (a) 그림이 없거나, (b) 축이나 비교 대상이 리포트 질문과 안 맞을 때뿐이다.
  "스타일 통일"은 다시 그릴 이유가 아니다. 기존 그림은 audit에서 겹침 검사만 하고 폰트 규칙은
  면제한다. 캡션에 원본 경로를 적는다.

## 3. 분석

- master csv를 전부 덤프해 읽는다 (`to_string`). 수치를 보지 않고 불릿을 쓰지 않는다.
- 각 figure의 본문 불릿 초안을 쓴다. 불릿마다 근거 수치 2개 이상.
- 주장 하나마다 확인 스크립트 한 줄을 돌린다 (예: "XPhos의 NMR 값이 나머지 밖"이면
  groupby로 실제 값을 뽑는다). 확인 안 된 주장은 지운다.
- 흥미로운 결과는 축별로 모은다. 축은 데이터의 자연 축(데이터셋, 모델, feature, 조건).

## 4. 생산: subagent 분배

sonnet subagent에 그림 스크립트 작성과 실행을 맡긴다. 한 subagent에 figure 1~2개.
프롬프트에 반드시 넣을 것:

```
- fig_common.py 경로와 OUT 폴더 (OUT은 <project>/figures/)
- master csv 경로와 열 이름, 필터 조건
- 파일 이름 규칙 <stem>__<dim1>__<dim2>.svg 와 변형 목록 전부
- matplotlib-scientific 하드 룰 6줄 (FontProperties, legend 밖, no grid/bold/tight_layout, audit)
- 완료 조건: 모든 변형에서 C.audit(fig)가 overlaps none, frame overflow none
- 반환 형식: 생성 파일 목록 + audit 출력 + 문제 있으면 어떤 값 조정했는지
```

- Blender 렌더는 subagent가 아니라 main이 `nohup bash render_*.sh` 로 순차 배치를 띄운다
  (blender-atom-render 규칙: 동시 1개). subagent는 xyz 준비와 legend 합성만.
- 이미지 검수는 별도 subagent: png 또는 Playwright 스크린샷 경로를 주고
  "겹침, 잘림, 빈 축, 범례 누락, 라벨 오탈자"를 항목별 예/아니오로 반환하게 한다.
- subagent 결과는 파일 목록으로만 받는다. svg 본문을 대화로 돌려받지 않는다.
- 여러 subagent를 한 메시지에 병렬로 띄운다. 독립적이지 않은 것(렌더 -> 그리드 합성)은 순차.

## 5. 합체: build_report.py

002의 `scripts/build_report.py`를 복사해서 시작한다. 구조:

- `svg(name)`: svg 인라인, 주석과 metadata 제거, 좌표 소수 2자리로 절단
- `png(name, width)`: PIL 리사이즈 + quantize(255) + base64
- `bl(items)`: 중첩 리스트 -> `<ul><li>`
- `figbox(id, dims, variants, caption)`: 버튼 그룹 + `.fv[data-key]` 변형 + `fvSync` JS
- `cap(n, text)`: `<b>Figure n.</b> 설명`
- `table(headers, rows)`: 첫 열 좌측, 나머지 가운데
- 폰트: Inter latin woff2 base64 (`001_flexcat/repro/inter_latin.b64` 재사용)
- 텍스트 블록은 전부 파이썬 리스트 상수(SUMMARY, R21, ...)로 두어 7단계에서 통째로 교체 가능하게

출력 파일 이름은 ASCII (`<name>_report.html`). 프로젝트 루트에 두고 figures/와 scripts/는 옆에.

## 6. audit (하드 게이트, 전부 통과 전 출력 금지)

정적 검사 스크립트 (`templates/check_html.py` 복사):
- 장식 border 0, `keep-all` 있음, `break-all` 없음
- `max-width`는 컨테이너, `@media`, `.fig img/svg`에만
- font-size 최소 13.5px (sub 제외)
- 콘텐츠 색 `#5a6573`보다 연한 회색 없음
- 외부 `src`/`<link>` 0
- 가운뎃점, 엠대시 0. 한다체 종결 0 (입니다체 문서일 때)
- 금지어(무너, 엉뚱, 폭발, 치솟, 핵심, 격차) 0
- 제목 전수: 질문형, 접속사 시작, 서술문, 수량 접미사 없음. **섹션 제목은 보고서식 명사구로만** (2026-09-17 사용자 지적, 반복 실수). 금지 예: "이 문서의 위치", "선행 연구가 끝낸 지점", "오차 바닥은 누가 정하는가", "DFT 없이 c를 맞출 수 있는가". 대신 "연구 개요", "선행 연구", "기울기 c의 예측 가능성", "공통 잔차의 분포". 질문은 본문 첫 문장에 쓰고 제목에는 쓰지 않는다. check_html.py의 `bad headings`가 잡는다 (200_what_mlip_learned/scripts/check_html.py).
- less-talk: 절마다 헤드라인 1개와 `ul.lead li` 3개 이하, `<details>` 밖의 `<table>` 1개 이하,
  수치 열이 있는 표는 셀 배경색 있음, 그림 범례가 axes 안에 없음
- 화학식 평문 숫자 없음

Playwright 검사 (`templates/pw_check.py` 복사):
- http 요청 전부 abort한 상태에서 `document.fonts.check` true, 모든 img naturalWidth>0
- 1440, 1280, 1024에서 `scrollWidth - innerWidth == 0`
- 토글 버튼 클릭 후 보이는 `.fv`가 정확히 1개
- JS 에러 0
- 스크린샷 4장 이상(요약, figure 2개, methods)을 이미지 검수 subagent에 넘겨 예/아니오 보고

실패 항목은 고치고 6단계를 처음부터 다시 돈다.

## 7. 문체 정제

- 텍스트 상수(SUMMARY, R2x, INTERESTING, METHODS, LIMITS, 캡션)를 md 하나로 뽑아
  ko-writing subagent에 준다. 지시: "ko-prose.md와 fluent-korean.md 전문 적용, 수치와
  파일 이름은 바꾸지 말 것, 반환은 같은 구조의 md".
- 돌아온 텍스트를 diff로 보고 수치가 바뀐 줄이 있으면 되돌린다.
- 반영 후 6단계 정적 검사만 다시 돈다.
- **용어 검사 (2026-09-17 사용자 지시, 필수).** 문체 교정과 별도로 subagent(sonnet) 한 번 더.
  같은 md와 `~/.claude/skills/ko-writing/domain-terms.md`를 주고 "분야에서 영어로 부르는 개념을
  억지 한국어로 옮긴 말(규약, 범함수, 의사퍼텐셜, 묶음, 판정, 처방 등)을 전부 찾아 사전의 오른쪽
  열 말로 바꿔라. 사전에 없어도 도메인 사람이 안 쓰는 번역어면 영어 용어로. 수치와 f-string은
  손대지 말 것"으로 지시한다. 사용자가 지적한 사례: "라벨 규약이 다른" -> "functional이 다른",
  "+U 없는 PBE 라벨". 돌아온 결과를 diff로 반영하고 새 사례는 domain-terms.md에 추가한다.
- 마지막으로 캡션, 본문, Methods의 역할 분리를 한 번 더 본다: 캡션에 수치나 "relax했다"류
  방법 문구가 있으면 옮긴다.

## 사용자에게 보고

끝나면 짧게: 파일 경로와 크기, 섹션 계층, figure 수와 토글 차원, 새로 확인한 결과 3~5개,
audit 통과 항목, 비용(로컬이면 0). 스크린샷은 붙이지 않는다.

## 하지 말 것

- 수치 없이 불릿 쓰기. master csv 덤프를 먼저 읽는다.
- subagent에 svg 내용을 대화로 받기. 파일 경로만.
- Blender를 subagent 병렬로 돌리기.
- 캡션에 해석 넣기. "Figure n."은 설명만.
- 한 파일에 en/ko 병기 요구가 없으면 한국어 단일로. 병기는 사용자가 말했을 때만.
- audit 실패 상태로 "완성" 보고.

## HTML 리포트 실전 규칙 (2026-09-22, PdPt/ceria 리포트에서 확립)

- **그림 스크립트를 고쳤으면 build를 다시 돌린다.** HTML은 SVG를 빌드 시점에 인라인하므로
  figure만 재생성하면 화면은 그대로다. 사용자가 "안 바뀌었다"고 말하기 전에 재빌드한다.
  figure 수정과 재빌드는 한 묶음이다.
- **회색 note 박스는 그 박스가 설명하는 그림 바로 아래에, 섹션당 1개.** 박스 2개가 연달아
  붙으면 병합하고 불릿을 줄인다. Blender 렌더처럼 설명이 캡션으로 끝나는 그림은 예외.
- **섹션 안 순서는 렌더 먼저, 그 렌더를 해석한 플롯 나중.** 독자는 구조를 본 다음에 분석을 읽는다.
- **강조는 `<span class='hl'>`(bold + `#b3261e`) 하나로, 박스당 최대 1개.** 두 개를 쓰면 둘 다
  안 읽힌다. f-string 안에서는 작은따옴표로 쓴다.
- **그림이 이미 보여 주는 표는 옆에 두지 말고 지운다.**
- **패널을 지우거나 순서를 바꾸면 본문의 패널 문자 참조가 전부 stale이 된다.** `(Figure g)` 류를
  전수 grep해서 고친다.
- p-value와 통계 검정 언급은 본문에서 뺀다. 수치는 json에만 남긴다.
- "대상 / 비교 대상 / 계산 종류" 류 설정 요약 박스는 만들지 않는다. 독자의 결정을 바꾸지 않는다.
- 출고 전에 **안 쓰이는 텍스트 상수**를 grep한다. 섹션을 지우면 상수만 남는다.
- **기존 리포트에 결과를 추가했으면 `redundancy-remove` 스킬을 이어서 돌린다 (2026-09-24 사용자
  지적).** 새 데이터가 들어오면 같은 관측량을 다룬 옛 절이 밀려나는데, 추가만 하고 옛 절을
  두면 독자가 같은 결과를 두 번 읽는다. 실사례: 궤적 1개짜리 MD 절(Figure 2장, 표 1개)이
  seed 30개 절 바로 위에 남아 있었다. 추가와 제거는 한 묶음이다.
- 어려운 한자어 검사를 문체 정제(7단계)에 포함한다. `ko-writing/domain-terms.md`의
  "어려운 한자어" 표 왼쪽 열을 전수 grep.
