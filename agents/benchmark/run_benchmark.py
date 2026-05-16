#!/usr/bin/env python3
"""
Paper Ref-Hunter Benchmark v2
Runs HUNT (Crossref) and DISCOVERY (OpenAlex) queries, computes Top-K precision,
and generates an HTML report.
"""

import json
import time
import urllib.parse
import urllib.request
import ssl
import sys
import html as html_mod
from pathlib import Path
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

MAILTO = "ccel20260422@gmail.com"
DELAY = 1.2
BASE_DIR = Path(__file__).parent
RESULTS_PATH = BASE_DIR / "benchmark_results.json"
REPORT_PATH = BASE_DIR / "benchmark_report.html"


# ── API helpers ──────────────────────────────────────────────

def crossref_search(query_str: str, rows: int = 5) -> list[dict]:
    params = urllib.parse.urlencode({
        "query.bibliographic": query_str,
        "rows": rows,
        "select": "DOI,title,author,published-print,container-title",
        "mailto": MAILTO,
    })
    url = f"https://api.crossref.org/works?{params}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": f"PaperRefHunterBenchmark/2.0 (mailto:{MAILTO})"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("message", {}).get("items", [])
    except Exception as e:
        print(f"  [ERROR] Crossref: {e}", file=sys.stderr)
        return []


def openalex_search(query_str: str, per_page: int = 10) -> list[dict]:
    params = urllib.parse.urlencode({
        "search": query_str,
        "per_page": per_page,
        "select": "id,doi,title,authorships,publication_year,cited_by_count",
    })
    url = f"https://api.openalex.org/works?{params}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": f"PaperRefHunterBenchmark/2.0 (mailto:{MAILTO})",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return data.get("results", [])
    except Exception as e:
        print(f"  [ERROR] OpenAlex: {e}", file=sys.stderr)
        return []


# ── Matching helpers ─────────────────────────────────────────

STOP_WORDS = frozenset({
    "the", "a", "an", "of", "in", "on", "for", "and", "to", "with",
    "from", "by", "at", "is", "are", "was", "its", "as", "or", "be",
})


def _keywords(text: str) -> set[str]:
    return {w for w in text.lower().split() if w not in STOP_WORDS and len(w) > 1}


def title_match(target: str, candidate: str, threshold: float = 0.5) -> bool:
    if not target or not candidate:
        return False
    tw = _keywords(target)
    cw = _keywords(candidate)
    if not tw:
        return False
    return len(tw & cw) / len(tw) >= threshold


def topic_relevance(query: str, candidate: str, threshold: float = 0.3) -> bool:
    if not candidate:
        return False
    qw = _keywords(query)
    cw = _keywords(candidate)
    if not qw:
        return False
    return len(qw & cw) / len(qw) >= threshold


# ── HUNT mode definitions ───────────────────────────────────

