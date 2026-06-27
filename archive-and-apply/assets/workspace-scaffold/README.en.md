# Archive and Apply

This repository is a long-term archive of experiences, projects, and publications that feeds CV, resume, and interview materials.

## Recommended Structure

- `experiences/`: internships, research, and other experience entries
- `projects/`: course projects, research projects, side projects, and competitions
- `publications/`: papers and research outputs
- `publications/papers/`: paper notes, parsed content, or reading notes
- `cv/`: resume source files, entry banks, audits, and TeX tooling
- `interview/`: reusable interview intros, company-specific prep, and coding notes
- `TEMPLATE.md`: canonical source-entry template

## Recommended Workflow

1. Build or update source entries in `experiences/`, `projects/`, and `publications/`.
2. Derive `cv/CV_ENTRY_BANK.md` from those source entries.
3. Create or revise `.tex` resume variants and run page checks.
4. Maintain `interview/interview.md` and company-specific folders under `interview/<company>/`.

## `cv/` Overview

Recommended files in `cv/`:

- `cv.tex` / `cv_cn.tex`
- `cv_1page.tex` / `cv_cn_1page.tex`
- `CV_ENTRY_BANK.md`
- `CV_ENTRY_AUDIT.md`
- `templates/README.md`
- `tools/detect_tex_dependencies.py`
- `tools/check_tex_pages.py`

## `interview/` Overview

- `interview/interview.md`: reusable project intros and topic bank
- `interview/coding/`: coding drills and implementation notes
- `interview/<company>/`: company- or role-specific prep folder

Company-specific folders usually contain:

- `jd.md`
- `mock.md`
- `my-q.md`
- optional domain notes
