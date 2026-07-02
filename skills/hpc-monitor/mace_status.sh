#!/bin/bash
# mace_status.sh — 스케줄러 없는 CPU 서버 (bare Ubuntu) 모니터.
#   load/RAM bar + 돌고 있는 계산 프로세스(python/mace/vasp/lammps/orca/…) 하이라이트.
#   uptime(/proc/loadavg)/free/nproc/ps/awk 만 사용 (읽기전용, 스냅샷 1회).
#   SLURM이 없어 '내 잡' = 계산 프로세스(이름 매칭 또는 CPU>10%). 상시 데몬은 제외.
# 사용:  ssh <CPU_HOST> 'bash -s' < mace_status.sh
export LC_ALL=C
W=20
mkbar(){ local n=$1 t=$2 w=${3:-$W} i f b=""; f=0
  if [ "$t" -gt 0 ]; then f=$(( n*w/t )); fi
  [ "$f" -gt "$w" ] && f=$w
  for((i=0;i<w;i++)); do if [ "$i" -lt "$f" ]; then b+="█"; else b+="░"; fi; done; printf '%s' "$b"; }

echo "=========== CPU 서버 현황 ==========="
NC=$(nproc)
read L1 L5 L15 rest < /proc/loadavg
LB=$(awk -v l="$L1" -v n="$NC" 'BEGIN{printf "%d",(n>0?l/n*100:0)}')
[ "$LB" -gt 100 ] && LB=100
printf "  load %3s%%|%s|  1m %s / %s core  (5m %s, 15m %s)\n" "$LB" "$(mkbar "$LB" 100)" "$L1" "$NC" "$L5" "$L15"
read MT MA < <(free -m | awk '/^Mem:/{print $2, $7}')
MU=$(( MT - MA )); MP=0; [ "$MT" -gt 0 ] && MP=$(( MU*100/MT ))
printf "  RAM  %3d%%|%s|  %dGi/%dGi used\n" "$MP" "$(mkbar "$MP" 100)" $((MU/1024)) $((MT/1024))

echo
echo "★ 계산 잡 (python/mace/vasp/lammps/orca/gpaw/cp2k/xtb, 또는 CPU>10%)"
OUT=$(ps -eo user,pid,pcpu,pmem,etime,args --sort=-pcpu | awk '
  NR==1{next}
  { line=tolower($0); cpu=$3+0;
    if (line ~ /gnome|gjs|ibus|vte|tracker|uvicorn|cloudflared|tailscaled|systemd|dbus|polkit|avahi|network|sshd|bash|zsh|ps -eo|grep|node |unattended|packagekit|update-notifier|snapd|fwupd|dpkg|colord|rtkit|gvfs|accounts-daemon|cron/) next;
    iscomp = (line ~ /python|mace|vasp|lmp|lammps|orca|gpaw|cp2k|pw\.x|xtb|mpirun|mpiexec/);
    if (iscomp || cpu>10) {
      cmd=""; for(i=6;i<=NF;i++) cmd=cmd $i " ";
      if(length(cmd)>52) cmd=substr(cmd,1,52) "…";
      printf "  ★ %-9s cpu%5.1f%% mem%4.1f%% %11s  %s\n",$1,$3,$4,$5,cmd }
  }')
if [ -z "$OUT" ]; then echo "  (돌고 있는 계산 잡 없음 — idle)"; else printf '%s\n' "$OUT" | head -12; fi

echo
echo "  legend: load=1분부하/코어 · █ 사용 ░ 여유 · ★=계산 프로세스(스케줄러 없는 bare 서버)"