HUNT_QUERIES = [
    # Norskov
    {
        "researcher": "Jens Norskov",
        "query": "Norskov oxygen reduction overpotential 2004",
        "target_title": "Origin of the Overpotential for Oxygen Reduction at a Fuel-Cell Cathode",
        "target_doi": "10.1021/jp047349j",
    },
    {
        "researcher": "Jens Norskov",
        "query": "Norskov computational catalyst design 2009",
        "target_title": "Towards the computational design of solid catalysts",
        "target_doi": "10.1038/nchem.121",
    },
    {
        "researcher": "Jens Norskov",
        "query": "Norskov universality in heterogeneous catalysis",
        "target_title": "Universality in Heterogeneous Catalysis",
        "target_doi": "10.1021/jp049517p",
    },
    {
        "researcher": "Jens Norskov",
        "query": "Norskov scaling relations adsorbates metal surfaces",
        "target_title": "Scaling Properties of Adsorption Energies for Hydrogen-Containing Molecules on Transition-Metal Surfaces",
        "target_doi": "10.1103/PhysRevLett.99.016105",
    },
    # Kitchin
    {
        "researcher": "John Kitchin",
        "query": "Kitchin machine learning catalysis 2018",
        "target_title": "Machine learning in catalysis",
        "target_doi": "10.1038/s41929-018-0056-y",
    },
    {
        "researcher": "John Kitchin",
        "query": "Kitchin strain ligand effects 2004",
        "target_title": "Role of Strain and Ligand Effects in the Modification of the Electronic and Chemical Properties of Bimetallic Surfaces",
        "target_doi": "10.1103/PhysRevLett.93.156801",
    },
    {
        "researcher": "John Kitchin",
        "query": "Kitchin high-throughput composition spread libraries 2004",
        "target_title": "High-throughput methods using composition and structure spread libraries",
        "target_doi": None,
    },
    {
        "researcher": "John Kitchin",
        "query": "Kitchin correlations coverage dependent adsorption energies 2014",
        "target_title": "Correlations in coverage-dependent atomic adsorption energies on Pd(111)",
        "target_doi": "10.1103/PhysRevB.89.115114",
    },
    # Mavrikakis
    {
        "researcher": "Manos Mavrikakis",
        "query": "Mavrikakis gold catalysis CO oxidation",
        "target_title": "Catalytic activity of Au nanoparticles",
        "target_doi": None,
    },
    {
        "researcher": "Manos Mavrikakis",
        "query": "Mavrikakis strain effect catalysis surface",
        "target_title": "Effect of Strain on the Reactivity of Metal Surfaces",
        "target_doi": "10.1103/PhysRevLett.81.2819",
    },
    {
        "researcher": "Manos Mavrikakis",
        "query": "Mavrikakis DFT methanol decomposition Pt",
        "target_title": None,
        "target_doi": None,
    },
    {
        "researcher": "Manos Mavrikakis",
        "query": "Mavrikakis water gas shift reaction mechanism copper",
        "target_title": None,
        "target_doi": None,
    },
    # Han Jeongwoo (SNU)
    {
        "researcher": "Jeongwoo Han",
        "query": "Han Jeongwoo single atom catalyst support effect",
        "target_title": None,
        "target_doi": None,
    },
    {
        "researcher": "Jeongwoo Han",
        "query": "한정우 metal oxide DFT catalysis",
        "target_title": None,
        "target_doi": None,
    },
    {
        "researcher": "Jeongwoo Han",
        "query": "Jeong Woo Han size effect single atom nanocluster Pt catalyst",
        "target_title": "Size effects of single atom and nanocluster Pt catalysts",
        "target_doi": None,
    },
    {
        "researcher": "Jeongwoo Han",
        "query": "Jeong Woo Han electronic tuning metal nanoparticles surface oxide",
        "target_title": "Electronic Tuning of Metal Nanoparticles by Surface Oxide",
        "target_doi": None,
    },
]


# ── DISCOVERY mode definitions ──────────────────────────────

DISCOVERY_QUERIES = [
    "single atom catalyst DFT screening",
    "machine learning interatomic potential",
    "oxygen evolution reaction perovskite",
    "graph neural network materials science",
    "methane activation transition metal",
]


# ── Run benchmarks ──────────────────────────────────────────

