# Experience Library Maintainer

A publishable Codex skill for bootstrapping and maintaining a personal experience archive as a source-first system for resume, interview, and company-specific application materials.

This skill was designed around a real workflow with folders such as:

- `experiences/` or legacy `internships/`
- `projects/`
- `publications/`
- `cv/`
- `interview/`

The core idea is simple:

1. Create a usable experience-library repo when needed.
2. Keep detailed source experience notes as the factual ground truth.
3. Derive resume bullets, interview scripts, and company-specific prep materials from those source files.
4. Keep the whole repo consistent as the workflow evolves.

## What the Skill Does

The skill helps an agent:

- create a brand-new experience library at a user-chosen path
- explore a given local directory, repo, or material dump and turn it into source entries
- update source experience entries before touching derived materials
- start from a reusable source-entry template instead of drafting from scratch
- maintain an opinionated resume entry bank
- sync Chinese and English resume variants
- maintain canonical TeX resume templates
- detect LaTeX package and tool dependencies
- compile a resume and check actual page count plus per-page fill heuristics
- maintain reusable interview talking points
- create company-specific interview prep packs
- save the JD into a company folder before generating mocks
- keep `README.md` / `AGENTS.md` aligned with the current file layout and workflow
- guide the user step by step with explicit next-action options after each milestone

It is especially useful when one repo has both:

- archival long-form experience notes
- downstream job-search artifacts that must stay consistent

It also works when the repo does not exist yet and must be scaffolded from zero.

## Repo Layout

```text
experience-library-maintainer-skill-repo/
|-- README.md
|-- LICENSE
`-- experience-library-maintainer/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    |-- assets/
    |   |-- lib-scaffold/
    |   |   |-- AGENTS.md
    |   |   |-- README.md
    |   |   |-- cv/
    |   |   `-- interview/
    |   |-- cv-templates/
    |   |   |-- CV_ENTRY_AUDIT.md
    |   |   `-- CV_ENTRY_BANK.md
    |   |-- source-templates/
    |   |   `-- TEMPLATE.md
    |   `-- tex-templates/
    |-- scripts/
    |   |-- check_tex_pages.py
    |   `-- detect_tex_dependencies.py
    `-- references/
        `-- file-map.md
```

The actual skill lives inside `experience-library-maintainer/`.

## Installation

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\experience-library-maintainer `
  $HOME\.codex\skills\experience-library-maintainer
```

If `CODEX_HOME` is set, use:

```powershell
Copy-Item -Recurse .\experience-library-maintainer `
  $env:CODEX_HOME\skills\experience-library-maintainer
