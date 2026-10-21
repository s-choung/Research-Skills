"""Replace exact sentences in a docx the author has already edited, keeping every other character and its
superscript/subscript/bold formatting. Writes a new version file; never overwrites the source.

usage: python replace_sentences.py <src.docx> <out.docx> <pairs.json>
pairs.json: [["old sentence with ^{sup} _{sub} **bold** markup", "new sentence"], ...]
Each old sentence must occur exactly once, otherwise the script stops.
Pairs are applied in order to the same paragraph, so an earlier replacement can create a new match for a later
pair (e.g. renumbering Table 3 -> 4 then 4 -> 5). Make each old string specific enough to match only its target."""
import json, re, sys
import docx

def serialize(p):
    return "".join(("^{%s}" % r.text) if r.font.superscript and r.text else
                   (("_{%s}" % r.text) if r.font.subscript and r.text else
                    (("**%s**" % r.text) if r.bold and r.text else r.text)) for r in p.runs)

TOK = re.compile(r"(\*\*[^*]+\*\*|_\{[^}]*\}|\^\{[^}]*\})")
def rebuild(p, text):
    for r in p.runs[1:]: r._r.getparent().remove(r._r)
    r0 = p.runs[0]; r0.text = ""; r0.font.superscript = None; r0.font.subscript = None; r0.bold = None
    for tok in TOK.split(text):
        if not tok: continue
        r = p.add_run()
        if tok.startswith("**"): r.text = tok[2:-2]; r.bold = True
        elif tok.startswith("_{"): r.text = tok[2:-1]; r.font.subscript = True
        elif tok.startswith("^{"): r.text = tok[2:-1]; r.font.superscript = True
        else: r.text = tok

if __name__ == "__main__":
    src, out, pairs = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
    assert src != out, "write a new version file"
    d = docx.Document(src)
    hits = [0] * len(pairs)
    for p in d.paragraphs:
        if not p.runs: continue
        s = serialize(p); new = s
        for k, (a, b) in enumerate(pairs):
            if a in new: new = new.replace(a, b); hits[k] += 1
        if new != s:
            rebuild(p, new); assert serialize(p) == new
    assert all(h == 1 for h in hits), hits
    d.save(out)
    print("replaced", hits, "->", out)
