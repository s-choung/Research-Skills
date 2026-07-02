# hpc-monitor

한 번의 명령으로 **로컬 컴퓨터 + SLURM GPU 클러스터 + 스케줄러 없는 CPU 서버 + Matlantis(MD 잡)** 를 tqdm 스타일 막대로 한눈에 보여주는 읽기전용 모니터.

- LLM/네트워크 API 없이 **순수 bash + ssh** 로 동작 (결정적, 빠름).
- 원격 3개는 **병렬 SSH**, 로컬은 그 사이 즉시 계산.
- 원격에서 실행하는 명령은 전부 **읽기전용** (`squeue`/`sinfo`/`ps`/`free`/`uptime`/`grep`/`awk`). 서버 상태를 바꾸지 않음.

```
====================이 컴퓨터 ====================
  CPU   12%|██░░░░░░░░░░░░░░░░░░|
  RAM   41%|████████░░░░░░░░░░░░|  used (free 59%)
====================SLURM-GPU 서버 ====================
  [ ★ 내 잡 (alice) — ... ]
  [ GPU 점유 (종류별) · busy/total ]
  ...
====================CPU 서버 ====================
====================Matlantis (MD) ====================
```

## 구성

| 파일 | 역할 | 실행 위치 |
|---|---|---|
| `monitor_all.sh` | 오케스트레이터 (아래 3개를 병렬 SSH로 던지고 취합) | 로컬 |
| `gpu_status.sh`  | SLURM GPU 점유/실행/대기 현황 | SLURM 로그인 노드 |
| `mace_status.sh` | 스케줄러 없는 CPU 서버 load/RAM/계산 프로세스 | CPU 서버 |
| `mtl_status.sh`  | Matlantis papermill 백그라운드 잡 현황 | Matlantis 인스턴스 |

각 프로브는 `ssh <host> 'bash -s' < probe.sh` 로 **스크립트를 서버에 전송해 실행**하므로, 서버에 미리 설치할 필요가 없다.

## 셋업

### 1. `~/.ssh/config` 에 3개 호스트 alias 등록
```sshconfig
Host hpc-gpu        # SLURM 로그인 노드
    HostName <IP 또는 도메인>
    User <계정>

Host cpu-server     # 스케줄러 없는 CPU 서버
    HostName <IP 또는 도메인>
    User <계정>

Host matlantis      # Matlantis 인스턴스 (연결 방식은 Matlantis 문서 참고)
    HostName <...>
    User jovyan
    ProxyCommand <matlantis 웹소켓 프록시>
```
> Matlantis 는 계정별로 발급되는 SSH-over-WebSocket 프록시로 접속한다. 각자 본인 계정의 연결 스크립트를 사용하고, **pre-shared key 등 비밀값을 이 저장소에 커밋하지 말 것.**

### 2. `monitor_all.sh` 상단 config 편집
```bash
SLURM_USER="alice"        # SLURM 계정 (squeue -u 대상)
MTL_PREFIX="1_Alice"      # matlantis /home/jovyan/<본인 폴더명>
HPC_HOST="hpc-gpu"        # 위 ssh config alias
CPU_HOST="cpu-server"
MTL_HOST="matlantis"
```
GPU 클러스터의 파티션/노드는 `gpu_status.sh` 상단(또는 환경변수 `PARTS`/`NODES`)에서 지정:
```bash
PARTS="gpu1,gpu2"
NODES="node01 node02"
```

### 3. alias 등록
```bash
echo "alias hpcmon='bash $HOME/hpc-monitor/monitor_all.sh'" >> ~/.zshrc
```

## 사용
```bash
hpcmon
```
필요한 서버만 쓰려면 개별 실행도 가능:
```bash
ssh hpc-gpu   'bash -s -- alice'  < gpu_status.sh
ssh cpu-server 'bash -s'          < mace_status.sh
ssh matlantis 'bash -s -- 1_Alice' < mtl_status.sh
```

## 주의
- 전부 읽기전용 스냅샷 1회. 폴링/데몬 없음.
- Matlantis 진행률(%)은 잡이 결과 노트북에 **실제로 찍은 값**만 사용한다. 근거가 없으면 지어내지 않고 `진행률 불명`으로 표기.
- 로컬 섹션은 macOS(`top`/`memory_pressure`) 기준. Linux 로컬이면 해당 섹션은 자동으로 비워진다.
