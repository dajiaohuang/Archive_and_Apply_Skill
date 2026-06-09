---
name: experience-library-maintainer
description: Bootstrap and maintain a personal experience-library workflow that turns source experience notes into resume, interview, and company-specific application materials. Use when the user wants to create a new experience library at a chosen path, ingest material from local directories or repos into source entries, derive CV artifacts from the library, compile and check TeX resumes, or generate reusable and company-specific interview prep packs.
---

# Experience Library Maintainer

Bootstrap or maintain an experience-library repo as a source-first career-materials system: create the library when needed, ingest source facts from raw materials or external directories/repos, then sync derivative resume and interview artifacts.

## Primary Modes

- Bootstrap a new experience library at a user-chosen path
- Explore a given local directory, repository, notes folder, or material dump and convert relevant content into source entries
- Derive CV entry banks and TeX resumes from source entries, then compile and check page count and page fill
- Generate reusable and company-specific interview materials, including storing the JD before generating mocks

## Workflow Decision Tree

- If the user wants to create a new experience library:
  Scaffold the repo at the chosen location using `assets/lib-scaffold/`, copy in the correct Chinese or English scaffold files, source-entry template, TeX templates, and TeX check scripts.
- If the user gives a directory, repo, or raw material folder and wants entries created:
  Explore the provided material, classify content into `experiences/`, `projects/`, or `publications/`, then create or strengthen source entries.
- If the user changes the facts of an experience:
  Update the source file under `experiences/` or legacy `internships/`, `projects/`, or `publications/` first.
- If the user wants better resume bullets or selection:
  Update the source file if facts changed, then sync `cv/` artifacts.
- If the user wants speaking materials:
  Update `interview/` artifacts, not just `cv/`.
- If the user wants company-specific prep:
  Create or update a focused pack under a company folder such as `interview/binance/`, store the JD there first, then suggest or generate `mock.md`.
- If the user mentions README, AGENTS, or repo instructions:
  Sync only after checking the current filesystem and current workflow outputs.

Read [references/file-map.md](references/file-map.md) at the start of non-trivial tasks in this repo.
Read [references/user-flow.md](references/user-flow.md) when the task benefits from guided next-step suggestions.
Read [references/role-cv-audit.md](references/role-cv-audit.md) when the user wants different CVs for different role directions.

## Core Rules

- Treat source experience files as the factual ground truth.
- Preserve Chinese in repo-authored content unless the target artifact is explicitly English or bilingual.
- On first bootstrap of a new library, if the user's install prompt or first invocation prompt is in Chinese, default to a Chinese library; otherwise default to an English library.
- If the user wants the whole library in Chinese, use Chinese templates consistently for source entries, CV entry files, and interview files.
- If the user wants the whole library in English, use English templates consistently for source entries, CV entry files, and interview files.
- If the user does not specify a language, follow the existing language of the target repo or target folder.
- Prefer updating existing artifacts over creating parallel duplicates.
- After every meaningful milestone, explicitly offer 2 to 4 concrete next-step options instead of ending with status only.
- Present next-step menus as multi-select by default: the user may choose one or more follow-up actions unless there is a true dependency that forces sequencing.
- When interview materials exist in both generic and company-specific form, keep:
  - generic material in `interview/interview.md`
  - company-specific material in subfolders like `interview/binance/`
- If docs mention files that no longer exist, verify against the filesystem before propagating the stale reference.

## Standard Workflow

### 1. Build Context

- If the library does not exist yet, create the structure before writing content.
- Inspect the relevant source file(s).
- Inspect the derivative artifact(s) the user actually uses.
- If the user provided a path, repo, or folder of materials, inspect it before drafting entries.
- Check whether the request is:
  - library bootstrap
  - external-material exploration and ingest
  - source update
  - resume sync
  - interview sync
  - company-specific prep
  - repo documentation sync

### 2. Bootstrap a New Library

When the user wants to create an experience library at a chosen location:

1. Create:
   - `experiences/`
   - `projects/`
   - `publications/`
   - `publications/papers/`
   - `cv/templates/`
   - `cv/tools/`
   - `interview/coding/`
