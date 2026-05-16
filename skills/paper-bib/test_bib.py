"""
Test script for paper-bib skill.
Fetches metadata from Crossref API for 3 real DOIs and formats as BibTeX.
"""

import json
import re
import unicodedata
import urllib.request
import urllib.error
import urllib.parse


DOIS = [
    # Choung et al., CatBench, Cell Reports Physical Science 2025
    "10.1016/j.xcrp.2025.102968",
    # Reproducibility in DFT calculations, Science 2016
    "10.1126/science.aad3000",
    # In Situ/Operando electrocatalyst characterization, Chemical Reviews 2021
    "10.1021/acs.chemrev.0c00396",
]

SKIP_WORDS = {"a", "an", "the", "on", "in", "of", "for", "and", "to", "with", "from", "by"}


def fetch_crossref(doi: str) -> dict:
    """Fetch work metadata from Crossref API."""
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "paper-bib-test/1.0 (mailto:ccel20260422@gmail.com)",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    return data["message"]


def strip_diacritics(s: str) -> str:
    """Remove diacritics and return ASCII-only lowercase string."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def make_citation_key(authors: list, year: int, title: str) -> str:
    """Generate citation key: firstauthorlastname + year + first significant title word."""
    if authors:
        last = authors[0].get("family", "unknown")
        last = strip_diacritics(last).replace(" ", "")
    else:
        last = "unknown"

    words = re.findall(r"[a-zA-Z]+", title)
    first_word = "untitled"
    for w in words:
        if w.lower() not in SKIP_WORDS:
            first_word = w.lower()
            break

    return f"{last}{year}{first_word}"


def format_authors(authors: list) -> str:
    """Format author list as 'LastName, FirstName and ...'."""
    parts = []
    for a in authors:
        family = a.get("family", "")
        given = a.get("given", "")
        if family and given:
            parts.append(f"{family}, {given}")
        elif family:
            parts.append(family)
    return " and ".join(parts)


def extract_year(msg: dict) -> int:
    """Extract publication year from Crossref message."""
    for key in ("published-print", "published-online", "created"):
        dp = msg.get(key, {}).get("date-parts", [[]])
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return 0


def format_pages(page_str: str) -> str:
    """Normalize page ranges to use BibTeX en-dash."""
    if not page_str:
        return ""
    return page_str.replace("-", "--").replace("----", "--")


def crossref_type_to_bibtex(ctype: str) -> str:
    """Map Crossref type to BibTeX entry type."""
    mapping = {
        "journal-article": "article",
        "proceedings-article": "inproceedings",
        "book-chapter": "incollection",
        "book": "book",
        "posted-content": "misc",
        "report": "techreport",
    }
    return mapping.get(ctype, "misc")


def format_bibtex(msg: dict) -> str:
    """Format Crossref message as a BibTeX entry string."""
    entry_type = crossref_type_to_bibtex(msg.get("type", ""))
    authors = msg.get("author", [])
    title = msg.get("title", ["Untitled"])[0]
    year = extract_year(msg)
    key = make_citation_key(authors, year, title)

    fields = []
    fields.append(f"  author    = {{{format_authors(authors)}}}")
    fields.append(f"  title     = {{{{{title}}}}}")

    journal = msg.get("container-title", [""])
    if journal and journal[0]:
        fields.append(f"  journal   = {{{journal[0]}}}")

    volume = msg.get("volume", "")
    if volume:
        fields.append(f"  volume    = {{{volume}}}")

    number = msg.get("issue", "")
    if number:
        fields.append(f"  number    = {{{number}}}")

    pages = format_pages(msg.get("page", ""))
    if pages:
        fields.append(f"  pages     = {{{pages}}}")

    fields.append(f"  year      = {{{year}}}")

    doi = msg.get("DOI", "")
    if doi:
        fields.append(f"  doi       = {{{doi}}}")
        fields.append(f"  url       = {{https://doi.org/{doi}}}")

    missing = []
    if not volume:
        missing.append("volume")
    if not pages:
        missing.append("pages")
    if not number:
        missing.append("number")

    body = ",\n".join(fields)
    entry = f"@{entry_type}{{{key},\n{body},\n}}"

    if missing:
        entry += f"\n% WARNING: Missing fields: {', '.join(missing)}"

    return entry


def main():
    print("=" * 70)
    print("paper-bib test: Fetching BibTeX entries from Crossref")
    print("=" * 70)

    for doi in DOIS:
        print(f"\n--- DOI: {doi} ---\n")
        try:
            msg = fetch_crossref(doi)
            bibtex = format_bibtex(msg)
            print(bibtex)
        except urllib.error.HTTPError as e:
            print(f"ERROR: HTTP {e.code} for DOI {doi}")
        except Exception as e:
            print(f"ERROR: {e}")
        print()

    print("=" * 70)
    print("Test complete.")


if __name__ == "__main__":
    main()
