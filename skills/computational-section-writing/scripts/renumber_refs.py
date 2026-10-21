"""Renumber superscript citations by first appearance and reorder the reference list, in place.
usage: python renumber_refs.py <docx>"""
import re, sys
import docx
F = sys.argv[1]
d = docx.Document(F)
P = d.paragraphs
texts = [p.text for p in P]
i_abs = texts.index("Abstract"); i_refs = texts.index("References")
def expand(s):
    out = []
    for part in s.split(","):
        if "-" in part: a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else: out.append(int(part))
    return out
def compress(nums):
    nums = sorted(nums); parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        parts.append(str(nums[i]) if j == i else ("%d,%d" % (nums[i], nums[j]) if j == i + 1 else "%d-%d" % (nums[i], nums[j])))
        i = j + 1
    return ",".join(parts)
cite_runs, first = [], []
for p in P[i_abs:i_refs]:
    for r in p.runs:
        t = r.text.strip()
        if r.font.superscript and re.fullmatch(r"\d+([,-]\d+)*", t):
            nums = expand(t); cite_runs.append((r, nums))
            for n in nums:
                if n not in first: first.append(n)
ref_ps = [p for p in P[i_refs + 1:] if re.match(r"^\d+\.\t", p.text)]
for n in range(1, len(ref_ps) + 1):
    if n not in first: first.append(n)
old2new = {old: k + 1 for k, old in enumerate(first)}
for r, nums in cite_runs: r.text = compress(old2new[n] for n in nums)
body = ref_ps[0]._p.getparent(); anchor = P[i_refs]._p
elems = {int(p.text.split(".")[0]): p._p for p in ref_ps}
for e in elems.values(): body.remove(e)
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
for new in range(1, len(ref_ps) + 1):
    e = elems[first[new - 1]]; anchor.addnext(e); anchor = e
    t0 = e.findall(".//" + W)[0]; t0.text = re.sub(r"^\d+\.", "%d." % new, t0.text)
d.save(F)
print("changed:", {o: n for o, n in old2new.items() if o != n})
