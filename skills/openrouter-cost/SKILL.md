---
name: openrouter-cost
description: OpenRouter API 지출·잔액 조회 + "방금 얼마 썼는지" 델타 측정. macOS keychain 또는 OPENROUTER_API_KEY로 계정별 lifetime/monthly/weekly/daily usage와 남은 크레딧을 표로 보여주고, run 전후 snapshot/diff로 정확한 증분 비용을 낸다. 키 값은 절대 출력하지 않는다. Triggers - openrouter 비용, openrouter 지출, 크레딧 확인, 잔액 확인, 얼마 썼어, 방금 얼마 썼어, api 비용 확인, spend check, openrouter usage, cost monitor, 이번에 얼마.
---

# OpenRouter Cost Monitor

OpenRouter 계정의 지출·잔액을 조회하고, 특정 LLM run이 "방금 얼마 썼는지" 증분을 측정한다.
**키 값은 절대 stdout/로그에 노출하지 않는다** — keychain/env에서 읽어 in-process로만 사용.

## 배경 (왜 필요한가)
opencode·에이전트 도구의 자체 cost 추정은 **캐시 할인 가정 + 불완전 로깅**으로 실제 청구와 크게 다를 수 있다
(실측 사례: opencode가 $11로 기록한 AS run의 실제 OpenRouter 청구는 $153). **OpenRouter 계정값이 진실**이다.
강모델 × 긴 timeout × 다수 task 는 폭발적으로 비싸다 — 발사 전 예상비용, 발사 후 실측을 습관화.

## 사용

### 현재 지출·잔액
```bash
python3 check_spend.py                 # keychain account: openrouter, openrouter2
python3 check_spend.py openrouter2     # 특정 account만
OPENROUTER_API_KEY=sk-or-... python3 check_spend.py   # 원시 키(env)
```
출력: account별 `credits / used / remaining / weekly / daily` (+ `monthly · lifetime`).

### "방금 얼마 썼는지" (run 전후 델타) — 핵심 기능
```bash
python3 check_spend.py --snapshot      # run 직전: 현재 usage 저장(~/.openrouter_spend_snapshot.json)
# ... LLM run 실행 ...
python3 check_spend.py --diff          # run 직후: snapshot 대비 증분($)
```

## 키 규약 (schoung 환경)
- macOS keychain: service `openrouter-api-key`, account `openrouter`(주) / `openrouter2`(sonnet 등 보조).
- 조회 엔드포인트는 읽기전용(`/credits`, `/auth/key`) — 과금 없음.

## 주의
- `total_usage` / `lifetime` 은 누적. **"이번 세션" 비용**은 `monthly`·`weekly` 또는 `--snapshot`/`--diff` 로 봐야 정확.
- `usage_weekly`/`usage_monthly`/`usage_daily` 는 OpenRouter `/auth/key` 응답 필드.
