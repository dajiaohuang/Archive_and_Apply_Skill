# Resume Layout QA and Correction

Read this reference whenever a resume/CV is compiled, visually reviewed, or adjusted for page count.

## Acceptance model

A resume is not layout-ready merely because it compiles or matches a target page count. Require all three layers:

1. **Deterministic checks:** clean compilation, expected page count and size, extractable text, safe edge margins, embedded fonts, valid link targets, and no obvious text-box overlap.
2. **Page-break review:** inspect the last three lines before and first three lines after every break. Reject stranded section or entry headings, a heading with only one following line, lone bullets, awkward bullet/paragraph splits, and a continuation page that starts or ends with excessive whitespace.
3. **Rendered visual review:** inspect every PNG page for clipping, overlap, missing glyphs, black squares, alignment, hierarchy, spacing rhythm, and balance. Automated bounding boxes cannot certify appearance.

## Page fill and density

- Compare each page's final text baseline with the intended bottom margin. A practical default is a 0.5-inch safety margin plus at most 0.35 inch of additional whitespace.
- Treat an internal page that ends substantially above that band as a pagination defect unless an explicit format requires the break.
- Treat a sparse final page as a signal to reconsider the page count, selection, and ordering. Do not add filler or stretch spacing merely to reach the bottom.
- Compare fill ratios across pages. Large differences often mean that a section should move as a unit or the document should use a different page count.
- Preserve readable top, left, and right margins; content reaching the bottom is not permission to invade the safety area.

These thresholds are diagnostics. Explicit employer, academic, regional, accessibility, or print requirements override them.

## Break-quality rules

Keep these units together where practical:

- section heading plus at least two content lines
- employer/project/degree heading plus role line and first bullet
- a short bullet or paragraph that would otherwise leave one line on either page
- a date aligned with the entry it belongs to

For TeX templates, prefer semantic break controls. The maintained `needspace` package provides this behavior when it is already available:

```tex
\usepackage{needspace}
\newcommand{\cvsection}[1]{\Needspace{4\baselineskip}\section{#1}}
\clubpenalty=10000
\widowpenalty=10000
\brokenpenalty=10000
```

Use `\Needspace{3\baselineskip}` or `\Needspace{4\baselineskip}` before an entry heading. Use a manual `\pagebreak` only after deciding the correct semantic break; never scatter forced breaks to hide unresolved content or spacing problems.

The bundled templates avoid adding another package dependency by defining a small `\cvneedspace` helper from `\pagegoal` and `\pagetotal`; preserve that helper when starting from those templates.

## Other checks

- **Compilation log:** resolve overfull boxes, missing characters, undefined references, and repeated rerun warnings. Review underfull boxes rather than suppressing them blindly.
- **Typography:** keep body size, line height, capitalization, date style, punctuation, bullet indentation, and section spacing consistent. Avoid solving overflow with unreadably small type.
- **Horizontal safety:** check long URLs, email addresses, dates, skill lists, and unbreakable technical tokens for right-edge overflow.
- **Text/ATS:** copy text from every page and verify reading order, Unicode, bullets, dates, and contact details. Font embedding and extraction success improve portability but do not guarantee ATS behavior.
- **Links:** verify email, portfolio, GitHub, LinkedIn, publication, and project links point to the intended target and that private tracking URLs are not exposed.
- **Visual defects:** check for clipped descenders, overlapping rules, broken CJK glyphs, black boxes, inconsistent bold/italic rendering, and unusually large internal gaps.
- **Document consistency:** confirm page size/orientation, header/footer behavior, page numbering policy, and filename match the recipient's instructions.

## Correction order

Correct the cause with the least damaging change:

1. Remove unsupported, redundant, or target-irrelevant content.
2. Rewrite verbose bullets without weakening evidence or inventing metrics.
3. Reorder or move whole semantic units to improve breaks.
4. Add `\Needspace`/widow-orphan controls or one intentional page break.
5. Tune list and section spacing modestly and consistently.
6. Adjust margins or type size only when recipient constraints allow it; preserve readability and visual hierarchy.

Do not use filler, arbitrary vertical space, negative spacing scattered through the document, or global typography shrinkage as the first fix.

## Required iteration loop

1. Compile and capture the TeX diagnostics.
2. Run the comprehensive layout checker and render every page:

   ```bash
   python cv/tools/check_tex_pages.py cv/cv.tex --target-pages 2 --output cv/check.pdf --render-dir cv/rendered --json
   ```

   For an existing PDF:

   ```bash
   python cv/tools/check_resume_layout.py cv/check.pdf --render-dir cv/rendered --json
   ```

3. Inspect every rendered page and every `page_breaks` before/after snapshot.
4. Apply one coherent correction pass following the correction order.
5. Recompile, rerender, and reinspect all pages—not only the page that changed.
6. Report unresolved warnings and whether visual inspection was actually completed.

## Tool references

- Poppler `pdftotext` bounding-box and layout modes: <https://manpages.debian.org/unstable/poppler-utils/pdftotext.1.en.html>
- Poppler font embedding and ToUnicode fields: <https://manpages.debian.org/bookworm/poppler-utils/pdffonts.1.en.html>
- CTAN `needspace` package: <https://ctan.org/pkg/needspace>
- LaTeX Project discussion of widow/orphan detection: <https://www.latex-project.org/publications/indexbytopic/2e-packages/>