```

## Triggering the Skill

Example prompt:

```text
Use $experience-library-maintainer to create or maintain my experience library, CV materials, and interview docs consistently.
```

Typical requests:

- "Create a new experience library in this folder and seed it with the standard structure."
- "Explore this repo and turn the relevant projects into source entries in my library."
- "Add a new internship and sync the resume bullets."
- "Update my project facts, then revise the interview introduction."
- "Create a company-specific mock interview pack based on this JD."
- "Check whether my Chinese resume still fits into 1 page and whether the last page is too sparse."
- "Fix stale README references after I changed the interview file layout."

## Workflow Philosophy

This skill enforces a source-first derivative workflow:

1. If needed, create the experience-library repo scaffold at the chosen path.
2. Build or update factual experience notes in `experiences/` or legacy `internships/`, `projects/`, or `publications/`.
3. Sync the resume layer in `cv/`.
4. Sync the interview layer in `interview/`.
5. Sync repo documentation only after checking the actual filesystem.

This avoids common failure modes in job-search repos:

- resume bullets becoming stronger than the source facts
- interview scripts drifting away from what is actually documented
- stale README / agent instructions pointing to deleted files
- company-specific packs being generated before the JD is actually captured
- users not knowing the most natural next action after each step

## Canonical Artifact Rules

The skill assumes and encourages these conventions:

- source facts live in `experiences/` or legacy `internships/`, `projects/`, `publications/`
- new source entries can start from a reusable `TEMPLATE.md` bundled with the skill
- generic interview prep lives in `interview/interview.md`
- company-specific prep lives in subfolders such as `interview/<company>/`
- company-specific directories should usually save the JD first, then generate `mock.md`
- resume selection and wording are maintained through `cv/CV_ENTRY_BANK.md`
- TeX template assets and TeX validation scripts can be bundled with the skill
- every completed step should be followed by a small menu of likely next steps

## My Actual Multi-Agent Workflow

The same repo can be maintained through different agent surfaces. This skill is built to make those surfaces converge on the same artifact order and decision rules.

### 1. Codex Flow

This is the most direct path when the agent can edit the repo locally.

Typical flow:

1. Create the library scaffold if the repo does not exist yet.
2. Inspect the relevant source experience file or raw material folder.
3. Update or create source files first.
4. Sync `cv/` artifacts.
5. Sync `interview/` artifacts.
6. Update `README.md` or `AGENTS.md` only if needed.

This is the cleanest mode for structured repo maintenance because the skill can directly enforce the source-first workflow.

It is also the best mode for TeX resume maintenance, because the same agent can update source wording, sync `.tex` variants, detect missing LaTeX dependencies, compile the resume, and check whether it really fits into 1 page or 2 pages.

### 2. Claude Code Flow

This works well as an alternative editing surface or as a second-pass drafting surface.

Typical flow:

1. Point Claude Code at the same repo.
2. Make sure it sees the same source-first expectations.
3. Ask it to update source files before derivatives.
4. Use it for rewriting, tightening interview phrasing, or generating bilingual variants.
5. Verify that it updates the same canonical interview files instead of creating duplicates.

In practice, this flow is strongest when Claude is used with explicit repo conventions rather than as a free-form writer.

### 3. OpenClaw / Hermes Flow

Treat OpenClaw / Hermes-style setups as orchestration layers rather than freeform writers.

Typical flow:

1. Use OpenClaw / Hermes to collect the task context:
   - target company
   - job description
   - desired artifact type
   - source path or repo path if ingestion is needed
2. Decide whether the request is:
   - library bootstrap
   - source ingest
   - resume sync
   - interview sync
   - company-specific prep
3. Route the task through the same source-first workflow.
4. Keep the agent bounded:
   - do not let it strengthen claims beyond source files
   - do not let it create parallel interview files unless explicitly needed
   - do not let it update repo docs without checking the filesystem
   - do not let it generate company mocks before saving the JD
   - remember the canonical library path after first bootstrap when the surface supports memory

In other words, OpenClaw / Hermes can be great for orchestration, planning, and multi-step agentic handoff, but this skill is what keeps the artifact logic stable.

## Included Skill Files

- `experience-library-maintainer/SKILL.md`
  Core workflow instructions and trigger description.
- `experience-library-maintainer/references/file-map.md`
  Repo-specific file roles, update order, and stale-doc signals.
- `experience-library-maintainer/references/user-flow.md`
  Guided step-by-step flow and recommended next-action menus.
- `experience-library-maintainer/assets/lib-scaffold/`
  Starter files and folders for creating a new experience-library repo at a chosen path.
- `experience-library-maintainer/assets/cv-templates/`
  Reusable templates for `CV_ENTRY_BANK.md` and `CV_ENTRY_AUDIT.md`.
- `experience-library-maintainer/assets/source-templates/TEMPLATE.md`
  A reusable source-entry template distilled from a real experience-library repo.
- `experience-library-maintainer/assets/tex-templates/`
  Canonical TeX resume templates copied from a real experience-library repo.
- `experience-library-maintainer/scripts/detect_tex_dependencies.py`
  Detects LaTeX packages, included files, and local compile tools.
- `experience-library-maintainer/scripts/check_tex_pages.py`
  Compiles a TeX resume, reports actual page count, and estimates per-page fill.
- `experience-library-maintainer/agents/openai.yaml`
  UI metadata and default invocation prompt.

## Example Use Cases

- Create an experience-library repo from scratch in a new directory.
- Explore a codebase or notes folder and ingest the relevant material into source entries.
- Maintain a long-term experience archive for experiences, projects, and publications.
- Turn source notes into a curated resume entry bank.
- Keep TeX resume templates healthy and detect page-count drift.
- Keep interview scripts aligned with updated project facts.
- Build tailored company-specific mock packs for specific employers or roles.
- Migrate the workflow across Codex, Claude Code, and OpenClaw/Hermes-style agent setups without losing artifact discipline.

## License

MIT