def run_hunt():
    print("=" * 60)
    print("HUNT mode — Crossref bibliographic search (top-5)")
    print("=" * 60)
    results = []
    for i, q in enumerate(HUNT_QUERIES):
        query_str = q["query"]
        print(f"\n[{i+1}/{len(HUNT_QUERIES)}] {q['researcher']}: {query_str}")
        time.sleep(DELAY)
        items = crossref_search(query_str, rows=5)

        hits = []
        found_at = None  # rank where target was found (1-indexed)
        for rank, item in enumerate(items, 1):
            t = (item.get("title") or [""])[0]
            doi = item.get("DOI", "")
            authors_raw = item.get("author", [])
            author_str = "; ".join(
                f"{a.get('family', '?')}, {a.get('given', '?')}"
                for a in authors_raw[:4]
            )
            pub_parts = item.get("published-print", {}).get("date-parts", [[None]])[0]
            year = pub_parts[0] if pub_parts else None
            journal = (item.get("container-title") or [""])[0]

            # Check match: by DOI if available, else by title overlap
            is_match = False
            if q.get("target_doi") and doi:
                is_match = doi.lower().strip() == q["target_doi"].lower().strip()
            if not is_match and q.get("target_title"):
                is_match = title_match(q["target_title"], t, 0.45)

            if is_match and found_at is None:
                found_at = rank

            tag = " *** MATCH ***" if is_match else ""
            print(f"  #{rank}: {t[:100]}{tag}")
            print(f"       {author_str[:80]} | {year} | {journal[:50]} | {doi}")

            hits.append({
                "rank": rank,
                "title": t,
                "doi": doi,
                "authors": author_str,
                "year": year,
                "journal": journal,
                "is_match": is_match,
            })

        status = f"FOUND @{found_at}" if found_at else "NOT FOUND"
        print(f"  -> {status}")

        results.append({
            "researcher": q["researcher"],
            "query": query_str,
            "target_title": q.get("target_title", ""),
            "target_doi": q.get("target_doi", ""),
            "found_at": found_at,
            "hits": hits,
        })

    return results


def run_discovery():
    print("\n" + "=" * 60)
    print("DISCOVERY mode — OpenAlex topic search (top-10)")
    print("=" * 60)
    results = []
    for i, query_str in enumerate(DISCOVERY_QUERIES):
        print(f"\n[{i+1}/{len(DISCOVERY_QUERIES)}] {query_str}")
        time.sleep(DELAY)
        items = openalex_search(query_str, per_page=10)

        hits = []
        relevant_count = 0
        for rank, item in enumerate(items, 1):
            t = item.get("title", "") or ""
            doi = (item.get("doi") or "").replace("https://doi.org/", "")
            year = item.get("publication_year", "")
            cites = item.get("cited_by_count", 0)
            authorships = item.get("authorships", [])
            lead = authorships[0].get("author", {}).get("display_name", "") if authorships else ""

            rel = topic_relevance(query_str, t, 0.3)
            if rel:
                relevant_count += 1

            tag = "REL" if rel else "---"
            print(f"  #{rank} [{tag}] {t[:100]}")
            print(f"       {lead} ({year}) | Cited: {cites} | {doi}")

            hits.append({
                "rank": rank,
                "title": t,
                "doi": doi,
                "year": year,
                "cited_by_count": cites,
                "lead_author": lead,
                "relevant": rel,
            })

        rate = relevant_count / len(hits) if hits else 0
        print(f"  -> {relevant_count}/{len(hits)} relevant ({rate:.0%})")

        results.append({
            "query": query_str,
            "total": len(hits),
            "relevant_count": relevant_count,
            "relevance_rate": rate,
            "hits": hits,
        })

    return results


# ── Top-K metrics ───────────────────────────────────────────

def compute_hunt_topk(hunt_results):
    """Compute Top-K precision for HUNT queries that have a known target."""
    # Only count queries that have a defined target (title or DOI)
    targeted = [r for r in hunt_results if r.get("target_title") or r.get("target_doi")]
    n = len(targeted)
    if n == 0:
        return {"@1": 0, "@3": 0, "@5": 0, "n": 0}
    at1 = sum(1 for r in targeted if r["found_at"] is not None and r["found_at"] <= 1)
    at3 = sum(1 for r in targeted if r["found_at"] is not None and r["found_at"] <= 3)
    at5 = sum(1 for r in targeted if r["found_at"] is not None and r["found_at"] <= 5)
    return {
        "@1": at1 / n,
        "@3": at3 / n,
        "@5": at5 / n,
        "n": n,
        "at1": at1,
        "at3": at3,
        "at5": at5,
    }


def compute_discovery_topk(discovery_results):
    """Compute relevance@10 for DISCOVERY queries."""
    total_hits = sum(r["total"] for r in discovery_results)
    total_rel = sum(r["relevant_count"] for r in discovery_results)
    rate = total_rel / total_hits if total_hits > 0 else 0
    return {
        "@10": rate,
        "total_hits": total_hits,
        "total_relevant": total_rel,
    }


