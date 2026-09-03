---
name: archive-and-apply
description: Build and maintain a source-first career and academic application workspace. Use when Codex needs to initialize, inspect, or continue an archive-and-apply workspace; ingest projects, experiences, publications, repositories, PDFs, or raw evidence; manage job targets, saved JDs, company research, and application status; tailor or audit resumes/CVs, cover letters, interview packs, or graduate-school statements; install or diagnose XeLaTeX/PDF dependencies; or compile and visually validate resume pagination and page fill while keeping every claim traceable to its source. Also use when the user invokes $archive-and-apply without a detailed request and needs to be guided directly into the appropriate workflow.
---

# Archive and Apply

Maintain one evidence-backed archive and derive targeted application artifacts from it. Preserve the user's existing layout when it is coherent; use the bundled layout only for a new workspace or an explicit migration.

## Enter the workflow immediately

Treat every invocation as an operational entry point, not a request for a capability description.

1. Match the user's language unless the requested artifact requires another language.
2. If the user gives a concrete task, file, JD, program prompt, resume, repository, or evidence bundle, inspect it and begin the matching workflow immediately. Do not make the user choose a menu first.
3. If the request is only `$archive-and-apply`, “start”, “help me apply”, or similarly underspecified, inspect the current user-scoped directory read-only before asking questions:
   - detect an existing workspace from repo-local instructions and canonical directories such as `experiences/`, `projects/`, `publications/`, `jobs/`, `cv/`, `interview/`, or `academia/`;
   - if one exists, summarize its current state and the most useful next milestone, then ask at most one question needed to proceed;
   - if none exists, ask only for the target path and preferred language, run `scripts/init_workspace.py <target> --language <zh|en> --dry-run`, explain the plan, and create it after the user confirms the target;
   - if several plausible workspaces exist, list their resolved paths and ask which one to use rather than combining them.
4. Offer a compact route choice only when neither the request nor the inspected workspace reveals intent: **build/import evidence**, **job search/application**, **resume/CV**, **interview**, or **academic application**.
5. Perform the work through the skill. Do not require the user to read bundled references, copy templates manually, or run commands that the active environment can safely run.
6. Ask for missing facts only when they block the next safe action. Continue with read-only inspection, evidence mapping, or a clearly marked draft wherever possible.

At the first useful milestone, show the artifact or diagnosis produced, unresolved evidence, and the next decision. Do not end the first response with a generic feature list.

## Non-negotiable rules

- Treat `experiences/`, `projects/`, and `publications/` as evidence, not polished marketing copy.
- Never invent a metric, date, title, authorship position, publication status, ownership claim, employer fact, or program requirement.
- Distinguish **verified**, **user-reported**, **inferred**, and **unknown** facts. Put unknowns in a follow-up list; do not silently fill them.
- Preserve contribution boundaries such as led, independently built, co-developed, contributed, or supported.
- Update source facts before derivatives. If only wording or selection changes, do not rewrite the source merely to match the derivative.
- Keep raw JDs and program prompts verbatim with their source URL and capture date. Put analysis in a separate section or file.
- Do not submit applications, send messages, or change external accounts unless the user explicitly asks and the active tools authorize it.
- Do not expose private contact data or confidential employer material in public-facing outputs.
- Update only artifacts affected by the request. Do not create parallel drafts when a canonical file already exists.

## Route the request

| Request | Primary workflow | Read |
|---|---|---|
| Create a workspace | Bootstrap | `references/file-map.md` |
| Import a repo, notes, PDFs, or raw text | Evidence ingest | `references/file-map.md` |
| Save or compare roles, track applications | Job pipeline | `references/application-workflows.md` |
| Tailor or audit a resume/CV | Resume pipeline | `references/resume-bullet-writing.md`, `references/resume-wording-constraints.md`, then `references/role-cv-audit.md` |
| Lock bilingual resume wording section by section | Section lock | `references/resume-section-lock.md`, then `references/resume-wording-constraints.md` |
| Diagnose or install XeLaTeX/PDF dependencies | TeX setup | `references/tex-setup.md` |
| Compile, inspect, or adjust resume pagination/layout | Layout QA | `references/resume-layout-qa.md` |
| Build interview material | Interview pipeline | `references/application-workflows.md` |
| Draft SOP, personal history, research statement, or recommender tracker | Academic pipeline | `references/academic-applications.md` |
| Continue after a completed milestone | Handoff | `references/user-flow.md` |

