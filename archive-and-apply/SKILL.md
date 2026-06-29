---
name: archive-and-apply
description: Bootstrap and maintain a personal archive-and-apply workflow that turns source experience notes into resume, interview, and company-specific application materials. Use when the user wants to create a new archive-and-apply workspace at a chosen path, ingest material from local directories or repos into source entries, derive CV artifacts from the workspace, compile and check TeX resumes, or generate reusable and company-specific interview prep packs.
---

# Archive and Apply Skill

Bootstrap or maintain an archive-and-apply repo as a source-first career-materials system: create the workspace when needed, ingest source facts from raw materials or external directories/repos, then sync derivative resume and interview artifacts.

## Core Rules

- Treat source experience files as the factual ground truth.
- Preserve Chinese in repo-authored content unless the target artifact is explicitly English or bilingual.
- On first bootstrap of a new workspace, if the user's install prompt or first invocation prompt is in Chinese, default to a Chinese workspace; otherwise default to an English workspace.
- If the user wants the whole workspace in Chinese, use Chinese templates consistently for source entries, CV entry files, and interview files.
- If the user wants the whole workspace in English, use English templates consistently for source entries, CV entry files, and interview files.
- If the user does not specify a language, follow the existing language of the target repo or target folder.
- Prefer updating existing artifacts over creating parallel duplicates.
- After every meaningful milestone, explicitly offer 2 to 4 concrete next-step options instead of ending with status only.
- Present next-step menus as multi-select by default: the user may choose one or more follow-up actions unless there is a true dependency that forces sequencing.
- When interview materials exist in both generic and company-specific form, keep generic material in `interview/interview.md` and company-specific material in subfolders like `interview/binance/`.
- If docs mention files that no longer exist, verify against the filesystem before propagating the stale reference.
- For source entries, optimize for reusable factual detail.
- For resume materials, optimize for density and verifiability.
- For interview materials, optimize for clear spoken flow.
- For company-specific packs, optimize for relevance to the JD and likely product realities.
- Prefer one strong maintained artifact over multiple overlapping drafts.

Before finishing, verify: source and derivative claims are consistent; the right canonical interview file was updated; the JD was saved before generating company-specific mocks; the user received concrete next-step options; deprecated duplicate files were not revived; repo docs (if updated) match the current filesystem.

## References

Read these references when relevant:

- [references/file-map.md](references/file-map.md) — canonical file roles, update order, and stale-doc signals. Read at the start of non-trivial tasks.
- [references/user-flow.md](references/user-flow.md) — guided next-step menus for each milestone.
- [references/role-cv-audit.md](references/role-cv-audit.md) — role-specific CV audit directions and a catalog of common role paths.

## Workflow Decision Tree

- **New workspace?** Scaffold the repo at the chosen location using `assets/workspace-scaffold/`, copy in the correct Chinese or English scaffold files, source-entry template, TeX templates, and TeX check scripts.
- **Directory / repo / raw material to ingest?** Explore the provided material, classify content into `experiences/`, `projects/`, or `publications/`, then create or strengthen source entries.
- **Experience facts changed?** Update the source file under `experiences/` or legacy `internships/`, `projects/`, or `publications/` first.
- **Better resume bullets or selection?** Update the source file if facts changed, then sync `cv/` artifacts.
- **Speaking materials?** Update `interview/` artifacts, not just `cv/`.
- **Company-specific prep?** Create or update a focused pack under a company folder such as `interview/binance/`, store the JD there first, then suggest or generate `mock.md`.
- **README / AGENTS / repo instructions?** Sync only after checking the current filesystem and current workflow outputs.

## Standard Workflow

### 1. Build Context

- If the workspace does not exist yet, create the structure before writing content.
- Inspect the relevant source file(s) and the derivative artifact(s) the user actually uses.
- If the user provided a path, repo, or folder of materials, inspect it before drafting entries.
- Classify the request: workspace bootstrap / external-material ingest / source update / resume sync / interview sync / company-specific prep / repo documentation sync.

### 2. Bootstrap a New Workspace

Create these directories:
- `experiences/`
- `projects/`
- `publications/`
- `publications/papers/`
- `cv/templates/`
- `cv/tools/`
- `interview/coding/`
- `academia/`

Seed these files:
- root `README.md`
- root `AGENTS.md`
- root `.gitignore`
- root `TEMPLATE.md`
- `cv/README.md`
- `cv/templates/README.md`
- `interview/README.md`
- `academia/README.md`

Then copy:
- TeX templates from `assets/tex-templates/`
- TeX check scripts from `scripts/`

**Language rules for bootstrapping:**
- First bootstrap + Chinese prompt → Chinese scaffold docs and templates
- Otherwise → English scaffold docs and templates (unless user explicitly requested another language)
- Target repo / folder already exists → follow its existing language
- Choose language for: root README/AGENTS, `cv/README.md`, `cv/templates/README.md`, `interview/README.md`, `academia/README.md`, source-entry template, `CV_ENTRY_BANK` / `CV_ENTRY_AUDIT` templates, interview templates, academia templates

