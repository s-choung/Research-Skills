---
name: paper-bib
description: Generate verified BibTeX entries from DOI, title, or paper-ref output
triggers:
  - /paper-bib
  - bib 생성
  - bibtex 만들어
  - DOI to bib
  - 참고문헌 bib
allowed-tools: Read, Edit, Write, Bash, Grep
---

# paper-bib

Generate properly formatted BibTeX entries from DOI, paper title, or `/paper-ref` output. Verify metadata via Crossref API and optionally append to an existing `.bib` file.

## Input formats

The user may provide one or more of the following:

1. **DOI** — e.g. `10.1038/s41929-023-01045-5`
2. **Paper title** — e.g. "Unravelling the role of metal–support interactions..."
3. **paper-ref-hunter output** — a markdown table with columns like Title, DOI, Year, etc.
4. **Mixed list** — multiple DOIs/titles, one per line or comma-separated

## Workflow

### Step 1. Extract DOIs

- If input is a DOI string (matches `10.\d{4,}/\S+`), use directly.
- If input is a title, search Crossref: `https://api.crossref.org/works?query.title=<URL-encoded-title>&rows=3`
  - Pick the top result whose title fuzzy-matches (>80% overlap).
  - If no match, warn and ask user to provide DOI manually.
- If input is a `/paper-ref` table, extract DOI column values.

### Step 2. Fetch metadata from Crossref

For each DOI, fetch:

```
https://api.crossref.org/works/{DOI}
```

Extract from the `message` object:
- `type` → determines BibTeX entry type (see mapping below)
- `title[0]` → title
- `author[]` → list of `{given, family}` pairs
- `container-title[0]` → journal name
- `volume`, `issue`, `page` → standard fields
- `published-print.date-parts[0]` or `published-online.date-parts[0]` → year
- `DOI` → doi field
- `publisher` → publisher (for books/proceedings)
- `URL` → url field

### Step 3. Determine entry type

| Crossref `type`       | BibTeX type       |
|----------------------|-------------------|
| `journal-article`    | `@article`        |
| `proceedings-article` | `@inproceedings` |
| `book-chapter`       | `@incollection`   |
| `book`               | `@book`           |
| `posted-content` (preprint) | `@misc`   |
| `report`             | `@techreport`     |
| other                | `@misc`           |

### Step 4. Format BibTeX entry

#### Citation key

Format: `{FirstAuthorLastName}{Year}{FirstTitleWord}`
- FirstAuthorLastName: ASCII-only, lowercase. Remove diacritics. E.g. `müller` → `muller`.
- Year: 4-digit year.
- FirstTitleWord: first significant word of title (skip articles: a, an, the, on, in, of, for).
- Example: `choung2023unravelling`

#### Author format

```
author = {LastName, FirstName and LastName, FirstName and ...},
```

- Use `family` and `given` from Crossref.
- If `given` is missing, use initials or just family name.
- For consortium/group authors, use `{Organization Name}` with braces.

#### Template

```bibtex
@article{key,
  author    = {LastName1, FirstName1 and LastName2, FirstName2},
  title     = {{Title with Braces for Capitalization}},
  journal   = {Journal Name},
  volume    = {V},
  number    = {N},
  pages     = {start--end},
  year      = {YYYY},
  doi       = {10.xxxx/yyyy},
  url       = {https://doi.org/10.xxxx/yyyy},
}
```

Notes:
- Title wrapped in double braces `{{...}}` to preserve capitalization.
- Pages use en-dash `--`.
- Trailing comma after last field (BibTeX tolerates this).
- Two-space indentation for fields.

### Step 5. Handle edge cases

#### ArXiv preprints
- If DOI is missing but arXiv ID is available, use:
  ```bibtex
  @misc{key,
    author       = {...},
    title        = {{...}},
    year         = {YYYY},
    eprint       = {XXXX.XXXXX},
    archiveprefix = {arXiv},
    primaryclass = {cond-mat.mtrl-sci},
  }
  ```
- Try Crossref first; if 404, try `https://export.arxiv.org/api/query?id_list=XXXX.XXXXX`

#### Missing fields
- If `volume`, `number`, or `pages` are missing, omit those fields (do NOT insert placeholders).
- If `year` is missing from both `published-print` and `published-online`, check `created.date-parts`.
- Always warn the user about missing fields: `⚠ Missing: volume, pages`

#### Preprints / posted-content
- Use `@misc` with `note = {Preprint}` and `howpublished = {\url{...}}` if no journal.

#### Duplicate detection
- Before appending to a `.bib` file, read the file and check if any existing entry has the same DOI.
- If duplicate found, warn and skip (do not overwrite).

### Step 6. Output

#### Default (no .bib file specified)
Print the BibTeX entry to the conversation. Format as a code block.

#### Append to .bib file
If user specifies a `.bib` file path (or one is found in the current project):
1. Read the existing file.
2. Check for duplicate DOIs.
3. Append new entries at the end, separated by a blank line.
4. Report what was added.

Auto-detect: look for `*.bib` files in the project root or `archive/06_references/`.

## Batch mode

When multiple DOIs/titles are provided:
1. Process each sequentially.
2. Collect all entries.
3. Print or append all at once.
4. Report summary: N entries generated, M skipped (duplicates), K warnings (missing fields).

## Error handling

- **Crossref 404**: DOI not found. Ask user to verify.
- **Crossref rate limit**: Wait and retry once. If still failing, report.
- **Network error**: Report and suggest user check connectivity.
- **Malformed DOI**: Regex-validate before calling API. Strip leading `https://doi.org/` if present.

## Integration with paper-ref

When receiving output from `/paper-ref`, parse the markdown table:
- Extract DOI column values.
- Process each DOI through the standard workflow.
- Return BibTeX entries in the same order as the table rows.

## Examples

User: `/paper-bib 10.1038/s41929-023-01045-5`

Output:
```bibtex
@article{choung2023unravelling,
  author    = {Choung, Seokhyun and Park, Jeong-Myeong and ...},
  title     = {{Unravelling the role of metal--support interactions ...}},
  journal   = {Nature Catalysis},
  volume    = {6},
  pages     = {1082--1093},
  year      = {2023},
  doi       = {10.1038/s41929-023-01045-5},
  url       = {https://doi.org/10.1038/s41929-023-01045-5},
}
```

User: `/paper-bib "machine learning interatomic potentials" --file refs.bib`

→ Search title on Crossref → fetch top match → format → append to `refs.bib`.
