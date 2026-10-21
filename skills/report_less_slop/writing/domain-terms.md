# 도메인 용어 사전 (2026-09-17 사용자 지시)

원칙: **분야에서 영어로 부르는 개념은 영어 그대로 쓴다.** 억지로 한국어로 옮기면 읽는 사람이
"이게 뭘 말하는 거지"를 한 번 더 해석해야 한다. 한국어 번역이 굳어진 말(에너지, 힘, 오차, 구조,
원자, 학습 데이터)만 한국어로 쓴다.

## 쓰지 말 것 -> 쓸 것 (계산화학, MLIP, ML)

| 억지 한국어 | 대신 쓸 말 |
|---|---|
| 규약, 라벨 규약, DFT 규약 | functional, DFT 설정, +U 유무, pseudopotential (무엇이 다른지를 그 이름으로) |
| 의사퍼텐셜 | pseudopotential (POTCAR) |
| 범함수 | functional |
| 묶음 (모델을 학습 데이터로 나눈 그룹) | cohort (학습 데이터 cohort) |
| (합의, 공통 잔차는 사용자가 쓰는 말이라 허용) | |
| 기울기 보정 | slope 보정, c 보정 |
| 잡음 | noise (라벨 noise) |
| 편향 | bias |
| 설명력 | R2 |
| 상한, 하한 | upper bound, lower bound (문맥이 수학이면), 아니면 최대, 최소 |
| 분할 | split (train/test split) |
| 검증 분할, 시험 분할 | validation split, test split |
| 평형 구조 | relaxed 구조 (DFT relaxed) |
| 이완, 이완한, 이완 절차, 이완 구조 | relaxation, relax. "relaxation한 구조", "relaxation 절차", "relax시킨 구조" (2026-09-21 재지시: 위반이 반복됨) |
| 학습 퍼텐셜, 머신러닝 퍼텐셜, 기계학습 퍼텐셜 | MLIP (machine-learning interatomic potential) |
| 단일점 계산 | single point |
| 전이 상태 | transition state, TS |
| 층화 추출 | stratified sampling |
| 볼록껍질, 하부 볼록껍질 | convex hull, lower convex hull |
| 배위수 | coordination number (처음 한 번 "배위수(coordination number)" 뒤로는 CN도 가능) |
| 앙상블 | ensemble |
| 미세 조정 | fine-tune |
| 원자당 에너지 | eV/atom 단위로 쓴 에너지 (원자당은 허용) |
| 판정 | 결론 |
| 처방 | 보정 방법, 제안 |
| 정답 배율 | oracle c |
| 통제군, 통제 모델 | control (random control) |
| 부호 있는 오차 | signed error |
| 절대 오차 | |error| 또는 absolute error |

## 과잉교정 금지 (한국어가 학계 표준인 말)

다음은 한국어가 표준이므로 영어로 바꾸지 않는다.
화학 퍼텐셜, 퍼텐셜 에너지, 배위수(첫 등장에 coordination number 병기 후 CN 허용), 형성 에너지, 공공,
격자, 흡착, 해리, 상태도, 분압, 수렴, 장벽, 궤적, 격자 상수.

"퍼텐셜"이 들어갔다고 전부 MLIP로 바꾸지 않는다. 앞에 붙은 말이 "학습", "머신러닝", "기계학습"일 때만 MLIP다.

## 유지해도 되는 한국어
에너지, 힘, 응력, 오차, MAE(그대로), 구조, 원자, 원소, 조성, 학습 데이터, 모델, 세트, 기울기(c의 뜻으로 그림에서 slope와 같이 쓸 때),
표, 그림, 요약, 결론, 방법, 한계.

## 검사 방법
리포트 텍스트 상수를 뽑아 subagent(sonnet)에 이 파일과 함께 넘긴다. 지시: "이 표의 왼쪽 열에 있는 말과,
표에 없더라도 분야에서 영어로 부르는 개념을 한국어로 억지 번역한 말을 전부 찾아 오른쪽 열의 말로 바꿔라.
수치와 {f-string}은 건드리지 마라." 돌아온 diff에서 수치가 바뀐 줄은 되돌린다.

## 어려운 한자어 (2026-09-22 사용자 지시, PdPt/ceria 리포트에서 확립)

원칙 확장: **분야 용어가 영어면 영어로, 분야 용어가 아닌 한자어면 일상 한국어로.**
읽는 사람이 소리 내어 읽고 한 번 더 뜻을 떠올려야 하는 한자어는 리포트에서 쓰지 않는다.
둘 중 무엇으로 갈지 애매하면 영어를 택한다.

| 쓰지 말 것 | 대신 쓸 말 |
|---|---|
| 입경 | 입자 크기, particle size |
| 시료 | 샘플 |
| 율속, 율속 단계 | 전체 속도를 결정하는 단계, rate-determining step |
| 담지, 담지체 | 지지체에 올린, support |
| 소성 | calcination |
| 전처리 | pretreatment |
| 분산도 | dispersion |
| 비표면적 | surface area (단위를 같이 적는다) |
| 산입 | 포함 |
| 배제 | 뺌, 제외 |
| 도출 | 얻음 |
| 기인함 | ~에서 옴 |
| 수반 | 같이 일어남 |
| 상이함 | 다름 |
| 잔류 | 남은 |
| 저감 | 줄임 |
| 유의미한 | 뚜렷한 (통계 검정을 말하는 것이 아니면) |
| 추이 | 변화, 시간에 따른 값 |
| 기저 | 기준 상태, baseline |

검사도 같다. 리포트 텍스트 상수를 뽑아 이 표의 왼쪽 열을 전수 grep한다.
