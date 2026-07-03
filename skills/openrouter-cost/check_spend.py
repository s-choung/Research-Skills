#!/usr/bin/env python3
"""OpenRouter API 지출/잔액 조회 + "방금 얼마 썼는지" 델타 측정.
키는 macOS keychain(account 지정) 또는 OPENROUTER_API_KEY env 에서 읽음. 키 값은 절대 출력하지 않음.

사용:
  python3 check_spend.py                      # keychain account: openrouter, openrouter2
  python3 check_spend.py openrouter2          # 특정 account
  OPENROUTER_API_KEY=sk-... python3 check_spend.py   # 원시 키(env)
  python3 check_spend.py --snapshot           # run 직전: 현재 usage 저장
  python3 check_spend.py --diff               # run 직후: snapshot 대비 증분($)
"""
import sys, os, json, subprocess, urllib.request, urllib.error

STATE = os.path.expanduser("~/.openrouter_spend_snapshot.json")
DEFAULT_ACCOUNTS = ["openrouter", "openrouter2"]


def keychain(account, service="openrouter-api-key"):
    try:
        r = subprocess.run(["security", "find-generic-password", "-a", account, "-s", service, "-w"],
                           capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return ""


def get(key, ep):
    req = urllib.request.Request("https://openrouter.ai/api/v1/" + ep,
                                 headers={"Authorization": "Bearer " + key})
    try:
        return json.load(urllib.request.urlopen(req, timeout=25)).get("data", {})
    except urllib.error.HTTPError as e:
        return {"_err": "HTTP %s" % e.code}
    except Exception as e:
        return {"_err": str(e)[:80]}


def resolve_keys(args):
    envkey = os.environ.get("OPENROUTER_API_KEY")
    if envkey:
        return [("env", envkey)]
    accts = [a for a in args if not a.startswith("--")] or DEFAULT_ACCOUNTS
    return [(a, keychain(a)) for a in accts]


def usage_of(key):
    cr = get(key, "credits")
    ak = get(key, "auth/key")
    tu = cr.get("total_usage")
    tc = cr.get("total_credits")
    return {
        "credits": tc, "used": tu,
        "remain": (tc - tu) if (tc is not None and tu is not None) else None,
        "daily": ak.get("usage_daily"), "weekly": ak.get("usage_weekly"),
        "monthly": ak.get("usage_monthly"), "lifetime": ak.get("usage"),
        "err": cr.get("_err") or ak.get("_err"),
    }


def fmt(v):
    return "$%.2f" % v if isinstance(v, (int, float)) else "-"


def main():
    args = sys.argv[1:]
    keys = resolve_keys(args)

    if "--snapshot" in args:
        snap = {name: usage_of(k).get("used") for name, k in keys if k}
        json.dump(snap, open(STATE, "w"))
        print("snapshot 저장:", {n: fmt(v) for n, v in snap.items()}, "->", STATE)
        return

    if "--diff" in args:
        if not os.path.exists(STATE):
            print("snapshot 없음. 먼저 --snapshot 실행."); return
        snap = json.load(open(STATE))
        print("%-14s %10s %10s %10s" % ("account", "before", "now", "증분($)"))
        for name, k in keys:
            if not k:
                continue
            now = usage_of(k).get("used")
            before = snap.get(name)
            delta = (now - before) if (now is not None and before is not None) else None
            print("%-14s %10s %10s %10s" % (name, fmt(before), fmt(now),
                                            ("+$%.4f" % delta) if delta is not None else "-"))
        return

    # 기본 리포트
    print("%-14s %9s %9s %9s %9s %9s" % ("account", "credits", "used", "remain", "weekly", "daily"))
    for name, k in keys:
        if not k:
            print("%-14s  (키 없음)" % name); continue
        u = usage_of(k)
        if u.get("err"):
            print("%-14s  오류: %s" % (name, u["err"])); continue
        print("%-14s %9s %9s %9s %9s %9s" % (name, fmt(u["credits"]), fmt(u["used"]),
                                             fmt(u["remain"]), fmt(u["weekly"]), fmt(u["daily"])))
        print("               monthly %s · lifetime %s" % (fmt(u["monthly"]), fmt(u["lifetime"])))


if __name__ == "__main__":
    main()
