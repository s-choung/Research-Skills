# Research-Skills TODO

작성일: 2026-05-16

---

## 0. Security Audit (민감 정보 점검)

- [ ] **개인정보 스캔 결과 리뷰**
  - `Seokhyun Choung` 이름 + `s-choung` GitHub handle: README, index.html footer, build_slides.py에 존재 → **공개 의도이므로 OK**
  - API key, 이메일, 전화번호, 주소 등: **미발견** ✅
  - `build_slides.py`: `Seokhyun Choung · SNU` 반복 (LinkedIn 슬라이드 생성용) → Task 1에서 처리
  - `agents/paper-ref-hunter.journals.json`: journal 목록 파일 → 개인정보 아님 ✅

---

## 1. LinkedIn Slides 비공개 처리

LinkedIn 슬라이드는 개인 자료이므로 public repo에서 제거.

- [ ] `.gitignore`에 추가:
  ```
  linkedin-slides/
  linkedin-slides.html
  build_slides.py
  extract_slides.py
  ```
- [ ] git tracking에서 제거 (`git rm --cached`)
- [ ] 로컬 파일은 보존 확인

---

## 2. LinkedIn Slide 1 배경 흰색으로 변경

- [ ] `linkedin-slides.html` Slide 1: `background: #000` → `background: #fff`, 텍스트 색상 반전
- [ ] `build_slides.py` 동일 수정 (재생성 시 반영되도록)
- [ ] slide_1.png 재생성 (Playwright 또는 수동 캡처)

---

## 3. MIT License 추가

- [ ] repo 루트에 `LICENSE` 파일 생성 (MIT, 2026, Seokhyun Choung)

---

## 4. ASE 벤치마크 바 차트 수정

현재 `assets/ase_bench_barplot.png` 이미지 문제점 4가지 수정. 원본 생성 스크립트 없음 — 새로 작성 필요.

- [ ] **바 순서 반전**: 현재 +Skill(위) → Vanilla(아래). 수정: w/o Skill(위, 낮은 값) → w/ Skill(아래, 높은 값)
- [ ] **레이블 변경**: "Vanilla" → "w/o Skill", "+ Skill" → "w/ Skill"
- [ ] **레전드 순서**: 위 = w/o Skill (연한색), 아래 = w/ Skill (진한색)
- [ ] **Provider 로고-라벨 간격**: "Gemini", "OpenAI", "Claude" 텍스트가 모델명과 겹침 → 여유 공간 확보
- [ ] matplotlib 스크립트 새로 작성 (`skills/ase/benchmark/build_barplot.py`)
  - 데이터: benchmark_report_v6.html의 SUMMARY에서 추출 (또는 하드코딩)
  - 출력: `assets/ase_bench_barplot.png` 덮어쓰기
- [ ] GitHub Pages 배포 HTML에서 PNG 경로 확인

### ASE 스킬 파일 정리

현재: `ase_skill_v1.md`, `ase_skill_v2.md`, `ase_skill_v3.md` (다른 스킬은 전부 `SKILL.md`)
- [ ] `ase_skill_v3.md` → `SKILL.md`로 rename (최신 버전이 메인)
- [ ] v1, v2는 `benchmark/` 또는 `archive/`로 이동 (비교용 보존)

---

## 5. Assets 폴더 정리 (repo 경량화)

현재 상태: benchmark PNG들이 각 skill 폴더에 산재 (blender-atom-render/benchmark만 19MB)

- [ ] `assets/benchmarks/` 하위에 스킬별 서브폴더 생성
- [ ] 각 skill의 `benchmark/*.png` → `assets/benchmarks/{skill}/`로 이동
- [ ] benchmark HTML 내 이미지 경로 상대→절대 or `../../assets/benchmarks/` 로 수정
- [ ] 각 skill 폴더에는 `SKILL.md` (+ 중요 스킬은 `README.md`) + benchmark HTML만 남기기
- [ ] 이동 대상 (크기순):
  | Skill | Size | Files |
  |---|---|---|
  | blender-atom-render | 19 MB | 8 PNG |
  | design2html | 1.4 MB | 6 PNG + 6 HTML |
  | matplotlib-scientific | 528 KB | 6 PNG |
  | humanizer_eng | 416 KB | 2 JSON |
  | humanizer_kor | 348 KB | HTML only |
  | transcript2html | 28 KB | HTML only |