# ── HTML generation ─────────────────────────────────────────

def esc(text):
    return html_mod.escape(str(text)) if text else ""


def generate_html(hunt_results, discovery_results, hunt_topk, disc_topk, timestamp):
    """Generate the benchmark HTML report."""

    # Group HUNT results by researcher
    researchers_order = []
    hunt_by_researcher = {}
    for r in hunt_results:
        name = r["researcher"]
        if name not in hunt_by_researcher:
            hunt_by_researcher[name] = []
            researchers_order.append(name)
        hunt_by_researcher[name].append(r)

    # Per-researcher stats
    researcher_stats = {}
    for name, queries in hunt_by_researcher.items():
        targeted = [q for q in queries if q.get("target_title") or q.get("target_doi")]
        n = len(targeted)
        at1 = sum(1 for q in targeted if q["found_at"] is not None and q["found_at"] <= 1)
        at3 = sum(1 for q in targeted if q["found_at"] is not None and q["found_at"] <= 3)
        at5 = sum(1 for q in targeted if q["found_at"] is not None and q["found_at"] <= 5)
        researcher_stats[name] = {"n": n, "at1": at1, "at3": at3, "at5": at5}

    # Build HUNT cards HTML
    hunt_cards_html = ""
    for name in researchers_order:
        queries = hunt_by_researcher[name]
        stats = researcher_stats[name]
        hunt_cards_html += f'<h3 class="researcher-name">{esc(name)}'
        if stats["n"] > 0:
            hunt_cards_html += f' <span class="stat-badge">{stats["at3"]}/{stats["n"]} @3</span>'
        hunt_cards_html += '</h3>\n'

        for q in queries:
            found = q["found_at"]
            status_cls = "hit" if found else "miss"
            status_txt = f"Found @{found}" if found else "Not found"
            target_line = ""
            if q.get("target_title"):
                target_line = f'<div class="target-line">Target: {esc(q["target_title"])}</div>'

            hits_rows = ""
            for h in q["hits"]:
                match_cls = ' class="match-row"' if h["is_match"] else ""
                match_icon = "&#x2705;" if h["is_match"] else f'<span class="rank-num">#{h["rank"]}</span>'
                doi_link = f'<a href="https://doi.org/{esc(h["doi"])}" target="_blank">{esc(h["doi"])}</a>' if h["doi"] else "—"
                hits_rows += f"""<tr{match_cls}>
                    <td class="rank-cell">{match_icon}</td>
                    <td>{esc(h["title"])}</td>
                    <td class="meta-cell">{esc(h["authors"][:60])}</td>
                    <td class="meta-cell">{h["year"] or "—"}</td>
                    <td class="meta-cell">{esc(h["journal"][:40])}</td>
                    <td class="meta-cell doi-cell">{doi_link}</td>
                </tr>"""

            hunt_cards_html += f"""
            <details class="result-card">
                <summary>
                    <span class="query-text">{esc(q["query"])}</span>
                    <span class="status-pill {status_cls}">{status_txt}</span>
                </summary>
                <div class="card-body">
                    {target_line}
                    <table class="hits-table">
                        <thead><tr><th>#</th><th>Title</th><th>Authors</th><th>Year</th><th>Journal</th><th>DOI</th></tr></thead>
                        <tbody>{hits_rows}</tbody>
                    </table>
                </div>
            </details>"""

    # Build DISCOVERY cards HTML
    disc_cards_html = ""
    for r in discovery_results:
        rel_count = r["relevant_count"]
        total = r["total"]
        rate = r["relevance_rate"]

        hits_rows = ""
        for h in r["hits"]:
            rel_cls = ' class="match-row"' if h["relevant"] else ""
            rel_icon = "&#x2705;" if h["relevant"] else "&#x2796;"
            doi_link = f'<a href="https://doi.org/{esc(h["doi"])}" target="_blank">{esc(h["doi"])}</a>' if h["doi"] else "—"
            hits_rows += f"""<tr{rel_cls}>
                <td class="rank-cell">{rel_icon}</td>
                <td>{esc(h["title"])}</td>
                <td class="meta-cell">{esc(h["lead_author"])}</td>
                <td class="meta-cell">{h["year"] or "—"}</td>
                <td class="meta-cell">{h["cited_by_count"]:,}</td>
                <td class="meta-cell doi-cell">{doi_link}</td>
            </tr>"""

        disc_cards_html += f"""
        <details class="result-card">
            <summary>
                <span class="query-text">{esc(r["query"])}</span>
                <span class="stat-badge">{rel_count}/{total} relevant ({rate:.0%})</span>
            </summary>
            <div class="card-body">
                <table class="hits-table">
                    <thead><tr><th></th><th>Title</th><th>Lead Author</th><th>Year</th><th>Cited</th><th>DOI</th></tr></thead>
                    <tbody>{hits_rows}</tbody>
                </table>
            </div>
        </details>"""

    # Per-researcher table rows
    researcher_rows = ""
    for name in researchers_order:
        s = researcher_stats[name]
        if s["n"] == 0:
            continue
        researcher_rows += f"""<tr>
            <td>{esc(name)}</td>
            <td>{s["n"]}</td>
            <td>{s["at1"]}/{s["n"]} ({s["at1"]/s["n"]:.0%})</td>
            <td>{s["at3"]}/{s["n"]} ({s["at3"]/s["n"]:.0%})</td>
            <td>{s["at5"]}/{s["n"]} ({s["at5"]/s["n"]:.0%})</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Paper Ref-Hunter Benchmark</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #ffffff;
  --fg: #111827;
  --muted: #6b7280;
  --border: #e5e7eb;
  --surface: #f9fafb;
  --green: #059669;
  --green-bg: #ecfdf5;
  --red: #dc2626;
  --red-bg: #fef2f2;
  --blue: #2563eb;
  --blue-bg: #eff6ff;
  --font: 'Inter', system-ui, -apple-system, sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, monospace;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font);
  font-size: 14px;
  line-height: 1.65;
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
  -webkit-font-smoothing: antialiased;
}}
h1 {{
  font-size: 1.75rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 0.25rem;
}}
.subtitle {{
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 2rem;
}}
h2 {{
  font-size: 1.15rem;
  font-weight: 600;
  margin: 2rem 0 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}
h3.researcher-name {{
  font-size: 0.95rem;
  font-weight: 500;
  margin: 1.25rem 0 0.5rem;
  color: var(--fg);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}

/* Summary table */
.summary-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0.75rem 0 1.5rem;
  font-size: 0.85rem;
}}
.summary-table th {{
  background: var(--surface);
  font-weight: 500;
  text-align: left;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}
.summary-table td {{
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.82rem;
}}
.summary-table tr:hover td {{ background: var(--surface); }}
.summary-table .total-row td {{
  font-weight: 600;
  background: var(--surface);
}}

/* Result cards */
details.result-card {{
  border: 1px solid var(--border);
  border-radius: 6px;
  margin-bottom: 0.5rem;
  overflow: hidden;
}}
details.result-card summary {{
  padding: 0.6rem 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  font-size: 0.85rem;
  background: var(--bg);
  transition: background 0.15s;
}}
details.result-card summary:hover {{ background: var(--surface); }}
details.result-card[open] summary {{ border-bottom: 1px solid var(--border); }}
.query-text {{
  font-family: var(--mono);
  font-size: 0.82rem;
  color: var(--fg);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}}
.status-pill {{
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.status-pill.hit {{ background: var(--green-bg); color: var(--green); }}
.status-pill.miss {{ background: var(--red-bg); color: var(--red); }}
.stat-badge {{
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: var(--blue-bg);
  color: var(--blue);
  white-space: nowrap;
  flex-shrink: 0;
}}
.card-body {{
  padding: 0.75rem;
  background: var(--surface);
}}
.target-line {{
  font-size: 0.8rem;
  color: var(--muted);
  margin-bottom: 0.5rem;
  font-style: italic;
}}

/* Hits table */
.hits-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
}}
.hits-table th {{
  text-align: left;
  padding: 0.35rem 0.5rem;
  border-bottom: 1px solid var(--border);
  color: var(--muted);
  font-weight: 500;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}
.hits-table td {{
  padding: 0.35rem 0.5rem;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}}
.hits-table tr:last-child td {{ border-bottom: none; }}
.hits-table tr.match-row td {{ background: var(--green-bg); }}
.rank-cell {{ text-align: center; width: 2rem; }}
.rank-num {{ color: var(--muted); }}
.meta-cell {{ color: var(--muted); white-space: nowrap; }}
.doi-cell {{ font-family: var(--mono); font-size: 0.72rem; }}
.doi-cell a {{ color: var(--blue); text-decoration: none; }}
.doi-cell a:hover {{ text-decoration: underline; }}

/* Language toggle */
.lang-toggle {{
  display: inline-flex;
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  font-size: 0.78rem;
  margin-bottom: 1rem;
}}
.lang-btn {{
  padding: 0.3rem 0.75rem;
  cursor: pointer;
  background: var(--bg);
  border: none;
  font-family: var(--font);
  font-size: 0.78rem;
  color: var(--muted);
  transition: all 0.15s;
}}
.lang-btn:not(:last-child) {{ border-right: 1px solid var(--border); }}
.lang-btn.active {{ background: var(--fg); color: #fff; }}

.lang-en, .lang-ko {{ display: none; }}
body.en .lang-en {{ display: block; }}
body.ko .lang-ko {{ display: block; }}
body.en span.lang-en, body.ko span.lang-ko {{ display: inline; }}

footer {{
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  font-size: 0.78rem;
  color: var(--muted);
}}
</style>
</head>
<body class="en">

<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
  <div>
    <h1>Paper Ref-Hunter Benchmark</h1>
    <p class="subtitle">
      <span class="lang-en">Crossref HUNT + OpenAlex DISCOVERY — real API results, Top-K precision</span>
      <span class="lang-ko">Crossref HUNT + OpenAlex DISCOVERY — 실제 API 결과, Top-K 정밀도</span>
    </p>
  </div>
  <div class="lang-toggle">
    <button class="lang-btn active" data-lang="en">ENG</button>
    <button class="lang-btn" data-lang="ko">KOR</button>
  </div>
</div>

<!-- ── TOP-K SUMMARY ── -->
<h2>
  <span class="lang-en">Top-K Precision Summary</span>
  <span class="lang-ko">Top-K 정밀도 요약</span>
</h2>
<table class="summary-table">
  <thead>
    <tr>
      <th>Mode</th>
      <th>Queries</th>
      <th>@1</th>
      <th>@3</th>
      <th>@5</th>
      <th>@10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>HUNT (Crossref)</td>
      <td>{hunt_topk["n"]}</td>
      <td>{hunt_topk["at1"]}/{hunt_topk["n"]} ({hunt_topk["@1"]:.0%})</td>
      <td>{hunt_topk["at3"]}/{hunt_topk["n"]} ({hunt_topk["@3"]:.0%})</td>
      <td>{hunt_topk["at5"]}/{hunt_topk["n"]} ({hunt_topk["@5"]:.0%})</td>
      <td>—</td>
    </tr>
    <tr>
      <td>DISCOVERY (OpenAlex)</td>
      <td>{len(discovery_results)}</td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
      <td>{disc_topk["total_relevant"]}/{disc_topk["total_hits"]} ({disc_topk["@10"]:.0%})</td>
    </tr>
  </tbody>
</table>

<!-- ── PER-RESEARCHER BREAKDOWN ── -->
<h2>
  <span class="lang-en">HUNT — Per-Researcher Breakdown</span>
  <span class="lang-ko">HUNT — 연구자별 결과</span>
</h2>
<table class="summary-table">
  <thead>
    <tr><th>Researcher</th><th>Queries</th><th>@1</th><th>@3</th><th>@5</th></tr>
  </thead>
  <tbody>
    {researcher_rows}
    <tr class="total-row">
      <td>Total</td>
      <td>{hunt_topk["n"]}</td>
      <td>{hunt_topk["at1"]}/{hunt_topk["n"]} ({hunt_topk["@1"]:.0%})</td>
      <td>{hunt_topk["at3"]}/{hunt_topk["n"]} ({hunt_topk["@3"]:.0%})</td>
      <td>{hunt_topk["at5"]}/{hunt_topk["n"]} ({hunt_topk["@5"]:.0%})</td>
    </tr>
  </tbody>
</table>

<!-- ── HUNT RESULTS ── -->
<h2>
  <span class="lang-en">HUNT Results — Full Query Details</span>
  <span class="lang-ko">HUNT 결과 — 쿼리별 상세</span>
</h2>
<p style="font-size:0.82rem;color:var(--muted);margin-bottom:0.75rem;">
  <span class="lang-en">Click a query to expand and see all returned results. Green rows indicate a match with the target paper.</span>
  <span class="lang-ko">쿼리를 클릭하면 반환된 전체 결과를 볼 수 있습니다. 녹색 행이 타겟 논문과 일치하는 결과입니다.</span>
</p>
{hunt_cards_html}

<!-- ── DISCOVERY RESULTS ── -->
<h2>
  <span class="lang-en">DISCOVERY Results — Topic Search Details</span>
  <span class="lang-ko">DISCOVERY 결과 — 토픽 검색 상세</span>
</h2>
<p style="font-size:0.82rem;color:var(--muted);margin-bottom:0.75rem;">
  <span class="lang-en">Click a topic to expand. Relevance is measured by keyword overlap between the query and each result title.</span>
  <span class="lang-ko">토픽을 클릭하면 펼쳐집니다. 관련성은 쿼리와 결과 제목 간 키워드 겹침으로 측정합니다.</span>
</p>
{disc_cards_html}

<footer>
  <span class="lang-en">Generated {timestamp} &mdash; Crossref Bibliographic API + OpenAlex Works API &mdash; Paper Ref-Hunter Benchmark v2</span>
  <span class="lang-ko">생성: {timestamp} &mdash; Crossref Bibliographic API + OpenAlex Works API &mdash; Paper Ref-Hunter Benchmark v2</span>
</footer>

<script>
document.querySelectorAll('.lang-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.body.className = btn.dataset.lang;
  }});
}});
</script>
</body>
</html>"""

    return html