For any non-trivial task, read `references/file-map.md` first. Read only the other references required by the selected branch.

## Standard operating loop

1. **Locate the workspace.** Confirm the target path and inspect repo instructions, current files, and existing changes.
2. **Identify the canonical artifacts.** Prefer filesystem truth over stale README text. Record legacy aliases instead of reviving them.
3. **Build an evidence map.** For every requested claim, identify its source file or mark it unresolved.
4. **Perform the smallest complete update.** Follow the selected workflow below.
5. **Validate.** Check factual consistency, links, dates, language, formatting, and affected downstream artifacts.
6. **Report.** State what changed, what was verified, what remains unknown, and only the next actions that are genuinely useful.

## Bootstrap

Use the deterministic initializer instead of manually copying files:

```bash
python scripts/init_workspace.py <target-path> --language zh --dry-run
python scripts/init_workspace.py <target-path> --language zh
```

Use `--language en` for an English-first workspace. The initializer refuses to overwrite existing files; use `--merge` only after inspecting a non-empty target. It creates the source, CV, job, interview, and academic application structure and selects canonical templates for the requested language.

After bootstrap, report the resolved workspace path. Do not claim persistent memory unless the current surface actually provides it.

## Evidence ingest

1. Inventory the supplied material before drafting.
2. Classify each item as an experience, project, publication, job artifact, or supporting evidence.
3. Start new source entries from `assets/source-templates/TEMPLATE.cn.md` or `TEMPLATE.en.md`.
4. Capture provenance, contribution scope, dates, outcomes, and unresolved facts.
5. Deduplicate against existing entries by project, organization, time range, and links.
6. Update the workspace index only if it exists and is actively maintained.
7. When a system replaces an earlier design, keep the old state as history. Do not overwrite the source so that only the latest architecture appears to have existed.

Do not turn a repository's existence into proof that the user authored all of it. Use commit history or explicit user statements only when authorship matters and is available.

## Job and application pipeline

Use `jobs/targets.md` for search constraints, `jobs/saved/` for immutable JD snapshots plus analysis, `jobs/companies/` for reusable company research, and `jobs/applications.md` for the application timeline. Preserve equivalent existing names.

For a target role:

1. Save the raw JD, source, location, and capture date.
2. Extract must-have, preferred, responsibility, and constraint signals without rewriting the JD.
3. Map each requirement to source-backed evidence and mark gaps honestly.
4. Decide whether to apply, research further, or deprioritize.
5. Tailor the requested resume, cover letter, or interview pack from that mapping.
6. Update application status only from user-provided or directly observed evidence.

Never infer that an application was submitted merely because materials were prepared.

## Resume/CV pipeline

