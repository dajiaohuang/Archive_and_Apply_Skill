# Experience Library Maintainer

A publishable Codex skill for maintaining a personal experience archive as a source-first system for resume, interview, and company-specific application materials.

This skill was designed around a real workflow with folders such as:

- `internships/`
- `projects/`
- `publications/`
- `cv/`
- `interview/`

The core idea is simple:

1. Keep detailed source experience notes as the factual ground truth.
2. Derive resume bullets, interview scripts, and company-specific prep materials from those source files.
3. Keep the whole repo consistent as the workflow evolves.

## What the Skill Does

The skill helps an agent:

- update source experience entries before touching derived materials
- maintain an opinionated resume entry bank
- sync Chinese and English resume variants
- maintain reusable interview talking points
- create company-specific interview prep packs
- keep `README.md` / `AGENTS.md` aligned with the current file layout and workflow

It is especially useful when one repo has both:

- archival long-form experience notes
- downstream job-search artifacts that must stay consistent

## Repo Layout

```text
experience-library-maintainer-skill-repo/
├── README.md
├── LICENSE
└── experience-library-maintainer/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        └── file-map.md
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
Use $experience-library-maintainer to update my experience library, resume materials, and interview docs consistently.
```

Typical requests:

- “Add a new internship and sync the resume bullets.”
- “Update my project facts, then revise the interview introduction.”
- “Create a company-specific mock interview pack based on this JD.”
- “Fix stale README references after I changed the interview file layout.”

## Workflow Philosophy

This skill enforces a source-first derivative workflow:

1. Update factual experience notes in `internships/`, `projects/`, or `publications/`.
2. Sync the resume layer in `cv/`.
3. Sync the interview layer in `interview/`.
4. Sync repo documentation only after checking the actual filesystem.

This avoids a common failure mode in job-search repos:

- resume bullets becoming stronger than the source facts
- interview scripts drifting away from what is actually documented
- stale README / agent instructions pointing to deleted files

## Canonical Artifact Rules

The skill assumes and encourages these conventions:

- source facts live in `internships/`, `projects/`, `publications/`
- generic interview prep lives in `interview/interview.md`
- company-specific prep lives in subfolders such as `interview/<company>/`
- resume selection and wording are maintained through `cv/CV_ENTRY_BANK.md`

## My Actual Multi-Agent Workflow

The same repo can be maintained through different agent surfaces. This skill is built to make those surfaces converge on the same artifact order and decision rules.

### 1. Codex Flow

This is the most direct path when the agent can edit the repo locally.

Typical flow:

1. Ask Codex to inspect the relevant source experience file.
2. Update the source file first if facts changed.
3. Sync `cv/` artifacts.
4. Sync `interview/` artifacts.
5. Update `README.md` or `AGENTS.md` only if needed.

This is the cleanest mode for structured repo maintenance because the skill can directly enforce the source-first workflow.

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

I treat OpenClaw / Hermes-style setups as orchestration layers rather than freeform writers.

Typical flow:

1. Use OpenClaw / Hermes to collect the task context:
   - target company
   - job description
   - desired artifact type
2. Use the agent to decide whether the request is:
   - source update
   - resume sync
   - interview sync
   - company-specific prep
3. Route the task through the same source-first workflow.
4. Keep the agent bounded:
   - do not let it strengthen claims beyond source files
   - do not let it create parallel interview files unless explicitly needed
   - do not let it update repo docs without checking the filesystem

In other words, OpenClaw / Hermes can be great for orchestration, planning, and multi-step agentic handoff, but this skill is what keeps the artifact logic stable.

## Why This Matters

As agents become better at drafting and planning, the hard part is no longer generating text. The hard part is keeping the repository trustworthy:

- which file is the source of truth
- which file is canonical for speaking materials
- which claims are safe to reuse in resumes and interviews
- how to keep company-specific prep separate from reusable base materials

This skill encodes those decisions.

## Included Skill Files

- `experience-library-maintainer/SKILL.md`
  Core workflow instructions and trigger description.
- `experience-library-maintainer/references/file-map.md`
  Repo-specific file roles, update order, and stale-doc signals.
- `experience-library-maintainer/agents/openai.yaml`
  UI metadata and default invocation prompt.

## Example Use Cases

- Maintain a long-term experience archive for internships, projects, and publications.
- Turn source notes into a curated resume entry bank.
- Keep interview scripts aligned with updated project facts.
- Build tailored company-specific mock packs for specific employers or roles.
- Migrate the workflow across Codex, Claude Code, and OpenClaw/Hermes-style agent setups without losing artifact discipline.

## License

MIT