# ── Main ────────────────────────────────────────────────────

if __name__ == "__main__":
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Paper Ref-Hunter Benchmark v2 — {ts}\n")

    hunt_results = run_hunt()
    discovery_results = run_discovery()

    hunt_topk = compute_hunt_topk(hunt_results)
    disc_topk = compute_discovery_topk(discovery_results)

    print("\n" + "=" * 60)
    print("TOP-K SUMMARY")
    print("=" * 60)
    print(f"HUNT @1={hunt_topk['@1']:.0%}  @3={hunt_topk['@3']:.0%}  @5={hunt_topk['@5']:.0%}  (n={hunt_topk['n']})")
    print(f"DISCOVERY @10={disc_topk['@10']:.0%}  ({disc_topk['total_relevant']}/{disc_topk['total_hits']})")

    # Save JSON
    output = {
        "timestamp": ts,
        "hunt_results": hunt_results,
        "discovery_results": discovery_results,
        "hunt_topk": hunt_topk,
        "discovery_topk": disc_topk,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nJSON saved: {RESULTS_PATH}")

    # Generate HTML
    html = generate_html(hunt_results, discovery_results, hunt_topk, disc_topk, ts)
    with open(REPORT_PATH, "w") as f:
        f.write(html)
    print(f"HTML saved: {REPORT_PATH}")
    print(f"\nDone at {datetime.now().strftime('%H:%M:%S')}")
