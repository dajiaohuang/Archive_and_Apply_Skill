# Archive and Apply Skill

[中文](README.md)

A source-first Codex skill that turns experience evidence, job information, and program requirements into traceable resumes, application materials, interview packs, and academic statements.

## Capabilities

- initialize Chinese- or English-first archive-and-apply workspaces
- ingest repositories, notes, PDFs, or raw text into experience, project, and publication entries
- preserve raw JDs, company research, requirement-to-evidence maps, and application events
- maintain a sourced CV entry bank and target-specific audit
- write progressively disclosed, interview-defensible entries for ATS, recruiting/HR, hiring managers/team leads, technical reviewers, and potential peers
- compile TeX resumes and inspect page count, text extraction, and page text bounds
- maintain reusable interview stories and target-specific mock packs
- draft SOP, personal, research, and recommendation-tracking materials from official prompts

The skill never invents facts, treats prepared materials as proof of submission, or performs name-only customization across companies or schools.

## Install

```powershell
$skillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
Copy-Item -Recurse .\archive-and-apply (Join-Path $skillRoot 'skills\archive-and-apply')
```

## Example invocation

```text
Use $archive-and-apply to audit this workspace, preserve source evidence, and update only the application artifacts affected by my request.
```

## Initialize a workspace

Preview, then create:

```powershell
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language en --dry-run
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language en
```

The initializer refuses a non-empty target by default. After inspection, `--merge` creates only missing files and never overwrites existing ones.

## Layout

```text
archive-and-apply/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
    ├── source-templates/
    ├── job-templates/
    ├── cv-templates/
    ├── interview-templates/
    ├── academia-templates/
    ├── tex-templates/
    └── workspace-scaffold/
```

## TeX / PDF dependency setup

Start with side-effect-free detection and English/Chinese smoke tests:

```powershell
python .\archive-and-apply\scripts\setup_tex_dependencies.py --json
python .\archive-and-apply\scripts\setup_tex_dependencies.py --smoke --json
```

The helper proposes a platform-specific plan for XeLaTeX, PDF tools, and `pypdf`, but installs nothing by default. TeX distributions can be large and may require elevation or a terminal restart. Only after reviewing the plan and obtaining explicit user confirmation should an agent run `python .\archive-and-apply\scripts\setup_tex_dependencies.py --install --yes`. Existing TeX installations are never silently replaced.

## Validation tools

```powershell
python .\archive-and-apply\scripts\detect_tex_dependencies.py path\to\cv.tex --json
python .\archive-and-apply\scripts\check_tex_pages.py path\to\cv.tex --target-pages 1 --output path\to\check.pdf --render-dir path\to\rendered --json
python .\archive-and-apply\scripts\check_resume_layout.py path\to\check.pdf --render-dir path\to\rendered --json
```

The comprehensive check covers page-boundary context, stranded headings/entries, split bullets, bottom fill and all edge safety bands, page density, compile warnings, font embedding, links, and text extraction. Every rendered PNG still requires visual review; automation cannot guarantee behavior in a particular ATS.

## License

MIT