2. Seed:
   - root `README.md`
   - root `AGENTS.md`
   - root `.gitignore`
   - root `TEMPLATE.md`
   - `cv/README.md`
   - `cv/templates/README.md`
   - `interview/README.md`
3. Copy:
   - TeX templates from `assets/tex-templates/`
   - TeX check scripts from `scripts/`
4. Make sure the repo is immediately usable for source entries, CV generation, and interview prep.

When bootstrapping language-sensitive files:

- if this is the first bootstrap and the user prompt is Chinese, default to Chinese scaffold docs and templates
- otherwise, default to English scaffold docs and templates unless the user explicitly requested another language
- if the target repo or target folder already exists, follow its existing language instead of the prompt default
- choose Chinese or English scaffold docs for root `README.md`, root `AGENTS.md`, `cv/README.md`, `cv/templates/README.md`, and `interview/README.md`
- choose `TEMPLATE.cn.md` or `TEMPLATE.en.md` for the root source-entry template
- choose Chinese or English `CV_ENTRY_BANK` / `CV_ENTRY_AUDIT` templates
- choose Chinese or English interview templates

When bootstrapping:

- prefer `experiences/` over `internships/` for new repos
- keep the scaffold simple and editable
- preserve Chinese defaults for content-facing files unless the user wants another language
- report the canonical library path after creation
- if the agent surface supports memory, store the canonical library path for future reuse
- on OpenClaw / Hermes style surfaces, treat the first successful bootstrap as a memory-worthy event

### 3. Update or Create Source Before Derivatives

When experience facts, scope, metrics, responsibilities, or technical details change:

- update the source entry first
- then update resume/interview derivatives
- if `cv/CV_ENTRY_BANK.md` already exists, explicitly prompt whether it should be refreshed from the updated source entry

When creating a brand-new source entry:

- start from `assets/source-templates/TEMPLATE.cn.md` or `assets/source-templates/TEMPLATE.en.md`
- adapt sections by entry type instead of writing from a blank file

When the user provides a directory, repo, or mixed material dump:

- inspect the material first
- identify what belongs in `experiences/`, `projects/`, or `publications/`
- create source entries from the discovered facts
- keep unsupported details in a follow-up checklist instead of inventing them

Do not let `cv/` or `interview/` contain stronger claims than the source files unless the user explicitly wants speculative drafting.

### 4. Sync Resume Artifacts

When working in `cv/`, use this order:

1. `cv/CV_ENTRY_BANK.md`
2. resume variants such as `cv/cv_cn.tex`, `cv/cv_cn_1page.tex`, `cv/cv.tex`
3. audits or supporting docs such as `cv/CV_ENTRY_AUDIT.md`

The intended flow is:

1. extract resume-ready bullets from source entries
2. place them in `cv/CV_ENTRY_BANK.md`
3. select and place them into the target TeX resume
4. compile and check whether the actual pages match the target
5. check whether a 1-page or 2-page resume is too sparse

When maintaining TeX resumes:

- use bundled template assets under `assets/tex-templates/` as canonical examples
- on the first CV workflow in a library, detect local TeX tooling before committing to compile-based actions
- run `scripts/detect_tex_dependencies.py` to inspect required LaTeX packages and local tools
- run `scripts/check_tex_pages.py` after edits to check actual page count and per-page fill heuristics

Keep the entry bank opinionated:

- mark mainline items clearly
- demote dropped items instead of deleting useful history
- keep claims concise and verifiable

When the user wants different CVs for different role directions:

- audit not only project entries but also the Skills section
- decide which entries are must-keep, optional, or weaken/drop for that role direction
- decide which skills should appear in the Skills block versus staying only inside project bullets
- prefer storing the reasoning in `cv/CV_ENTRY_AUDIT.md`

### 5. Sync Interview Artifacts

Use:

- `interview/interview.md` for reusable project/experience introductions and topic prep
- company folders such as `interview/binance/` for tailored mocks, domain notes, and closing questions

