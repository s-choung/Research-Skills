---
name: paper-bib
description: Generate BibTeX entries from DOI or paper title
argument-hint: "<DOI, title, or paper-ref output>"
allowed-tools: Read, Edit, Write, Bash, Grep
---

## Task

User invoked: `/paper-bib $ARGUMENTS`

Treat `$ARGUMENTS` as one or more DOIs, paper titles, or pasted `/paper-ref` output.

1. Parse the input to extract DOIs or titles.
2. For each, fetch metadata from Crossref API (`https://api.crossref.org/works/{DOI}`).
3. Format as BibTeX entries following the rules in the paper-bib skill.
4. If `--file <path>` is specified, append to that `.bib` file (checking for duplicates first).
5. Otherwise, print the BibTeX entries as a code block.

Refer to `skills/paper-bib/SKILL.md` for full formatting rules, edge cases, and examples.
