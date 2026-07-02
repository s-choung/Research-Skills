---
name: hpc-monitor
description: Use when the user wants a one-shot read-only status view of their compute — local machine + SLURM GPU cluster + a scheduler-less CPU server + Matlantis (papermill MD jobs) — as tqdm-style bars. Pure bash + ssh, no LLM/API. Triggers - hpcmon, HPC 모니터, GPU 현황, 큐 상황, squeue, 서버 현황, 잡 현황, matlantis 잡, MD 잡 확인, "얼마나 busy".
---

# hpc-monitor

로컬 머신 + 원격 3종(SLURM GPU 클러스터 · 스케줄러 없는 CPU 서버 · Matlantis 인스턴스)의 사용률·잡 현황을 한 번에 뽑는 **읽기전용** bash 모니터. LLM/네트워크 API 없이 순수 bash + ssh 로 동작하며, 원격에서 실행하는 명령은 전부 관측용(`squeue`/`sinfo`/`ps`/`free`/`uptime`/`grep`/`awk`)이라 서버 상태를 바꾸지 않는다.

## 구성
- `monitor_all.sh` — 오케스트레이터. 아래 3개를 병렬 SSH로 던지고 취합. `hpcmon` alias 대상.
- `gpu_status.sh` — SLURM GPU 점유/실행/대기 현황 (로그인 노드에서 실행).
- `mace_status.sh` — 스케줄러 없는 CPU 서버 load/RAM/계산 프로세스.
- `mtl_status.sh` — Matlantis papermill 백그라운드 잡 현황 + "내 잡" 진행률.

## Usage
```bash
# 1) monitor_all.sh 상단 config (SLURM_USER, MTL_PREFIX, HPC_HOST, CPU_HOST, MTL_HOST) 를 본인 환경으로 편집
# 2) alias 등록 후:
hpcmon
```
개별 실행:
```bash
ssh "$HPC_HOST" "bash -s -- $SLURM_USER"  < gpu_status.sh
ssh "$CPU_HOST" 'bash -s'                 < mace_status.sh
ssh "$MTL_HOST" "bash -s -- $MTL_PREFIX"  < mtl_status.sh
```

셋업 상세는 `README.md`, 에이전트용 안내는 `AGENTS.md` 참고.
