# CV / Resume Workspace

- `CV_ENTRY_BANK.md`: reusable candidate bullets with source mappings
- `CV_ENTRY_AUDIT.md`: target-specific requirement-to-evidence decisions
- `*.tex`: actual resume / CV sources
- `tools/`: TeX dependency, page-count, PDF bounding-box, and text-extraction checks

First identify whether the target is an industry resume, academic CV, or another format, then follow the recipient's page and file requirements. Layout diagnostics do not mean every page must be filled to the bottom.

Record the expected reader path in `CV_ENTRY_AUDIT.md` before drafting. The first bullet should let recruiting/HR and non-specialist leaders understand the problem, scope, ownership, and value; later bullets should give team leads, technical interviewers, and potential peers/cross-functional partners evidence of tradeoffs, validation, interfaces, quality, and team leverage. Every claim must survive accurate interview follow-up, and a team result must not be presented as entirely individual.

```powershell
python cv/tools/setup_tex_dependencies.py --json
python cv/tools/setup_tex_dependencies.py --smoke --json
python cv/tools/detect_tex_dependencies.py cv/cv.tex --json
python cv/tools/check_tex_pages.py cv/cv.tex --target-pages 1 --output cv/check.pdf --render-dir cv/rendered --json
python cv/tools/check_resume_layout.py cv/check.pdf --render-dir cv/rendered --json
```

Layout acceptance covers more than page count: review three lines on both sides of every break, stranded headings/entries, split bullets, whether every page reaches the bottom band without entering the safety margin, cross-page density, compile warnings, font embedding, links, and extracted reading order. Then inspect every PNG in `cv/rendered/` for clipping, overlap, missing glyphs, black boxes, hierarchy, and spacing. Correct content and semantic breaks first, consistent spacing second, and margins/type size last; never use filler or scattered negative spacing to force page fill.

The setup helper only detects by default. Run `python cv/tools/setup_tex_dependencies.py --install --yes` only after reviewing the proposed commands and obtaining explicit user confirmation. TeX distributions can be large, may require elevation and a terminal restart, and must not silently replace an existing partial installation.
