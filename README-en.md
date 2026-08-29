# Archive & Apply

> Turn experience evidence into traceable, testable, maintainable application materials.

[中文](README.md) · [Project site](https://dajiaohuang.github.io/Archive_and_Apply_Skill/) · [MIT License](LICENSE)

Archive & Apply is a source-first Codex skill. It accepts repositories, notes, PDFs, job descriptions, and official program prompts; organizes the facts into a canonical evidence layer; and derives resumes, job materials, interview packs, and academic statements from that layer.

It does not invent a more impressive history. Its central contract is simple: **material claims trace back to sources, facts stay separate from inference and unknowns, and prepared materials never become evidence of submission.**

```text
repositories / notes / PDFs / raw material
                   │
                   ▼
experience · project · publication sources
       ├──► CV entry bank ──► targeted resume ──► TeX / PDF checks
       ├──► JD evidence map ──► application material and status events
       ├──► reusable stories ──► target interview pack
       └──► academic evidence map ──► program-specific statements
```

## Why it exists

Application facts often live across old resumes, chat history, project repositories, and temporary documents. Rewriting from scratch for every target creates predictable failure modes:

- claims become stronger than their evidence and fail under interview follow-up;
- JDs, company research, resumes, and interview answers drift apart;
- statuses such as saved, preparing, and submitted lose their event evidence.

Archive & Apply separates sources from derivatives. A fact change starts at the source entry; a wording or targeting change updates only the affected downstream artifacts.

## What it covers

| Workflow | Output | Core checks |
|---|---|---|
| Evidence ingest | experience, project, and publication source entries | provenance, dates, contribution boundary, unknowns |
| Job pipeline | JD snapshot, company research, evidence map, event-based status | raw text separate from analysis; no inferred status |
| Resume / CV | entry bank, role audit, targeted TeX/PDF | multi-reader clarity, defensible claims, extractable text |
| Interview | reusable story bank, target mock, candidate questions | evidence anchors for every answer |
| Academic application | prompt record, SOP, personal/research statements, recommendation tracker | official requirements first; no name-only customization |
| Layout QA | PDF diagnostics JSON and rendered PNG pages | page count, bounds, breaks, fonts, links, reading order |

## Quick start

### 1. Install the skill

PowerShell:

```powershell
$skillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
Copy-Item -Recurse .\archive-and-apply (Join-Path $skillRoot 'skills\archive-and-apply')
```

macOS / Linux:

```bash
skill_root="${CODEX_HOME:-$HOME/.codex}"
cp -R ./archive-and-apply "$skill_root/skills/archive-and-apply"
```

### 2. Enter the workflow directly

```text
$archive-and-apply
```

The skill starts clear requests immediately. For a bare “start” request, it inspects the current workspace read-only, identifies the highest-value milestone, and asks at most one question required to continue.

Materials can be the entry point:

```text
Use $archive-and-apply to turn this repository and my notes into traceable experience entries.
Use $archive-and-apply to save this JD, assess fit, and tailor a one-page English resume.
Use $archive-and-apply to inspect this PDF's page breaks, bottom fill, fonts, and text extraction, then fix the TeX.
Use $archive-and-apply to start an SOP workflow from this program's official prompt.
```

### 3. Initialize a dedicated workspace (optional)

Preview, then create:

```powershell
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language en --dry-run
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language en
```

The initializer refuses a non-empty target by default. After inspection, `--merge` creates only missing files and never overwrites existing ones.

## Workspace model

The recommended shape is not a forced migration. The skill first reads repository instructions and existing canonical files, then chooses the smallest affected scope.

```text
experiences/                factual experience sources
projects/                   project facts and contribution boundaries
publications/               publication records and exact status
jobs/                       JDs, company research, fit maps, status events
cv/                         entry bank, role audit, TeX, validation tools
interview/                  reusable stories and target interview packs
academia/                   program prompts and academic materials
discard/                    explicitly archived, non-canonical material
```

## A resume has more than one reader

Archive & Apply infers the likely review path instead of keyword-stuffing for an imaginary universal ATS:

1. parsers need ordinary text, expected structure, and supported role terms;
2. recruiting/HR needs recognizable problems, scope, ownership, and transferable signals;
3. hiring managers and team leads need judgment, responsibility, and outcomes;
4. technical reviewers need probe-worthy methods, constraints, and validation;
5. potential peers and cross-functional partners need clear interfaces and contribution boundaries.

Every bullet should survive questions about ownership, rationale, alternatives, validation, collaborators, and remaining unknowns.

## TeX / PDF tools

Dependency inspection is side-effect free by default:

```powershell
python .\archive-and-apply\scripts\setup_tex_dependencies.py --json
python .\archive-and-apply\scripts\setup_tex_dependencies.py --smoke --json
```

System-level installation with `--install --yes` should run only after the plan is reviewed and the user gives explicit confirmation. Existing TeX installations are never silently replaced.

Inspect a TeX source or PDF:

```powershell
python .\archive-and-apply\scripts\detect_tex_dependencies.py path\to\cv.tex --json
python .\archive-and-apply\scripts\check_tex_pages.py path\to\cv.tex --target-pages 1 --output path\to\check.pdf --render-dir path\to\rendered --json
python .\archive-and-apply\scripts\check_resume_layout.py path\to\check.pdf --render-dir path\to\rendered --json
```

Checks cover compiler diagnostics, page count and size, break context, edge safety, bottom fill, font embedding, links, and text extraction. Automation is diagnostic—not visual proof. Every rendered PNG still needs page-by-page review, and no checker can guarantee the behavior of a particular ATS.

## Repository map

```text
archive-and-apply/
├── SKILL.md                 workflow entry and hard constraints
├── agents/openai.yaml       skill interface metadata
├── references/              judgment and validation rules
├── scripts/                 initialization, dependency, and layout tools
└── assets/
    ├── source-templates/    evidence-layer templates
    ├── job-templates/       JD, company, and application templates
    ├── cv-templates/        entry-bank and role-audit templates
    ├── interview-templates/ interview preparation templates
    ├── academia-templates/  academic application templates
    ├── tex-templates/       Chinese and English TeX resumes
    └── workspace-scaffold/  complete initial workspace
```

## What it will not do

- invent metrics, dates, titles, authorship position, publication status, or contribution scope;
- present inference as verified fact;
- treat prepared material as a submitted application;
- reuse one template by changing only a company, school, or faculty name;
- submit applications, send messages, or change external accounts without explicit authority;
- present automated page and margin checks as an ATS compatibility guarantee.

## Development and verification

The skill can be read and installed without adding runtime dependencies. After changing scripts, run at least:

```powershell
python -m compileall -q .\archive-and-apply\scripts
python .\archive-and-apply\scripts\init_workspace.py .\tmp-workspace --language en --dry-run
```

For template or TeX-tool changes, also complete the smoke, compile, render, and page-by-page visual review workflow described above.

## License

[MIT](LICENSE)
