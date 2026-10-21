
# Humanize-Codex: HTML/문서 가독성 검수 via Codex CLI

## Overview

design2html의 하드 룰(약어 금지, 비유 금지, 명사구 제목, 숫자 일관성)은 생성
시점 규칙이지만, 문서가 여러 라운드 누적 편집되면 위반이 다시 스며든다.
Codex CLI를 "이 프로젝트를 모르는 첫 독자"로 세워 이해 장애물을 잡아낸다.
작성자(Claude)는 자기 문서의 맥락을 알아서 결함을 못 보므로 외부 눈이 필요.

**핵심 원칙: 실행 전 사용자 승인, read-only 고정, 지적은 제안으로만 소비,
종료 시 토큰 보고.**

## When to Use

- HTML 리포트가 수 라운드 편집 후 일관성 점검이 필요할 때
- 사용자가 "이해가 안 된다 / 흐름이 안 잡힌다 / 약어가 많다"고 할 때
- 발표나 공유 직전 최종 검수

**쓰지 말 것:** 한글 문체 윤문(그건 /humanize 계열), 과학적 정확성 검증(그건
/paper-critic), 생성 직후 자체 체크(design2html self-check로 충분).

## Input Preparation (중요)

렌더된 HTML은 base64 이미지 때문에 수 MB라 그대로 못 먹인다. 우선순위:

1. **생성기 소스가 있으면 그것을** (예: build_report.py 안의 f-string 본문)
2. 없으면 텍스트만 추출한 사본 생성:
   ```bash
   python3 -c "import re,sys; h=open(sys.argv[1]).read(); h=re.sub(r'data:[^\"\\')]+','DATA_URI',h); open(sys.argv[2],'w').write(h)" in.html /tmp/doc_stripped.html
   ```

## Workflow

1. **승인**: "codex로 문서 가독성 검수 (read-only, 플랜 쿼터)" 보고, OK.
2. 입력 준비 (위), 프롬프트 파일 Write.
3. 실행:
   ```bash
   codex exec --skip-git-repo-check --sandbox read-only \
     -c model_reasoning_effort=low \
     --output-last-message /path/readability.md - < /path/prompt.txt
   ```
   프롬프트 안에 대상 파일 절대경로 명시 (codex가 직접 읽음).
4. 결과를 심각도별 요약 -> 사용자 확인 후 타당한 것만 Claude가 원본 수정.
5. `tokens used` 보고.

## Prompt File Rules - 검수 축 (design2html 하드 룰 파생)

프롬프트에 아래 축을 그대로 나열한다. 역할: "너는 이 프로젝트를 전혀 모르는
전공 인접 독자다. 처음 읽으면서 걸리는 모든 지점을 기록하라."

1. **약어/전문용어**: 첫 등장에서 풀이 없는 약어, 자체 발명 용어 (표준 용어
   MAE, DFT, MLIP 등은 허용)
2. **지엽성**: 전체 주장과 연결 안 되는 세부 수치/서술, "왜 이 얘기가 여기
   있지" 싶은 문단
3. **비유/수사**: 은유, 극적 표현, 질문형/서술문 제목 (명사구 제목이 표준)
4. **흐름**: 섹션 간 논리 연결 누락, 결론이 어디 있는지 못 찾는 구조,
   같은 내용의 중복 서술
5. **일관성**: 같은 양이 다른 숫자로 등장, 그림 번호와 본문 참조 불일치,
   용어 표기 흔들림 (예: mean3 / 3모델 평균 혼용)
6. **독자 부하**: 한 문장에 조건 3개 이상, 괄호 중첩, 표가 말로 풀려 있는 곳

출력 형식 고정: `| severity | 위치(섹션/그림) | 문제 | 수정 제안 |` 표.
마지막 줄: "확신 없으면 [추정]. 완벽보다 완료 우선."

## Common Mistakes

- 렌더된 3MB HTML을 통째로 투입 -> 컨텍스트 낭비. 반드시 소스나 stripped 사본.
- codex 제안 문장을 그대로 붙여넣기 -> 문서 문체(입니다체, 가운뎃점 금지 등)와
  충돌. Claude가 문체 규칙에 맞춰 다시 쓴다.
- 가독성 지적과 사실 오류 지적을 섞어 받기 -> 사실 검증은 별도 절차로. 이 스킬
  결과에서 사실 관련 지적이 나오면 데이터로 재확인 후에만 반영.
