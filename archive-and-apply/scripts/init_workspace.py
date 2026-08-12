#!/usr/bin/env python3
"""Initialize a source-first archive-and-apply workspace without overwrites."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlannedFile:
    source: Path
    destination: Path


def localized(base: Path, stem: str, language: str, suffix: str = ".md") -> Path:
    language_suffix = "cn" if language == "zh" else "en"
    return base / f"{stem}.{language_suffix}{suffix}"


def build_plan(skill_root: Path, target: Path, language: str) -> tuple[list[Path], list[PlannedFile]]:
    assets = skill_root / "assets"
    scaffold = assets / "workspace-scaffold"
    source_templates = assets / "source-templates"
    cv_templates = assets / "cv-templates"
    interview_templates = assets / "interview-templates"
    academic_templates = assets / "academia-templates"
    job_templates = assets / "job-templates"
    scripts = skill_root / "scripts"

    directories = [
        target / "experiences",
        target / "projects",
        target / "publications" / "papers",
        target / "jobs" / "saved",
        target / "jobs" / "companies",
        target / "jobs" / "comparisons",
        target / "jobs" / "templates",
        target / "cv" / "templates",
        target / "cv" / "tools",
        target / "interview" / "coding",
        target / "interview" / "templates",
        target / "academia" / "templates",
        target / "academia" / "writing-samples",
        target / "discard",
    ]

    readme_source = scaffold / ("README.md" if language == "zh" else "README.en.md")
    agents_source = scaffold / ("AGENTS.md" if language == "zh" else "AGENTS.en.md")
    cv_readme = scaffold / "cv" / ("README.md" if language == "zh" else "README.en.md")
    cv_template_readme = scaffold / "cv" / "templates" / (
        "README.md" if language == "zh" else "README.en.md"
    )
    interview_readme = scaffold / "interview" / (
        "README.md" if language == "zh" else "README.en.md"
    )
    academia_readme = scaffold / "academia" / (
        "README.cn.md" if language == "zh" else "README.en.md"
    )

    files = [
        PlannedFile(readme_source, target / "README.md"),
        PlannedFile(agents_source, target / "AGENTS.md"),
        PlannedFile(scaffold / ".gitignore", target / ".gitignore"),
        PlannedFile(
            source_templates / ("TEMPLATE.cn.md" if language == "zh" else "TEMPLATE.en.md"),
            target / "TEMPLATE.md",
        ),
        PlannedFile(cv_readme, target / "cv" / "README.md"),
        PlannedFile(cv_template_readme, target / "cv" / "templates" / "README.md"),
        PlannedFile(
            cv_templates / ("CV_ENTRY_BANK.md" if language == "zh" else "CV_ENTRY_BANK.en.md"),
            target / "cv" / "CV_ENTRY_BANK.md",
        ),
        PlannedFile(
            cv_templates / ("CV_ENTRY_AUDIT.md" if language == "zh" else "CV_ENTRY_AUDIT.en.md"),
            target / "cv" / "CV_ENTRY_AUDIT.md",
        ),
        PlannedFile(interview_readme, target / "interview" / "README.md"),
        PlannedFile(
            localized(interview_templates, "interview", language),
            target / "interview" / "interview.md",
        ),
        PlannedFile(
            localized(job_templates, "README", language),
            target / "jobs" / "README.md",
        ),
        PlannedFile(
            localized(job_templates, "targets", language),
            target / "jobs" / "targets.md",
        ),
        PlannedFile(
            localized(job_templates, "applications", language),
            target / "jobs" / "applications.md",
        ),
        PlannedFile(
            localized(job_templates, "job", language),
            target / "jobs" / "templates" / "job.md",
        ),
        PlannedFile(
            localized(job_templates, "company", language),
            target / "jobs" / "templates" / "company.md",
        ),
        PlannedFile(academia_readme, target / "academia" / "README.md"),
    ]

    for stem in ["jd", "mock", "my-q"]:
        files.append(
            PlannedFile(
                localized(interview_templates, stem, language),
                target / "interview" / "templates" / f"{stem}.md",
            )
        )

    for stem in ["SOP", "RESEARCH_STATEMENT", "PERSONAL_STATEMENT", "PUBLICATION_SUMMARY", "REC_TRACKER"]:
        files.append(
            PlannedFile(
                localized(academic_templates, stem, language),
                target / "academia" / "templates" / f"{stem}.md",
            )
        )

    tex_names = ["cv_cn.tex", "cv_cn_1page.tex"] if language == "zh" else ["cv.tex", "cv_1page.tex"]
    for name in tex_names:
        files.append(PlannedFile(assets / "tex-templates" / name, target / "cv" / name))

    for name in [
        "setup_tex_dependencies.py",
        "detect_tex_dependencies.py",
        "check_tex_pages.py",
        "check_resume_layout.py",
        "check_pdf_fill.py",
    ]:
        files.append(PlannedFile(scripts / name, target / "cv" / "tools" / name))

    return directories, files


def validate_plan(skill_root: Path, files: list[PlannedFile]) -> None:
    missing = [item.source for item in files if not item.source.is_file()]
    if missing:
        formatted = "\n".join(f"  - {path}" for path in missing)
        raise SystemExit(f"Skill assets are incomplete:\n{formatted}")

    for item in files:
        if skill_root in item.destination.parents or item.destination == skill_root:
            raise SystemExit("Refusing to initialize a workspace inside the skill directory.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize an archive-and-apply workspace without overwriting existing files."
    )
    parser.add_argument("target", type=Path, help="Workspace directory to create")
    parser.add_argument("--language", choices=["zh", "en"], default="zh")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Allow a non-empty target and create only missing files",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without writing")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    target = args.target.expanduser().resolve()
    directories, files = build_plan(skill_root, target, args.language)
    validate_plan(skill_root, files)

    if target.exists() and not target.is_dir():
        raise SystemExit(f"Target exists and is not a directory: {target}")
    if target.exists() and any(target.iterdir()) and not args.merge:
        raise SystemExit(
            f"Target is not empty: {target}\n"
            "Inspect it first, then rerun with --merge to create only missing files."
        )

    directory_conflicts = [path for path in directories if path.exists() and not path.is_dir()]
    file_conflicts = [
        item.destination
        for item in files
        if item.destination.exists() and not item.destination.is_file()
    ]
    if directory_conflicts or file_conflicts:
        conflicts = directory_conflicts + file_conflicts
        formatted = "\n".join(f"  - {path}" for path in conflicts)
        raise SystemExit(f"Target contains path-type conflicts:\n{formatted}")

    existing = [item.destination for item in files if item.destination.exists()]
    print(f"Target: {target}")
    print(f"Language: {args.language}")
    print(f"Directories planned: {len(directories)}")
    print(f"Files planned: {len(files)}")
    if existing:
        print(f"Existing files preserved: {len(existing)}")

    if args.dry_run:
        for item in files:
            action = "preserve" if item.destination.exists() else "create"
            print(f"  [{action}] {item.destination}")
        return

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    created = 0
    for item in files:
        if item.destination.exists():
            continue
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.source, item.destination)
        created += 1

    print(f"Created files: {created}")
    print(f"Preserved files: {len(existing)}")
    print("Workspace initialized successfully.")


if __name__ == "__main__":
    main()
