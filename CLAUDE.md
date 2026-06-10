# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Compile to PDF (runs xelatex → biber → xelatex → xelatex)
./build.sh

# Or via Make
make        # same as make all
make clean  # delete aux, log, bbl, blg files

# Manual compile sequence
xelatex main
biber main
xelatex main
xelatex main
```

Requires `texlive` (`brew install texlive` on macOS, `sudo apt-get install texlive-full` on Ubuntu).

## Architecture

This is an **XeLaTeX thesis template** for NTUT (National Taipei University of Technology). The entry point is `main.tex`, which assembles all parts in order.

**Document structure** (`main.tex` include order):
1. `page/titlepage.tex` — cover (appears twice: with and without watermark)
2. `static-page/signpage.pdf` — scanned oral defense signature form
3. `page/abstract.tex` / `page/abstract-en.tex` — Chinese and English abstracts (write page count and keywords here)
4. `page/thanks.tex` — acknowledgements
5. `page/table-of-content.tex` — TOC, list of figures, list of tables
6. `chapter/chapter1-introduction.tex` through `chapter/chapter5-conclusion.tex`
7. `page/reference.tex` — bibliography (pulls from `reference.bib` via biblatex/biber)

**Key configuration files:**
- `ntut-labels.tex` — **all thesis metadata**: title (Chinese/English), author name, advisor names, department, degree, defense year/month. Edit here first.
- `ntut-report.cls` — the custom LaTeX document class (formatting, layout). Rarely needs editing.
- `reference.bib` — BibTeX entries for all citations.
- `main.tex` — sets fonts (`DFKai-SB.ttf` for CJK, Times New Roman for Latin), geometry, and includes all parts.

**Figures** go in `figures/`. SVG originals are compiled to PDF via Inkscape and stored in `svg-inkscape/`.

**Research context** (this is an active thesis, not just a blank template):
- Thesis topic: auxiliary diagnosis of COPD using chest CT images
- Research notes/data: `COPD_quantifacation/` and `nnMamba_paper_experiment_notes/`
- Literature reference map: `參考文獻連結對照.md` (cross-references citations from `AI Meeting.md` meeting notes)
- School formatting rules: `學校論文規範/J1.pdf` (NTUT graduate thesis writing standard, v114.02.01)

## NTUT Formatting Rules (from AGENTS.md)

When editing chapters or pages, follow the official NTUT thesis standard:

- **Thesis language**: Chinese; formal academic register; no filler phrases without substance.
- **Chapter headings**: new page, centered, 20pt bold 標楷體; no punctuation or English translation in headings.
- **Section headings**: left-aligned, 18pt bold 標楷體; one blank line above, none below.
- **Fonts**: 標楷體 for Chinese, Times New Roman for English/numbers; body 12pt, thesis title 24pt; 1.5× line spacing.
- **Margins**: left/right 2.5 cm, top 2.5 cm, bottom 2.75 cm; page number centered in footer.
- **Page numbering**: title page and signature form have no numbers; front matter uses lowercase Roman numerals; body and back matter use Arabic numerals.
- **Figures/tables**: caption above tables, below figures, centered; numbered per chapter (e.g., 圖 3.1); cite as「如圖 X 所示」not「如下圖」.
- **Equations**: centered, numbered `(章.序)` (e.g., (3.1)), right-aligned number; include punctuation.
- **Abstracts**: ≤500 words / one page; no citations or figure/table references.
- **References**: must exist; cite with `[n]` brackets; follow advisor/field convention.

## Writing Guidance

When drafting or editing thesis content, consult:
- `AGENTS.md` — writing persona and constraints
- `AI Meeting.md` — meeting notes with paper/dataset/tool references
- `參考文獻連結對照.md` — organized literature links (verify full bibliographic info before citing)
- `前人paper/` — prior work papers
