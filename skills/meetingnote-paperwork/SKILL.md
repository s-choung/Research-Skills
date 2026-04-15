---
name: meetingnote-paperwork
description: Generate Korean research project meeting notes (회의록) in a fixed paperwork template. Use when the user asks for 회의록, meeting note paperwork, 과제 회의록 써줘, 회의록 부탁, or types /meetingnote-paperwork. Takes a 과제명 as input (asks once if missing) and drafts content in a computational chemistry / materials design voice (screening, DFT, descriptor, ML, benchmark, reaction path).
---

# Meeting Note Paperwork Skill

Drafts Korean meeting notes (회의록) in the fixed paperwork template the user
uses for project reporting. Content is grounded in computational chemistry /
materials design themes: screening, DFT, descriptor analysis, ML model
comparison, benchmarking, reaction path analysis.

## Invocation flow

### Step 1. Get the 과제명
Look at the user's message for a 과제명.

- **과제명이 있으면** 그대로 사용. 키워드에서 과제 주제를 추론해서 내용을 작성.
- **없으면** 한 번만 물어본다.
  Example: "어떤 과제 회의록이에요? 과제명 주세요."
  유저는 본인 과제명을 알고 있으니 리스트를 펼치지 말 것.

### Step 2. Figure out how many notes
Default: **one** note.

The user may say "회의록 2개", "1) ... 2) ...", or paste two placeholder
blocks. In that case generate exactly that many, numbered `1)`, `2)`, ...

### Step 3. Draft in the fixed template
Use this template verbatim for each note (preserve the `X/X`, `XX:XX`,
`XX,000원`, `XX동 XXX호` placeholders; those are filled in later by hand):

```
X/X XX:XX XX,000원
회의참석자 (성명/직급/소속) :
회의 시간/장소 : XX:XX ~ XX:XX / XX동 XXX호
회의 목적/내용 :
<one-line overall purpose tied to the 과제>

- <bullet 1>
- <bullet 2>
- <bullet 3>
(- <bullet 4, optional>)
```

If generating multiple notes, prefix each with `1)`, `2)`, ... on its own
line before the `X/X ...` line.

### Step 4. Content rules (computational chemistry voice)

Content should read like the user's group doing calculation-side work for
the project. Safe, recurring motifs:

- 후보 소재/조성 스크리닝 기준 논의 / 재정의
- DFT 흡착 에너지 / 반응 경로 / 활성화 에너지 분석
- Descriptor 기반 분석 (d-band center, work function, E(O*), p-d coupling, charge gradient 등)
- ML 모델 (RF / XGBoost / GNN) 성능 비교, uncertainty-aware ranking
- Microkinetic / AIMD 모델링 결과 해석
- 실험 그룹과의 협업 조성/물질 선정 및 전달
- 벤치마크: PBE vs meta-GGA, 계산 정확도/속도 비교, 슬랩 모델 축소 전략
- 파이프라인 자동화 (VASP-ASE 연동 등) 현황 공유

Each bullet should read like a real discussion outcome, not a todo.
Examples: "X 논의", "Y 결과 공유", "Z 기준 재조정", "N종 선정 및 전달안 확정".
2 to 4 bullets per note is normal.

Tie the content to the 과제. 과제명의 키워드(예: N2O 저감, MLCC 유전체,
암모니아 SOFC, 수전해, 탄산광물화, LOHC, BTX 분리, de novo 효소 등)에서
주제를 추론하고, 해당 주제에 맞는 계산 방법론과 소재군을 bullet에 반영.

### Step 5. Output

Output only the meeting notes. No preamble, no trailing explanation.
Plain text (not wrapped in a code block). Keep everything in Korean. Do
not invent participant names or real times (those stay as `XX:XX`
placeholders).

## Tonal anchors

Three reference example sets from when the skill was created:
(a) spinel oxide / microkinetic, (b) BCC/FCC/HCP 초기 구조 + VASP-ASE
자동화, (c) descriptor 최적화 + ML uncertainty ranking. Use them as tonal
anchors for the bullet voice, not as templates to reproduce literally.
