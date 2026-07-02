#!/bin/bash
# gpu_status.sh — SLURM GPU 클러스터 종합 현황 (tqdm 스타일).
#   - 종류별 GPU 점유 막대 (멀티타입 노드 분해)        → 100%|████| 4/4
#   - 실행중(RUNNING) 누가 몇 장
#   - 대기중(PENDING) 종류별 막대 + 누가 몇 건 (건수 내림차순) ← 누가 큐 걸었는지 바로 보임
#   - "비었는데 왜 안 들어가나" 자동 진단
# sinfo/squeue/grep/awk 만 사용 → 로그인 노드에서 안전 (python/계산/임시파일 없음).
# 사용:  ssh <SLURM_LOGIN_HOST> 'bash -s -- <YOUR_SLURM_USER>' < gpu_status.sh
#
# ============ EDIT: 클러스터/계정에 맞게 ============
SLURM_USER="${1:-$USER}"                  # squeue -u 대상 (arg 로 넘기거나 로컬 $USER)
PARTS="${PARTS:-gpu1,gpu2}"               # 모니터할 파티션 (comma 구분) ← 본인 클러스터 값으로
NODES="${NODES:-node01 node02}"           # GPU 노드 목록 (space 구분)   ← 본인 클러스터 값으로
# sinfo/squeue 가 PATH 에 없으면 아래 주석 해제하고 경로 지정:
# export PATH="/opt/slurm/bin:$PATH"
# ===================================================
export LC_ALL=C
W=20

# tqdm 막대: filled 개수 / total → █(찬칸) + ░(빈칸) width W
mkbar(){ local ub=$1 tot=$2 w=${3:-$W} i f b=""; f=0; [ "$tot" -gt 0 ] && f=$(( ub*w/tot ));
  for((i=0;i<w;i++)); do if [ "$i" -lt "$f" ]; then b+="█"; else b+="░"; fi; done; printf '%s' "$b"; }

echo "=========== GPU 현황 (SLURM) ==========="
echo
echo "[ ★ 내 잡 ($SLURM_USER) — ID NAME ST GRES TIME LEFT NODE ]"
MINE=$(squeue -u "$SLURM_USER" -h -o "%.8i  %12j %.2t  %16b %.11M %.11L  %.6R" 2>/dev/null)
if [ -z "$MINE" ]; then echo "  (돌거나 대기 중인 내 잡 없음)"; else echo "$MINE" | awk '{printf "  ★%s\n",$0}'; fi
echo
echo "[ GPU 점유 (종류별) · busy/total ]"

TOT_BUSY=0; TOT_ALL=0
FREEMAP=""   # "type free\n..." 누적 (진단에서 사용)
for node in $NODES; do
  gres=$(sinfo -n "$node" -h -O "Gres:120")
  used=$(sinfo -n "$node" -h -O "GresUsed:120")
  types=$(echo "$gres" | grep -oE 'gpu:[a-z0-9]+:[0-9]+' | awk -F: '{print $2}')
  for t in $types; do
    tot=$(echo "$gres" | grep -oE "gpu:$t:[0-9]+" | head -1 | awk -F: '{print $3}')
    ub=$( echo "$used" | grep -oE "gpu:$t:[0-9]+" | head -1 | awk -F: '{print $3}')
    [ -z "$tot" ] && tot=0 ; [ -z "$ub" ] && ub=0
    free=$(( tot - ub ))
    pct=0; [ "$tot" -gt 0 ] && pct=$(( ub*100/tot ))
    printf "  %-5s %-7s %3d%%|%s| %d/%d  free %d\n" "$node" "$t" "$pct" "$(mkbar "$ub" "$tot")" "$ub" "$tot" "$free"
    FREEMAP+="$t $free"$'\n'
    TOT_BUSY=$(( TOT_BUSY+ub )); TOT_ALL=$(( TOT_ALL+tot ))
  done
done
echo "  ──────────────────────────────────────────────────"
TPCT=0; [ "$TOT_ALL" -gt 0 ] && TPCT=$(( TOT_BUSY*100/TOT_ALL ))
printf "  %-13s %3d%%|%s| %d/%d\n" "TOTAL" "$TPCT" "$(mkbar "$TOT_BUSY" "$TOT_ALL")" "$TOT_BUSY" "$TOT_ALL"

echo
echo "[ 실행중 (RUNNING) — 누가 몇 장 ]"
squeue -p "$PARTS" -t R -h -o "%u|%b" | awk -F'|' '
  { u=$1; b=$2; n=1; ty="gpu";
    if (match(b,/gpu:[a-z0-9]+:[0-9]+/)) { s=substr(b,RSTART,RLENGTH); split(s,a,":"); ty=a[2]; n=a[3] }
    else if (match(b,/gpu:[0-9]+/))      { s=substr(b,RSTART,RLENGTH); split(s,a,":"); ty="any"; n=a[2] }
    tot[u]+=n;
    if (!((u SUBSEP ty) in seen)) { seen[u SUBSEP ty]=1; tylist[u]=tylist[u] (tylist[u]?" ":"") ty }
    cnt[u SUBSEP ty]+=n }
  END { if (length(tot)==0) { print "  (없음)"; exit }
        for (u in tot) { det=""; m=split(tylist[u],ts," ");
          for (j=1;j<=m;j++){ det=det (det?", ":"") ts[j] "x" cnt[u SUBSEP ts[j]] }
          printf "  %-11s %2d GPU  (%s)\n", u, tot[u], det } }' | sort -k2 -rn

PEND=$(squeue -p "$PARTS" -t PD -h -o "%u|%b|%r")
echo
echo "[ 대기중 (PENDING) — 종류별 막대 + 누가 걸었나 (건수순) ]"
if [ -z "$PEND" ]; then
  echo "  (없음)"
else
  echo "$PEND" | awk -F'|' -v W="$W" '
    { u=$1; b=$2; ty="미지정";
      if (match(b,/gpu:[a-z0-9]+:[0-9]+/)) { s=substr(b,RSTART,RLENGTH); split(s,arr,":"); ty=arr[2] }
      tot[ty]++; uc[ty SUBSEP u]++;
      if (!((ty SUBSEP u) in useen)) { useen[ty SUBSEP u]=1; ulist[ty]=ulist[ty] (ulist[ty]?SUBSEP:"") u }
      if (tot[ty]>maxt) maxt=tot[ty] }
    END{ nt=0; for(t in tot) tord[++nt]=t;
      for(i=1;i<=nt;i++) for(j=i+1;j<=nt;j++) if(tot[tord[j]]>tot[tord[i]]){x=tord[i];tord[i]=tord[j];tord[j]=x}
      for(i=1;i<=nt;i++){ t=tord[i];
        f=(maxt>0)?int(tot[t]*W/maxt):0; bar="";
        for(k=0;k<W;k++) bar=bar (k<f?"█":"░");
        m=split(ulist[t],us,SUBSEP);
        for(p=1;p<=m;p++) for(q=p+1;q<=m;q++) if(uc[t SUBSEP us[q]]>uc[t SUBSEP us[p]]){x=us[p];us[p]=us[q];us[q]=x}
        det="";
        for(p=1;p<=m && p<=6;p++) det=det (det?" ":"") us[p] "x" uc[t SUBSEP us[p]];
        if(m>6) det=det " …";
        printf "  %-7s %3d |%s| %s\n", t, tot[t], bar, det } }'
fi

echo
echo "  legend: █ busy/대기 ░ free · 잡 낼 땐 --gres=gpu:<type>:N"