- [ ] slide-audit의 `package-lock.json` (불필요) → `.gitignore` 또는 삭제
- [ ] `index-preview.png` (루트) → `assets/`로 이동, README 경로 수정

---

## 6. index.html: Paper Ref Hunter 강조

- [ ] `/paper-ref-hunter` 카드 추가 (Writing 카테고리)
  - `Frequent` 배지 달기
  - 설명: "Run /paper-ref with a claim. Hunts matching papers via Crossref + OpenAlex, verifies DOIs, and returns a ranked shortlist. Catches hallucinated references before they enter your manuscript."
- [ ] `/smart-compact`의 `Frequent` 배지 제거 (또는 순서를 뒤로)
- [ ] 카드 순서: ase → matplotlib → paper-ref-hunter → humanizer_eng → humanizer_kor → design2html → ...

---

## 7. Paper Ref Hunter 벤치마크

내 도메인(계산화학/촉매) 연구자 기반으로 hallucinated paper 검출 테스트.

- [ ] 테스트 대상 연구자:
  - **Jens Norskov** (Stanford/DTU, 촉매/DFT)
  - **John Kitchin** (CMU, 전기화학/ML)
  - **한정우 (Jeong Woo Han)** (POSTECH, 촉매/계산화학)
  - **정석현 (Seokhyun Choung)** — 내 논문 25편
- [ ] `/wiki`에서 내 논문 25편 리스트 로드
- [ ] 벤치마크 시나리오 설계:
  - (A) paper-ref-hunter **있이** → 실제 논문 검증률, hallucination 검출률
  - (B) paper-ref-hunter **없이** (vanilla LLM) → hallucinated paper 비율
  - (C) 내 논문 25편 중 무작위 claim으로 본인 논문 찾는지
- [ ] 결과를 `skills/paper-ref-hunter/benchmark/benchmark_report.html`로 생성
- [ ] index.html 카드에 Benchmark 링크 연결

---

## 8. Paper .bib 생성 스킬 제작

DOI/제목 → `.bib` entry 자동 생성 스킬.

- [ ] `skills/paper-bib/SKILL.md` 작성
  - 입력: DOI, 논문 제목, 또는 paper-ref-hunter 결과
  - 출력: BibTeX entry (article, inproceedings 등)
  - Crossref API로 메타데이터 검증
  - 기존 `.bib` 파일에 append 또는 신규 생성
- [ ] `commands/paper-bib.md` slash command 작성
- [ ] 테스트: 내 논문 5편 DOI로 .bib 생성 검증
- [ ] index.html에 카드 추가 (Writing 카테고리)

---

## 9. 최종 Push

- [ ] 모든 변경사항 확인 (git diff)
- [ ] Task 1~8 완료 여부 체크
- [ ] git add + commit
- [ ] `git push origin main`

---

## 실행 순서 (의존성 기준)

```
병렬 그룹 A (독립 작업):
├── Task 1: LinkedIn 비공개 처리
├── Task 2: Slide 1 흰색 배경
├── Task 3: MIT License
├── Task 4: ASE 바 차트 수정 + 스킬 파일 정리
└── Task 5: Assets 정리

병렬 그룹 B (A 완료 후):
├── Task 6: index.html Paper Ref Hunter 강조
├── Task 7: Paper Ref Hunter 벤치마크 (wiki 로드 → 시나리오 → HTML)
└── Task 8: Paper .bib 스킬 제작

순차:
└── Task 9: 최종 Push (B 완료 후)
```

---

## 서브에이전트 배정 계획

| Task | Agent Type | 비고 |
|---|---|---|
| 1 LinkedIn 비공개 | general-purpose | gitignore + git rm --cached |
| 2 Slide 배경 | general-purpose | HTML/CSS 수정 |
| 3 MIT License | general-purpose | 파일 1개 생성 |
| 4 ASE 바 차트 | general-purpose | matplotlib 스크립트 작성 + PNG 재생성 + SKILL.md rename |
| 5 Assets 정리 | general-purpose | mv + 경로 수정 (가장 큰 작업) |
| 6 index.html 수정 | general-purpose | 카드 추가/수정 |
| 7 Ref Hunter 벤치마크 | general-purpose | wiki 로드 + API 호출 + HTML |
| 8 .bib 스킬 | general-purpose | SKILL.md + command 작성 + 테스트 |
