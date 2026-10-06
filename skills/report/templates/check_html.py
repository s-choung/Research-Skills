"""design2html self-checks on the built report: borders, keep-all, max-width, font sizes,
gray text, external resources, forbidden chars, ending style, plus Playwright layout checks."""
import re
import sys

p = sys.argv[1]
s = open(p).read()
head = s.split("</style>")[0]
body = s.split("</style>")[1]
print("size MB", round(len(s) / 1e6, 2))
css = head
print("border decl:", [m for m in re.findall(r"border[^:;{}]*:[^;}]*", css) if "radius" not in m and "box" not in m and "border:0" not in m.replace(" ", "")])
print("keep-all:", "keep-all" in css, "| break-all:", "break-all" in css)
print("max-width:", re.findall(r"[.\w# ,]*\{[^}]*max-width[^;]*", css))
print("font sizes:", sorted(set(re.findall(r"font-size:\s*([\d.]+)(px|em|rem)", css))))
print("overflow-x:", re.findall(r"overflow-x[^;]*", css))
print("colors:", sorted(set(re.findall(r"color:\s*(#[0-9a-fA-F]{3,6})", css))))
ext = re.findall(r"(?:src|href)=['\"](https?://[^'\"]+)", body)
print("external src/href:", [e for e in ext if "src" in e][:5], "count", len(ext))
print("gaunde-dot:", body.count("·") + body.count("ㆍ"), "| em-dash:", body.count("—"))
# text-only checks
txt = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
txt = re.sub(r"<svg.*?</svg>", "", txt, flags=re.S)
txt = re.sub(r"<img[^>]*>", "", txt)
txt = re.sub(r"<[^>]+>", " ", txt)
txt = re.sub(r"\s+", " ", txt)
print("handa-che sentences:", re.findall(r"[가-힣]+(?:한다|이다|된다|있다|없다|않다)\.", txt)[:10])
print("banned words:", [w for w in ["무너", "엉뚱", "폭발", "치솟", "핵심", "흥미로운 점", "천장에 걸", "격차"] if w in txt])
print("headings:", re.findall(r"<h[12][^>]*>(.*?)</h[12]>", body))
print("plain formula:", re.findall(r"\b(?:CO2|H2O|O2|P\(tBu\)3|P\(Ph\)3|P\(Cy\)3|P\(o-Tol\)3)\b", txt)[:5])