**Bootstrap notes:** prefer `experiences/` over `internships/` for new repos; keep the scaffold simple and editable; report the canonical workspace path after creation; if the agent surface supports memory, store the canonical workspace path for future reuse.

### 3. Update or Create Source Before Derivatives

When experience facts change: update the source entry first, then update resume/interview derivatives. If `cv/CV_ENTRY_BANK.md` already exists, explicitly prompt whether it should be refreshed from the updated source entry.

When creating a brand-new source entry: start from `assets/source-templates/TEMPLATE.cn.md` or `assets/source-templates/TEMPLATE.en.md`, adapt sections by entry type instead of writing from a blank file.

When the user provides a directory, repo, or mixed material dump: inspect the material first, identify what belongs in `experiences/`, `projects/`, or `publications/`, create source entries from the discovered facts, and keep unsupported details in a follow-up checklist instead of inventing them.

Do not let `cv/` or `interview/` contain stronger claims than the source files unless the user explicitly wants speculative drafting.

### 4. Sync Resume Artifacts

Order: `cv/CV_ENTRY_BANK.md` → resume variants (`.tex`) → audits or supporting docs (`cv/CV_ENTRY_AUDIT.md`).

Flow:
1. Extract resume-ready bullets from source entries
2. Place them in `cv/CV_ENTRY_BANK.md`
3. Select and place them into the target TeX resume
4. Compile and check whether the actual pages match the target
5. Check whether a 1-page or 2-page resume is too sparse

**TeX maintenance:** use bundled template assets under `assets/tex-templates/` as canonical examples; on the first CV workflow in a workspace, detect local TeX tooling before committing to compile-based actions; run `scripts/detect_tex_dependencies.py` to inspect required LaTeX packages and local tools; run `scripts/check_tex_pages.py` after edits to check actual page count and per-page fill heuristics.

**Entry bank conventions:** mark mainline items clearly; demote dropped items instead of deleting useful history; keep claims concise and verifiable.

**Role-direction CVs:** audit not only project entries but also the Skills section; decide which entries are must-keep, optional, or weaken/drop for that role direction; decide which skills should appear in the Skills block versus staying only inside project bullets; prefer storing the reasoning in `cv/CV_ENTRY_AUDIT.md`.

### 5. Sync Interview Artifacts

Use `interview/interview.md` for reusable project/experience introductions and topic prep. Use company folders such as `interview/binance/` for tailored mocks, domain notes, and closing questions.

When creating a company- or role-specific directory:
1. Create `interview/<company-or-role>/`
2. Save the JD there first, usually as `jd.md`
3. Create or suggest the next files: `mock.md`, `my-q.md`, optional domain notes

After a JD is saved: explicitly note that the next natural step is to generate `mock.md`; tie the mock questions to the user's source entries rather than generic interview lists.

When adding interview material: write for actual speech, not essay style; prefer 30-90 second answers; tie answers back to concrete projects from the repo; add English alongside Chinese when the interview target is bilingual or international.

### 6. Sync Repo Docs

Update repo docs only when they materially help future maintenance. Typical targets: `README.md`, `AGENTS.md`. Only describe workflows that are actually current. Prefer filesystem truth over older prose.

### 7. Sync Academia Application Materials

Use `academia/` for graduate school, professional school, and fellowship applications.

**Core materials and their use:**

- `PUBLICATION_SUMMARY.md` — 1-2 sentence academic abstracts for all papers, always kept current. Cite from here in other materials without rewriting.
- `SOP.md` — Statement of Purpose. Research motivation + experience narrative, typically 800-1000 words. Customize per school.
- `RESEARCH_STATEMENT.md` — PhD / research master's only. Deeper technical research narrative, more detailed than SOP, names potential advisors.
- `PERSONAL_STATEMENT.md` — required by some programs. Personal growth narrative, differentiated from SOP (do not copy SOP content here).
- `REC_TRACKER.md` — tracks all recommenders: relationship depth, what they can highlight, request timing, submission status.

**Order of work:**

1. Ensure source entries are complete and up to date (this is the foundation for all academic materials)
2. Generate `PUBLICATION_SUMMARY.md` from `publications/` and `projects/` with paper-ready work
3. Draft `SOP.md` from source entries (extract problem → approach → result narrative)
4. If applying for PhD or research master's, draft `RESEARCH_STATEMENT.md`
5. If the program requires Personal Statement, draft it separately from SOP
6. Identify 2-3 recommenders early, fill `REC_TRACKER.md`, and provide them CV + draft before requesting
7. For each target school: copy the general materials to `<school>/` subdirectory and customize school name, professor names, lab names, course names

**Key rules:**

- All claims in SOP / Research Statement / Personal Statement must be traceable to source entries
- SOP, Research Statement, and Personal Statement must each have a distinct focus — do not reuse the same content across them
- When customizing per school, change only the school-specific parts (names, lab descriptions, course names); keep the core narrative
- Academic CV for PhD / research master's: typically 2 pages, stronger emphasis on research than on work experience
- Start recommender outreach 1-2 months before the earliest deadline
