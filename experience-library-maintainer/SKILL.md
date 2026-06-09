---
name: experience-library-maintainer
description: Maintain and extend the personal experience-library workflow used to turn source experience notes into resume, interview, and company-specific application materials. Use when working in an experience archive repo with folders like experiences/ or legacy internships/, projects/, publications/, cv/, and interview/, especially for tasks such as adding or updating source entries, syncing derivative resume files, generating or revising interview talking points, creating company-specific interview prep packs, keeping README/index files aligned with the current workflow and file layout, or maintaining TeX-based resume templates and checks.
---

# Experience Library Maintainer

Maintain the repo as a source-first career-materials system: update detailed source experience files first, then sync derivative resume and interview artifacts.

## Workflow Decision Tree

- If the user changes the facts of an experience:
  Update the source file under `experiences/` or legacy `internships/`, `projects/`, or `publications/` first.
- If the user wants better resume bullets or selection:
  Update the source file if facts changed, then sync `cv/` artifacts.
- If the user wants speaking materials:
  Update `interview/` artifacts, not just `cv/`.
- If the user wants company-specific prep:
  Create or update a focused pack under a company folder such as `interview/binance/`.
- If the user mentions README, AGENTS, or repo instructions:
  Sync only after checking the current filesystem and current workflow outputs.

Read [references/file-map.md](references/file-map.md) at the start of non-trivial tasks in this repo.

## Core Rules

- Treat source experience files as the factual ground truth.
- Preserve Chinese in repo-authored content unless the target artifact is explicitly English or bilingual.
- Prefer updating existing artifacts over creating parallel duplicates.
- When interview materials exist in both generic and company-specific form, keep:
  - generic material in `interview/interview.md`
  - company-specific material in subfolders like `interview/binance/`
- If docs mention files that no longer exist, verify against the filesystem before propagating the stale reference.

## Standard Workflow

### 1. Build Context

- Inspect the relevant source file(s).
- Inspect the derivative artifact(s) the user actually uses.
- Check whether the request is:
  - source update
  - resume sync
  - interview sync
  - company-specific prep
  - repo documentation sync

### 2. Update Source Before Derivatives

When experience facts, scope, metrics, responsibilities, or technical details change:

- update the source entry first
- then update resume/interview derivatives

When creating a brand-new source entry:

- start from `assets/source-templates/TEMPLATE.md`
- adapt sections by entry type instead of writing from a blank file

Do not let `cv/` or `interview/` contain stronger claims than the source files unless the user explicitly wants speculative drafting.

### 3. Sync Resume Artifacts

When working in `cv/`, use this order:

1. `cv/CV_ENTRY_BANK.md`
2. resume variants such as `cv/cv_cn.tex`, `cv/cv_cn_1page.tex`, `cv/cv.tex`
3. audits or supporting docs such as `cv/RESUME_ENTRY_AUDIT.md`

When maintaining TeX resumes:

- use bundled template assets under `assets/tex-templates/` as canonical examples
- run `scripts/detect_tex_dependencies.py` to inspect required LaTeX packages and local tools
- run `scripts/check_tex_pages.py` after edits to check actual page count and per-page fill heuristics

Keep the entry bank opinionated:

- mark mainline items clearly
- demote dropped items instead of deleting useful history
- keep claims concise and verifiable

### 4. Sync Interview Artifacts

Use:

- `interview/interview.md` for reusable project/experience introductions and topic prep
- company folders such as `interview/binance/` for tailored mocks, domain notes, and closing questions

When adding interview material:

- write for actual speech, not essay style
- prefer 30–90 second answers
- tie answers back to concrete projects from the repo
- add English alongside Chinese when the interview target is bilingual or international

### 5. Sync Repo Docs

Update repo docs only when they materially help future maintenance.

Typical targets:

- `README.md`
- `AGENTS.md`

Only describe workflows that are actually current. Prefer filesystem truth over older prose.

## Common Task Patterns

### Add or revise an experience

- update the source entry
- update `README.md` index if the entry is indexed there
- sync any affected `cv/` and `interview/` artifacts

### Add company-specific interview prep

- inspect the target company folder under `interview/`
- create focused files such as:
  - domain notes
  - mock Q&A
  - "questions I want to ask"
- keep answers anchored to the user’s existing projects

### Convert project updates into talking points

- extract:
  - problem
  - contribution boundary
  - technical approach
  - metrics or evidence
  - why it matters
- then write:
  - short resume version
  - longer interview version
  - bilingual version if needed

### Maintain resume templates

- keep TeX templates under `assets/tex-templates/`
- prefer updating the template assets when the repo has settled on a better resume layout
- use dependency and page-check scripts before declaring the resume variants healthy

## Output Style Guidelines

- For resume materials, optimize for density and verifiability.
- For interview materials, optimize for clear spoken flow.
- For company-specific packs, optimize for relevance to the JD and likely product realities.
- Prefer one strong maintained artifact over multiple overlapping drafts.

## Checks Before Finishing

- Are source and derivative claims consistent?
- Did the right canonical interview file get updated?
- Did you avoid reviving deprecated duplicate files?
- If repo docs were updated, do they match the current filesystem?
