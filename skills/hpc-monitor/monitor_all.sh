#!/bin/bash
# monitor_all.sh — 한 방 HPC 모니터: 이 컴퓨터 + SLURM-GPU 서버 + CPU 서버 + Matlantis(MD).
#   LLM 안 거치고 이 스크립트 하나로 결정적/빠른 포맷 출력.
#   원격 3개는 병렬 SSH(백그라운드), 로컬(이 컴퓨터)은 그 사이 즉시 계산.
#   결과 캐시: ~/.cache/hpcmon (매 실행 덮어쓰기).
# 사용:  bash monitor_all.sh   (또는 alias hpcmon='bash /경로/monitor_all.sh')

# ============ EDIT: 본인 환경에 맞게 바꾸세요 ============
SLURM_USER="${SLURM_USER:-$USER}"       # SLURM 서버 로그인 계정 (squeue -u 대상) ← 본인 것으로
MTL_PREFIX="${MTL_PREFIX:-CHANGE_ME}"   # matlantis /home/jovyan/<이 폴더명>       ← 본인 것으로
HPC_HOST="${HPC_HOST:-hpc-gpu}"         # ~/.ssh/config 의 SLURM 로그인노드 alias
CPU_HOST="${CPU_HOST:-cpu-server}"      # ~/.ssh/config 의 CPU 서버 alias
MTL_HOST="${MTL_HOST:-matlantis}"       # ~/.ssh/config 의 matlantis alias
# =======================================================

export LC_ALL=C
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GPU="$DIR/gpu_status.sh"
MACE="$DIR/mace_status.sh"
MTL="$DIR/mtl_status.sh"
CACHE="$HOME/.cache/hpcmon"
mkdir -p "$CACHE"
W=20
mkbar(){ local n=$1 t=$2 w=${3:-$W} i f b=""; f=0; [ "$t" -gt 0 ] && f=$(( n*w/t ));
  [ "$f" -gt "$w" ] && f=$w
  for((i=0;i<w;i++)); do if [ "$i" -lt "$f" ]; then b+="█"; else b+="░"; fi; done; printf '%s' "$b"; }

# --- 원격 3개 병렬로 던져놓고 (백그라운드), 그 사이 로컬 계산·출력 ---
ssh -o ConnectTimeout=15 -o BatchMode=yes "$HPC_HOST" "bash -s -- $SLURM_USER" < "$GPU" >"$CACHE/gpu.txt" 2>"$CACHE/gpu.err" &
P1=$!
ssh -o ConnectTimeout=15 -o BatchMode=yes "$CPU_HOST" 'bash -s' < "$MACE" >"$CACHE/cpu.txt" 2>"$CACHE/cpu.err" &
P2=$!
ssh -o ConnectTimeout=15 -o BatchMode=yes "$MTL_HOST" "bash -s -- $MTL_PREFIX" < "$MTL" >"$CACHE/mtl.txt" 2>"$CACHE/mtl.err" &
P3=$!

echo "====================이 컴퓨터 ===================="
echo "  load avg:$(uptime | sed -E 's/.*load averages?://')"
IDLE=$(top -l 2 -n 0 2>/dev/null | awk '/CPU usage/{l=$0} END{k=split(l,a," "); for(i=1;i<=k;i++) if(a[i]=="idle"){v=a[i-1]; gsub(/%/,"",v); print v}}')
if [ -n "$IDLE" ]; then BUSY=$(awk -v i="$IDLE" 'BEGIN{printf "%d",100-i}');
  printf "  CPU  %3d%%|%s|\n" "$BUSY" "$(mkbar "$BUSY" 100)"; fi
FREE=$(memory_pressure 2>/dev/null | awk -F: '/free percentage/{gsub(/[ %]/,"",$2); print $2}')
if [ -n "$FREE" ]; then USED=$(( 100-FREE ));
  printf "  RAM  %3d%%|%s|  used (free %s%%)\n" "$USED" "$(mkbar "$USED" 100)" "$FREE"; fi
DUSED=$(df -h / 2>/dev/null | awk 'NR==2{gsub(/%/,"",$5); print $5}')
if [ -n "$DUSED" ]; then printf "  DISK %3d%%|%s|  /\n" "$DUSED" "$(mkbar "$DUSED" 100)"; fi

# --- 원격 결과 회수 ---
wait "$P1" "$P2" "$P3" 2>/dev/null
echo
echo "====================SLURM-GPU 서버 ===================="
if [ -s "$CACHE/gpu.txt" ]; then cat "$CACHE/gpu.txt"; else echo "  ⚠ 접속/실행 실패:"; sed 's/^/    /' "$CACHE/gpu.err"; fi
echo
echo "====================CPU 서버 ===================="
if [ -s "$CACHE/cpu.txt" ]; then cat "$CACHE/cpu.txt"; else echo "  ⚠ 접속/실행 실패:"; sed 's/^/    /' "$CACHE/cpu.err"; fi
echo
echo "====================Matlantis (MD) ===================="
if [ -s "$CACHE/mtl.txt" ]; then cat "$CACHE/mtl.txt"; else echo "  ⚠ 접속/실행 실패:"; sed 's/^/    /' "$CACHE/mtl.err"; fi
