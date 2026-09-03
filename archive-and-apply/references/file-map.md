# Workspace Map and Canonicalization

Read this reference at the start of non-trivial work.

## Discover before changing

1. Read repo-local instructions such as `AGENTS.md`.
2. Inventory relevant files with `rg --files`.
3. Check the repository status and preserve unrelated changes.
4. Identify the canonical artifact from actual links, recent edits, and repo instructions.
5. Treat README descriptions as hints until verified against the filesystem.

Do not force a migration merely because the workspace differs from this map.

## Recommended new-workspace shape

```text
experiences/                 factual work and research experiences
projects/                    factual project entries
publications/                publication records
publications/papers/         paper notes or extracted source material
jobs/targets.md              search criteria and priorities
jobs/saved/                  captured JDs plus role analysis
jobs/companies/              reusable company research
jobs/comparisons/            cross-role comparisons
jobs/applications.md         application event/status tracker
cv/CV_ENTRY_BANK.md          reusable resume wording and evidence links
cv/CV_ENTRY_AUDIT.md         reusable role-selection decisions
cv/tools/                    local validation scripts
interview/interview.md       reusable spoken material
interview/<target>/          target-specific interview material
academia/                    graduate/professional application material
discard/                     explicitly archived, non-canonical material
```

## Artifact roles

### Source layer

`experiences/`, `projects/`, and `publications/` hold detailed facts, contribution boundaries, provenance, outcomes, and unknowns. New files start from the matching source template.

### Job layer

- `jobs/targets.md`: desired roles, constraints, location, timing, and priorities.
- `jobs/saved/<company>-<role>.md`: raw JD snapshot, capture metadata, evidence map, gaps, and decision.
- `jobs/companies/<company>.md`: reusable, sourced company research.
- `jobs/applications.md`: event log and current status. Keep dates explicit; distinguish planned from submitted.

### Resume layer

- `cv/CV_ENTRY_BANK.md`: reusable candidate bullets backed by source entries.
- `cv/CV_ENTRY_AUDIT.md`: role-specific selection logic, not another resume draft.
- `cv/tools/setup_tex_dependencies.py`: detect dependencies, smoke-test English/Chinese TeX, and propose a confirmation-gated platform install plan.
- `cv/tools/check_resume_layout.py`: inspect page fill, safety margins, page-break context, fonts, links, extraction, and render all pages for visual review.
- Resume/CV outputs: names are workspace-specific. Common legacy names include `cv.tex`, `cv_1page.tex`, `cv_cn.tex`, and `cv_cn_1page.tex`. When those four exist, lock wording against `cv_cn.tex` first; see `references/resume-section-lock.md`.

### Interview layer

- `interview/interview.md`: reusable stories and technical explanations.
- `interview/<target>/jd.md`: JD snapshot or a link to the canonical job record.
- `interview/<target>/mock.md`: target-specific mock questions and answer outlines.
- `interview/<target>/my-q.md`: questions to ask the interviewer.

Avoid duplicating a full JD in multiple places. If the canonical copy is under `jobs/saved/`, link to it from the interview folder.

### Academic layer

Create only documents required by the target program. Common names include:

- `academia/PUBLICATION_SUMMARY.md`
- `academia/SOP.md` or `ACADEMIC_STATEMENT.md`
- `academia/PERSONAL_STATEMENT.md` or `PERSONAL_HISTORY.md`
- `academia/RESEARCH_STATEMENT.md`
- `academia/REC_TRACKER.md`
- `academia/<program>/` for prompt, research notes, and final tailored files

Do not assume these documents are interchangeable; the program prompt defines the role of each.

## Dependency direction

```text
source entries ─┬─> CV entry bank ─> targeted resume/CV
                ├─> job evidence map ─> application materials
                ├─> reusable interview stories ─> target interview pack
                └─> academic evidence map ─> program-specific statements
```

Update only downstream artifacts affected by the changed fact or request.

## Staleness signals

- a derivative claim has no source or is stronger than its source
- a JD analysis lacks the raw JD, URL, or capture date
- an application status has no date or evidence
- multiple files claim to be the canonical resume or interview base
- a program essay contains another school's faculty, lab, or program name
- docs reference missing files or templates
- archived files under `discard/` are treated as current without explicit recovery