1. Confirm whether the target is an industry resume, academic CV, region-specific CV, or portal-specific form.
2. Read the JD or target direction and infer the likely reader path: application parser, recruiter/HR, hiring manager/team leader, technical reviewers, potential peers, and cross-functional interviewers as applicable. State assumptions rather than treating every process as identical.
3. Build entries with progressive disclosure: an accessible problem/ownership signal first, discriminating method or judgment next, and evidence of outcome/validation/team leverage last. Make every clause defensible in an interview. Follow `references/resume-wording-constraints.md` for bilingual punctuation, version leakage, score leakage, and combo-entry rules.
4. For a full bilingual rewrite, lock wording section by section against `cv/cv_cn.tex` before compiling. Follow `references/resume-section-lock.md`. Treat “不用改了”, “下一节”, or “先不变了” as a lock for the section under discussion.
5. After each locked section, sync meaning to the other TeX variants and `cv/CV_ENTRY_BANK.md`. Variants may be shorter or omit an item; they must not contradict the locked claim or invent a stronger result.
6. Update `cv/CV_ENTRY_BANK.md` only when reusable wording, reader signal, or evidence changes.
7. Record role-specific keep, weaken, omit, and reader-coverage decisions in `cv/CV_ENTRY_AUDIT.md` when they will be reused.
8. Tailor the actual target document; do not blindly synchronize every variant or keyword-stuff for an assumed ATS.
9. Prefer simple, consistent formatting and readable text extraction. Follow explicit employer length and file requirements over generic page rules.

For TeX work:

```bash
python scripts/setup_tex_dependencies.py --json
python scripts/setup_tex_dependencies.py --smoke --json
python scripts/detect_tex_dependencies.py path/to/resume.tex --json
python scripts/check_tex_pages.py path/to/resume.tex --target-pages 1 --output path/to/check.pdf --render-dir path/to/rendered --json
python scripts/check_resume_layout.py path/to/check.pdf --render-dir path/to/rendered --json
```

The setup helper is detect-only by default. If it reports missing dependencies, show its install plan and explain the platform-level changes. TeX distributions can be large and may require elevation or a terminal restart. Obtain explicit user confirmation immediately before running `python scripts/setup_tex_dependencies.py --install --yes`; never add `--yes` merely to bypass that boundary. Do not silently replace an existing partial TeX installation. Follow `references/tex-setup.md` for repair and managed-TeX alternatives.

Do not compile during a section-by-section wording lock. After the full wording lock—or after a later layout-only request—compile every target TeX with this skill's `scripts/check_tex_pages.py` and `--output` next to the source. Prefer that script over a stale workspace copy of `cv/tools/check_tex_pages.py`; older local copies may fail on Windows when `pathlib.Path` is passed to `subprocess`. Review the last/first lines around every page boundary; every page's top, bottom, left, and right safety bands; stranded section/entry headings; split bullets or paragraphs; density balance; compile warnings; font embedding; links; and extracted reading order. Then inspect every rendered page for clipping, overlap, broken glyphs, hierarchy, alignment, and spacing. First reduce empty vertical space and the skills block; then follow `references/resume-layout-qa.md` for the rest of the correction order. Repeat the full compile-render-inspect loop after each coherent pass. Page count and bounding-box heuristics are diagnostics, not proof of visual quality or ATS compatibility.

## Interview pipeline

- Keep reusable stories and topic explanations in `interview/interview.md`.
- Keep target-specific material in `interview/<company-or-role>/` or the workspace's existing equivalent.
- Store or link the JD before generating a target-specific mock.
- Write spoken answers with a clear question, concise answer, evidence anchor, and likely follow-up.
- Prepare questions the candidate genuinely wants answered; do not manufacture company facts.

## Academic application pipeline

Capture the exact program, department, deadline, prompt, word/page limit, and required documents before drafting. Program instructions override every bundled template. Tailor intellectual fit from verified faculty, lab, curriculum, or program sources; do not perform name-only substitution across schools.

Keep SOP/academic-purpose, personal-history/personal-statement, and research-statement content distinct according to the actual prompts. Track each substantive claim back to a source entry. Treat recommender choice, timing, and materials as program- and relationship-specific rather than universal.

## Completion checks

- Every material claim has a source or an explicit unresolved marker.
- Raw JD/program text remains separate from analysis.
- Dates, status labels, language, and naming are consistent.
- The requested target artifact—not every possible derivative—was updated.
- TeX outputs compile and extract text; every page and page boundary was rendered and reviewed when TeX/layout changed.
- No stale path or deleted file was reintroduced.
- The final report names unresolved facts and validation limits.
