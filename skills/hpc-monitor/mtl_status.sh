#!/bin/bash
# mtl_status.sh — Matlantis 백그라운드 잡 현황 + "내 잡" 하이라이트 (tqdm 스타일)
#   · 내 잡(OWNER_PREFIX)은 ★ 달아 상단 고정 + tqdm 진행률 막대
#   · 남의 잡은 아래에 owner별 count/elapsed로 요약
#   · 진행률은 잡이 결과노트북에 "실제로 찍은 값"만 사용 → 근거 없으면 '불명'으로 정직하게(지어내지 않음)
# ps/grep/awk/tail 만 사용 → 1-CPU 인스턴스 안전 (python/임시파일/폴링 없음, 스냅샷 1회).
# 사용:  ssh <MATLANTIS_HOST> 'bash -s -- <YOUR_FOLDER>' < mtl_status.sh
#   OWNER_PREFIX = matlantis 인스턴스 /home/jovyan/ 아래 본인 폴더명.
export LC_ALL=C
OWNER_PREFIX="${1:-CHANGE_ME}"
W=20

mkbar(){ local n=$1 t=$2 w=${3:-$W} i f b=""; f=0; [ "$t" -gt 0 ] && f=$(( n*w/t ));
  for((i=0;i<w;i++)); do if [ "$i" -lt "$f" ]; then b+="█"; else b+="░"; fi; done; printf '%s' "$b"; }

fmt_et(){ case "$1" in
    *-*)   printf "%sd%s" "${1%%-*}" "$(x=${1#*-}; printf '%s' "${x%:*}")";;  # D-HH:MM:SS → Dd HH:MM
    *:*:*) printf "%s" "${1%:*}";;                                            # HH:MM:SS → HH:MM
    *)     printf "%s" "$1";;                                                 # MM:SS 그대로
  esac; }

# 한 잡당: etime|outpath|owner|name  (owner=/home/jovyan/<owner>/... , name=결과노트북 basename에서 _results_날짜 제거)
JOBS=$(ps -eo etime,args | grep -E 'bin/papermill' | grep -v 'grep' | awk '
  { et=$1; out=$NF; n=split(out,seg,"/"); owner=seg[4];
    name=seg[n]; sub(/\.ipynb$/,"",name); sub(/_results_[0-9].*$/,"",name);
    if (owner!="") print et "|" out "|" owner "|" name }')

echo "=========== Matlantis 잡 현황 (스냅샷 1회) ==========="
echo
echo "★ 내 잡 ($OWNER_PREFIX)"
if [ -z "$JOBS" ]; then echo "  (papermill 백그라운드 잡 없음)"; fi
mine=0
while IFS='|' read -r et out owner name; do
  [ -z "$owner" ] && continue
  [ "$owner" = "$OWNER_PREFIX" ] || continue
  mine=1
  pct=-1; cur=0; tot=0; detail=""
  case "$out$name" in
    *umbrella*)
      tr=$(grep -oE "Trial [0-9]+/[0-9]+" "$out" 2>/dev/null | tail -1)
      st=$(grep -oE "Stage [0-9]+/[0-9]+" "$out" 2>/dev/null | tail -1)
      if [ -n "$tr" ] && [ -n "$st" ]; then
        T=${tr##* }; T=${T%%/*}; NT=${tr##*/}
        S=${st##* }; S=${S%%/*}; NS=${st##*/}
        tot=$(( NT*NS )); cur=$(( (T-1)*NS + S ))
        [ "$tot" -gt 0 ] && pct=$(( cur*100/tot ))
        detail="trial $T/$NT stage $S/$NS"
      fi;;
    *)
      # 범용: 잡이 찍은 마지막 진행 토큰(있으면 그대로 표시, 없으면 불명)
      detail=$(grep -oE "t=[0-9.]+ *fs|[0-9.]+ *ps|Time\[?ps\]? *[0-9.]+|[Ss]tep *[0-9]+ */ *[0-9]+" "$out" 2>/dev/null | tail -1)
      ;;
  esac
  if [ "$pct" -ge 0 ]; then
    printf "  ★ %-14s %3d%%|%s| %s  (%s)\n" "$name" "$pct" "$(mkbar "$cur" "$tot")" "$detail" "$(fmt_et "$et")"
  elif [ -n "$detail" ]; then
    printf "  ★ %-14s  %s  (%s)  [%%계산불가, 잡이 찍은 값]\n" "$name" "$detail" "$(fmt_et "$et")"
  else
    printf "  ★ %-14s  진행률 불명 (elapsed만)  (%s)\n" "$name" "$(fmt_et "$et")"
  fi
done <<< "$JOBS"
[ "$mine" = 0 ] && [ -n "$JOBS" ] && echo "  (돌고 있는 내 잡 없음 — prefix '$OWNER_PREFIX' 확인)"

echo
echo "──── 그 외 공유 잡 (요약) ────"
echo "$JOBS" | awk -F'|' -v me="$OWNER_PREFIX" '
  $3!=me {
    o=$3; cnt[o]++;
    if (!((o SUBSEP $4) in seen)) { seen[o SUBSEP $4]=1; nm[o]=nm[o] (nm[o]?" ":"") $4 }
    if (et[o]=="") et[o]=$1 }
  END{ k=0; for(o in cnt){ k++;
         nn=nm[o]; if(length(nn)>46) nn=substr(nn,1,46) "…";
         printf "  · %-11s %d잡 running  (~%s)  %s\n", o, cnt[o], et[o], nn }
       if(k==0) print "  (없음)" }'

echo
echo "  legend: ★=내 잡(top) · █ 진행 ░ 남음 · 진행률=잡이 결과노트북에 찍은 값만(없으면 불명) · 남의 잡은 요약"
