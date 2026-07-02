# AGENTS.md — hpc-monitor (에이전트용 안내)

이 문서는 **동료의 AI 에이전트**가 이 도구를 이해하고 바로 쓰도록 돕기 위한 것이다. 사람용 셋업은 `README.md` 참고.

## 이게 뭔가
로컬 머신 + 최대 3종 원격(SLURM GPU 클러스터 / 스케줄러 없는 CPU 서버 / Matlantis 인스턴스)의 사용률·잡 현황을 **읽기전용**으로 한 번에 뽑는 bash 스크립트 묶음. 상태를 변경하는 명령은 하나도 없다.

## 안전 계약 (agent 는 이걸 지킬 것)
- 이 스크립트들은 `squeue`/`sinfo`/`ps`/`free`/`uptime`/`grep`/`awk`/`df`/`top` 만 쓴다. **write/제출/kill 없음.**
- 파일 삭제·잡 취소·설정 변경을 임의로 하지 말 것. 이 도구의 범위는 "관측"뿐.
- 비밀값(API 키, matlantis pre-shared key, 토큰)을 출력하거나 커밋하지 말 것. 스크립트에도 비밀값은 없다.

## 사용 전 채워야 할 값 (사용자에게 물어보거나 설정에서 읽을 것)
| 변수 | 의미 | 예시 | 위치 |
|---|---|---|---|
| `SLURM_USER` | SLURM 계정 (squeue -u 대상) | `alice` | `monitor_all.sh` 상단 / `gpu_status.sh` 첫 arg |
| `MTL_PREFIX` | Matlantis `/home/jovyan/<폴더명>` | `1_Alice` | `monitor_all.sh` 상단 / `mtl_status.sh` 첫 arg |
| `HPC_HOST` | SLURM 로그인노드 ssh alias | `hpc-gpu` | `monitor_all.sh` 상단 |
| `CPU_HOST` | CPU 서버 ssh alias | `cpu-server` | `monitor_all.sh` 상단 |
| `MTL_HOST` | Matlantis ssh alias | `matlantis` | `monitor_all.sh` 상단 |
| `PARTS` | GPU 파티션 (comma) | `gpu1,gpu2` | `gpu_status.sh` 상단 / env |
| `NODES` | GPU 노드 (space) | `node01 node02` | `gpu_status.sh` 상단 / env |

`CHANGE_ME` 또는 placeholder(`hpc-gpu`/`node01` 등)가 남아 있으면 아직 설정 안 된 것이니, 실행 전에 사용자에게 실제 값을 확인할 것.

## 실행 방법
전체 요약:
```bash
bash monitor_all.sh
```
개별 서버(호스트별로 stdin 파이프):
```bash
ssh "$HPC_HOST" "bash -s -- $SLURM_USER"  < gpu_status.sh
ssh "$CPU_HOST" 'bash -s'                 < mace_status.sh
ssh "$MTL_HOST" "bash -s -- $MTL_PREFIX"  < mtl_status.sh
```
환경변수로 오버라이드도 가능:
```bash
SLURM_USER=alice MTL_PREFIX=1_Alice HPC_HOST=hpc-gpu CPU_HOST=cpu-server bash monitor_all.sh
```

## 출력 해석
- 막대 `█ = 사용/busy`, `░ = 여유/free`. 퍼센트는 busy/total.
- SLURM 섹션: `★ 내 잡`(squeue -u), GPU 종류별 점유, RUNNING(누가 몇 장), PENDING(종류별 + 누가 몇 건). "비었는데 왜 안 들어가나" 힌트 포함.
- CPU 서버 섹션: load(1분/코어) + RAM + 계산 프로세스(python/vasp/lammps/… 또는 CPU>10%). 상시 데몬은 제외.
- Matlantis 섹션: `★ 내 잡`(OWNER_PREFIX 일치)은 진행률 막대, 나머지는 owner별 요약.
  - **진행률은 잡이 노트북에 실제로 찍은 값만 사용.** 없으면 `진행률 불명`. 값을 추정/날조하지 말 것.

## 실패 모드
- 원격 섹션에 `⚠ 접속/실행 실패` + stderr 가 뜨면 → 십중팔구 ssh alias/네트워크/키 문제. 호스트 설정부터 확인.
- Matlantis `내 잡 없음` 은 (a) 진짜 안 도는 중이거나 (b) `MTL_PREFIX` 가 실제 폴더명과 다른 것. 둘 다 아니면 papermill 이 아닌 방식으로 띄운 잡일 수 있음(이 스크립트는 papermill 만 grep).
- 캐시는 `~/.cache/hpcmon/*.txt`(+`.err`) 에 매 실행 덮어씀. 실패 원인은 해당 `.err` 에 있음.
