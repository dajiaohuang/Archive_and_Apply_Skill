# Archive and Apply File Map

Use this reference when the repo appears to be an archive-and-apply workspace that feeds resume and interview outputs.

## Bootstrap shape for a new workspace

When creating a new archive-and-apply workspace from scratch, prefer this base structure:

- `experiences/`
- `projects/`
- `publications/`
- `publications/papers/`
- `cv/templates/`
- `cv/tools/`
- `interview/coding/`
- `academia/`
- root `README.md`
- root `AGENTS.md`
- root `TEMPLATE.md`
- root `.gitignore`

When the user prefers a language-specific workspace, choose Chinese or English scaffold files and copy them into these canonical names.

## Source-of-truth layers

### Source experiences

- `experiences/`
- legacy `internships/`
- `projects/`
- `publications/`

When creating a new source entry from scratch, start from:

- `assets/source-templates/TEMPLATE.cn.md` inside the skill for Chinese libraries
- `assets/source-templates/TEMPLATE.en.md` inside the skill for English libraries

These hold detailed factual material and should be updated first when experience content changes.

### CV derivatives

- `cv/CV_ENTRY_BANK.md`
- `cv/CV_ENTRY_AUDIT.md`
- `cv/cv_cn.tex`
- `cv/cv_cn_1page.tex`
- `cv/cv.tex`
- `cv/cv_1page.tex`
- optional draft files in `cv/`
- `cv/cv fixed/` only as historical reference, not the default editing target

If `cv/CV_ENTRY_BANK.md` already exists, any source-entry update should consider whether the bank needs to be refreshed from the updated source facts.

Use `cv/CV_ENTRY_AUDIT.md` when the user wants role-specific CV decisions such as:

- which entries belong in an Agent / LLM CV versus a Data Science CV
- which entries should be shortened, weakened, or dropped
- which skills should stay in the Skills section versus only appear inside bullets

### Resume templates and checks

- `assets/tex-templates/` inside the skill for canonical TeX resume templates
- `cv/templates/README.md` inside the repo for the current template mapping
- `cv/tools/detect_tex_dependencies.py` inside the repo for local dependency checks
- `cv/tools/check_tex_pages.py` inside the repo for local page-count and fill checks
- `scripts/detect_tex_dependencies.py` for package and tool detection
- `scripts/check_tex_pages.py` for page count and fill heuristics

### Interview derivatives

- `interview/interview.md` for general reusable speaking materials
- `interview/<company>/` for company-specific prep
- `interview/<company>/jd.md` for the saved job description
- `interview/<company>/mock.md` for mock interview Q&A
- `interview/<company>/my-q.md` for closing questions the candidate wants to ask
- `interview/coding/` for coding practice and implementation drills

Current known company-specific pattern:

- `interview/binance/crypto.md`
- `interview/binance/mock.md`
- `interview/binance/my-q.md`

### Academia derivatives

- `academia/PUBLICATION_SUMMARY.md` — 1-2 sentence academic abstracts for all papers. Always kept current; cite from here in other materials.
- `academia/SOP.md` — Statement of Purpose. Research motivation + experience narrative. Customize per school.
- `academia/RESEARCH_STATEMENT.md` — PhD / research master's only. Deeper technical narrative, names potential advisors.
- `academia/PERSONAL_STATEMENT.md` — required by some programs. Personal growth narrative; do not copy SOP content here.
- `academia/REC_TRACKER.md` — tracks recommenders: relationship, highlights, request timing, submission status.
- `academia/<school>/` — per-school customized materials: copy general files and swap school / professor / lab names.
- `academia/writing-samples/` — writing sample storage (course papers, published work).

**Typical update order for academia:**

1. Source entries complete and current
2. `academia/PUBLICATION_SUMMARY.md`
3. `academia/SOP.md`
4. `academia/RESEARCH_STATEMENT.md` (if PhD / research master's)
5. `academia/PERSONAL_STATEMENT.md` (if required)
6. `academia/REC_TRACKER.md` — start early, 1-2 months before deadline
7. Per-school customization in `academia/<school>/`

### Archive and discard areas

- `discard/` holds archived experiments, job-search artifacts, old scripts, and deprecated drafts
- treat `discard/` as non-canonical unless the user explicitly wants to recover something from it

## Maintenance conventions

- Keep Chinese as the default for repo-authored archival and interview notes unless the artifact is explicitly English or bilingual.
- Generic interview material belongs in `interview/interview.md`, not `cv/`.
- Company-specific prep belongs under `interview/<company>/`.
- Coding-prep snippets belong under `interview/coding/`.
- Treat `cv/cv fixed/` and `discard/` as reference-only by default.
- If a README mentions files that no longer exist, verify against the filesystem before copying the reference forward.

## Typical update order

1. Source entry
2. `cv/CV_ENTRY_BANK.md`
3. Resume variants in `cv/`
4. `interview/interview.md`
5. company-specific interview files
6. repo-local checks in `cv/tools/` when TeX artifacts changed
7. `README.md` or `AGENTS.md` if needed

When building company-specific prep from a JD:

1. create `interview/<company>/`
2. store the JD there first
3. create `mock.md`
4. create `my-q.md`

## Signals that derivative docs are stale

- references to deleted files
- stronger claims than the source entries support
- duplicated interview files in multiple folders
- old workflow notes that point to the wrong canonical file
