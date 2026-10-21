"""report_less_slop 최소 빌더.

텍스트와 표는 아래 상수만 고친다. STYLE은 같은 폴더의 build_report_example.py에서 가져온다.
출력: 단일 HTML 파일 하나 (외부 리소스 0, Inter 폰트 base64 내장).

실행: python build_minimal.py out.html
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
OUT_HTML = Path(sys.argv[1] if len(sys.argv) > 1 else "report.html")
FONT_B64 = (HERE / "inter_latin.b64").read_text().strip()

src = (HERE / "build_report_example.py").read_text()
STYLE = re.search(r'STYLE = f"""(.*?)"""', src, re.S).group(1)
STYLE = STYLE.replace("{FONT_B64}", FONT_B64).replace("{{", "{").replace("}}", "}")
STYLE += """
.f{display:inline-block;min-width:22px;padding:0 7px;border-radius:9999px;background:#fdebd8;color:#9a3412;font-weight:600;font-size:13.5px;text-align:center}
.f0{background:transparent;color:#555555;font-weight:400}
.sub{display:block;font-size:13.5px;color:#555555;margin-top:2px}
td.l,th.l{text-align:left}
tr.ch td{background:#f7f7f8;font-weight:600}
"""


# ---------- helpers ----------
def bullets(tree):
    """tree: [(최상위 주장, [근거, ...]), ...]  계층은 두 단계까지만."""
    h = "<ul>"
    for text, subs in tree:
        h += f"<li>{text}"
        if subs:
            h += "<ul>" + "".join(f"<li>{s}</li>" for s in subs) + "</ul>"
        h += "</li>"
    return h + "</ul>"


def heat(v, vmax, rgb="194,65,12"):
    """수치 셀 배경. 값이 클수록 진하다. 좋고 나쁨이 있으면 rgb를 초록/빨강으로 나눠 쓴다."""
    if not v:
        return f"<td>{v}</td>"
    a = 0.15 + 0.6 * v / vmax
    return f"<td style='background:rgba({rgb},{a:.2f});font-weight:600'>{v}</td>"


def table(headers, rows, left_cols=(0,)):
    """첫 열(라벨)은 왼쪽, 나머지는 가운데. 머리글과 셀 정렬을 맞춘다."""
    def cls(i):
        return " class='l'" if i in left_cols else ""
    h = "<div class='tbl'><table><tr>" + "".join(f"<th{cls(i)}>{x}</th>" for i, x in enumerate(headers)) + "</tr>"
    for r in rows:
        h += "<tr>" + "".join(x if str(x).startswith("<td") else f"<td{cls(i)}>{x}</td>" for i, x in enumerate(r)) + "</tr>"
    return h + "</table></div>"


def cap(label, text):
    return f"<p class='cap'><b>{label}.</b> {text}</p>"


def details(summary, body):
    return f"<details class='arch'><summary>{summary}</summary>{body}</details>"


# ---------- 내용 (여기만 고친다) ----------
NAV_LEFT, NAV_SUB, NAV_DATE = "프로젝트", "리포트 주제", "2026-01-01"
TITLE = "A안과 B안의 비교"
# lead: 주장 하나에 한 줄. 두 주장이면 두 줄.
LEAD = [
    "B안은 A안과 구조가 같고, 비용도 비슷합니다.",
    "다른 곳은 처리 시간과 유지보수 항목입니다.",
]
# 요약: 최상위 불릿만 읽어도 결론이 이어지게. 결정을 바꾸지 않는 숫자는 표로 보낸다.
SUMMARY = [
    ("B안의 구조와 분량은 A안과 같습니다.", []),
    ("B안은 처리 시간이 짧습니다.", ["A안은 12분, B안은 7분입니다."]),
    ("B안은 유지보수 항목이 하나 더 있습니다.", []),
]
KING = table(
    ["항목", "A안", "B안"],
    [["단계 1", heat(3, 3), heat(2, 3)],
     ["단계 2", heat(1, 3), heat(1, 3)],
     ["<b>합계</b>", "<b>4</b>", "<b>3</b>"]],
)
CMP_ROWS = [
    ["<tr class='ch'><td class='l'>1. 준비</td><td class='l'>1. 준비</td></tr>"],
    ["1.1 입력 정리 <span class='f'>1</span><span class='sub'>그림 설명</span>", "1.1 입력 정리"],
]


def cmp_table(rows):
    h = "<div class='tbl'><table><tr><th class='l' style='width:50%'>A안</th><th class='l' style='width:50%'>B안</th></tr>"
    for r in rows:
        h += r[0] if len(r) == 1 else f"<tr><td class='l'>{r[0]}</td><td class='l'>{r[1]}</td></tr>"
    return h + "</table></div>"


BODY = f"""
<h1 class="sec">요약</h1>
<div class="note">{bullets(SUMMARY)}</div>
{KING}{cap("Table 1", "단계별 항목 수. 색이 진할수록 많습니다.")}

<h1 class="sec">항목별 대조</h1>
<p>다른 곳은 1.1의 그림입니다.</p>
{cmp_table(CMP_ROWS)}{cap("Table 2", "A안과 B안의 항목 목록. 주황 숫자는 그림 수입니다.")}

<h1 class="sec">부록</h1>
{details("집계 방법", bullets([("원자료와 집계 기준을 여기에 적습니다.", [])]))}
"""

html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<style>{STYLE}</style></head>
<body>
<nav><div><span class="brand">{NAV_LEFT}</span> <span class="meta">{NAV_SUB}</span></div><div class="meta">{NAV_DATE}</div></nav>
<div class="wrap">
<div class="hero">
<h1>{TITLE}</h1>
{''.join(f'<p class="lead">{x}</p>' for x in LEAD)}
</div>
{BODY}
<footer>원자료 경로와 비용을 한 줄로 적습니다.</footer>
</div>
</body></html>
"""
OUT_HTML.write_text(html)
print(OUT_HTML, len(html))