When creating a company- or role-specific directory:

1. create `interview/<company-or-role>/`
2. save the JD there first, usually as `jd.md`
3. create or suggest the next files:
   - `mock.md`
   - `my-q.md`
   - optional domain notes

After a JD is saved:

- explicitly note that the next natural step is to generate `mock.md`
- tie the mock questions to the user’s source entries rather than generic interview lists

When adding interview material:

- write for actual speech, not essay style
- prefer 30-90 second answers
- tie answers back to concrete projects from the repo
- add English alongside Chinese when the interview target is bilingual or international

### 6. Sync Repo Docs

Update repo docs only when they materially help future maintenance.

Typical targets:

- `README.md`
- `AGENTS.md`

Only describe workflows that are actually current. Prefer filesystem truth over older prose.

## Common Task Patterns

### Create a new library at a chosen path

- create the directory structure from `assets/lib-scaffold/`
- copy in the source-entry template
- copy in TeX templates and TeX check scripts
- seed interview and CV readmes so future agents know the canonical files

### Explore a repo or materials folder and create entries

- inspect the given path
- identify likely experiences, projects, and publications
- turn discovered facts into source entries
- update the main index after creating new entries if the repo uses one

### Add or revise an experience

- update the source entry
- update `README.md` index if the entry is indexed there
- if `cv/CV_ENTRY_BANK.md` already exists, prompt whether to sync it now
- sync any affected `cv/` and `interview/` artifacts

### Build CV artifacts from library content

- mine source entries for strong, verifiable bullets
- update `cv/CV_ENTRY_BANK.md`
- draft or revise the target TeX resume
- compile and check target page count plus fill level

### Audit CV variants by role direction

- identify the target role direction, such as Agent / LLM Engineering, Data Science / Applied AI, or CV / Multimodal
- decide which entries to keep, weaken, or drop for that direction
- decide what the Skills block should emphasize for that direction
- write or update `cv/CV_ENTRY_AUDIT.md`
- then sync `cv/CV_ENTRY_BANK.md` and the target `.tex` CV

### Add company-specific interview prep

- inspect the target company folder under `interview/`
- if it does not exist, create it and save the JD first
- create focused files such as:
  - `jd.md`
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

- For source entries, optimize for reusable factual detail.
- For resume materials, optimize for density and verifiability.
- For interview materials, optimize for clear spoken flow.
- For company-specific packs, optimize for relevance to the JD and likely product realities.
- Prefer one strong maintained artifact over multiple overlapping drafts.

## Checks Before Finishing

- Is the repo scaffold complete if the task started from an empty location?
- Are source and derivative claims consistent?
- Did the right canonical interview file get updated?
- Was the JD saved before generating company-specific mocks?
- Did the user receive concrete next-step options after the milestone?
- Did you avoid reviving deprecated duplicate files?
- If repo docs were updated, do they match the current filesystem?

## Suggested Next-Step Menus

### After skill install or first invocation

- create a new experience library at a chosen path
- inspect an existing library
- ingest a local directory, repo, or notes folder into a library

### After library bootstrap

- create the first source entries from raw materials
- ingest a local repo or folder into source entries
- check TeX availability before the first CV workflow

### After source entries exist

- create more source entries
- build `cv/CV_ENTRY_BANK.md` in bullet form
- create or update `interview/interview.md`

### After updating an existing source entry

- sync `cv/CV_ENTRY_BANK.md` if it already exists
- refresh the relevant TeX resume
- refresh `interview/interview.md`
- refresh company-specific interview files that depend on the updated entry

### After CV content bank creation

- detect TeX tools
- draft an English resume
- draft a Chinese resume
- draft a one-page or two-page variant

### After resume creation or update

- compile and check page count
- tighten a one-page version
- expand a sparse page
- refresh the entry bank from updated source entries

### After company directory creation

- save the JD to `jd.md`
- generate `mock.md`
- generate `my-q.md`

In all of the menus above, treat the list as "you can pick one or more of these next" unless a hard prerequisite blocks one of them.
