#!/usr/bin/env python3
"""Compile TeX and run comprehensive resume PDF layout checks."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:
        raise SystemExit("Install pypdf to run this script: python -m pip install pypdf") from exc

from check_resume_layout import analyze_resume_pdf, find_executable


def source_prefers_unicode_engine(tex_file: Path) -> bool:
    text = tex_file.read_text(encoding="utf-8", errors="replace")
    return bool(re.search(r"\\(?:usepackage\{(?:ctex|xeCJK|fontspec)\}|documentclass(?:\[[^]]*\])?\{ctex)", text))


def choose_engine(tex_file: Path, preferred: Optional[str] = None) -> str:
    if preferred:
        explicit = Path(preferred).expanduser()
        if explicit.is_file():
            return str(explicit.resolve())
        found = shutil.which(preferred)
        if found:
            return found
        raise SystemExit(f"Requested engine not found: {preferred}")

    candidates = (
        ["xelatex", "tectonic", "pdflatex"]
        if source_prefers_unicode_engine(tex_file)
        else ["pdflatex", "tectonic", "xelatex"]
    )
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
    raise SystemExit("No TeX engine found. Expected one of: pdflatex, xelatex, tectonic")


def compile_tex(tex_file: Path, engine_path: str, build_dir: Path, passes: int) -> tuple[Path, dict[str, object]]:
    engine_name = Path(engine_path).name.lower()
    if "tectonic" in engine_name:
        command = [engine_path, "--outdir", str(build_dir), str(tex_file)]
        run_count = 1
    else:
        command = [
            engine_path,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={build_dir}",
            tex_file.name,
        ]
        run_count = passes

    logs = []
    for run_number in range(1, run_count + 1):
        try:
            proc = subprocess.run(
                command,
                capture_output=True,
                text=True,
                errors="replace",
                cwd=tex_file.parent,
                check=False,
                timeout=180,
            )
        except subprocess.TimeoutExpired as exc:
            raise SystemExit(
                f"TeX compile timed out on pass {run_number}. A TeX package manager may be waiting "
                "for input; run setup/detection and resolve package prompts before retrying.\n{exc}"
            )
        if proc.returncode != 0:
            raise SystemExit(
                f"TeX compile failed on pass {run_number}.\n"
                f"Command: {' '.join(command)}\n"
                f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
        logs.append(proc.stdout + "\n" + proc.stderr)

    pdf_path = build_dir / f"{tex_file.stem}.pdf"
    if not pdf_path.is_file():
        raise SystemExit(f"Expected PDF not found: {pdf_path}")
    combined = "\n".join(logs)
    warning_patterns = [
        ("overfull_hbox", r"Overfull \\hbox.*"),
        ("overfull_vbox", r"Overfull \\vbox.*"),
        ("underfull_hbox", r"Underfull \\hbox.*"),
        ("underfull_vbox", r"Underfull \\vbox.*"),
        ("missing_character", r"Missing character:.*"),
        ("undefined_reference", r"LaTeX Warning:.*undefined.*"),
        ("rerun_required", r"LaTeX Warning:.*Rerun.*"),
    ]
    warnings = []
    for code, pattern in warning_patterns:
        for match in re.findall(pattern, combined, flags=re.IGNORECASE):
            item = {"code": code, "message": match.strip()}
            if item not in warnings:
                warnings.append(item)
    return pdf_path, {"passes": run_count, "warnings": warnings, "clean": not warnings}


def inspect_text(pdf_path: Path) -> dict[str, object]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(
            {
                "page": index,
                "characters_no_whitespace": len(re.sub(r"\s+", "", text)),
                "words": len(re.findall(r"\S+", text)),
                "text_extractable": bool(text.strip()),
            }
        )
    return {
        "page_count": len(reader.pages),
        "pages": pages,
        "all_pages_text_extractable": all(page["text_extractable"] for page in pages),
    }


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Compile TeX and check page count, page breaks, margins, fonts, links, and rendered layout."
    )
    parser.add_argument("tex_file", type=Path, help="Root .tex file")
    parser.add_argument("--engine", help="Engine name or executable path")
    parser.add_argument("--passes", type=int, default=2, help="Compile passes for pdfLaTeX/XeLaTeX")
    parser.add_argument("--target-pages", type=int, help="Expected page count")
    parser.add_argument("--margin", type=float, default=0.5, help="Expected bottom margin in inches")
    parser.add_argument("--tolerance", type=float, default=0.35, help="Allowed extra bottom whitespace in inches")
    parser.add_argument("--skip-layout", action="store_true", help="Skip comprehensive PDF layout analysis")
    parser.add_argument("--skip-bottom-fill", dest="skip_layout", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, help="Copy the compiled PDF to this path")
    parser.add_argument("--render-dir", type=Path, help="Render every page to PNG for visual review")
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--fail-on", choices=["none", "error", "warning"], default="none")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.passes < 1:
        raise SystemExit("--passes must be at least 1")
    if args.target_pages is not None and args.target_pages < 1:
        raise SystemExit("--target-pages must be at least 1")
    tex_file = args.tex_file.expanduser().resolve()
    if not tex_file.is_file() or tex_file.suffix.lower() != ".tex":
        raise SystemExit(f"Expected an existing .tex file: {tex_file}")

    engine_path = choose_engine(tex_file, args.engine)
    with tempfile.TemporaryDirectory(prefix="archive-apply-tex-") as temp_dir:
        compiled_pdf, compile_diagnostics = compile_tex(tex_file, engine_path, Path(temp_dir), args.passes)
        report = inspect_text(compiled_pdf)
        report.update({"tex_file": str(tex_file), "engine": engine_path, "compile_diagnostics": compile_diagnostics})
        if args.target_pages is not None:
            report["target_pages"] = args.target_pages
            report["target_match"] = report["page_count"] == args.target_pages

        if not args.skip_layout:
            try:
                pdftotext = find_executable("pdftotext")
                if pdftotext is None:
                    raise SystemExit("pdftotext was not found; install Poppler before layout analysis")
                report["layout"] = analyze_resume_pdf(
                    compiled_pdf,
                    pdftotext,
                    args.margin,
                    args.tolerance,
                    find_executable("pdffonts"),
                    find_executable("pdftoppm"),
                    args.render_dir.expanduser().resolve() if args.render_dir else None,
                    args.dpi,
                )
            except SystemExit as exc:
                report["layout"] = {"status": "skipped", "reason": str(exc)}

        if args.output:
            output = args.output.expanduser().resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.suffix.lower() != ".pdf":
                raise SystemExit(f"--output must end in .pdf: {output}")
            shutil.copy2(compiled_pdf, output)
            report["output_pdf"] = str(output)
            if report.get("layout", {}).get("pages"):
                report["layout"]["pdf_file"] = str(output)
        elif report.get("layout", {}).get("pages"):
            report["layout"].pop("pdf_file", None)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"TeX file: {report['tex_file']}")
        print(f"Engine: {report['engine']}")
        print(f"Page count: {report['page_count']}")
        if "target_pages" in report:
            print(f"Target pages: {report['target_pages']} (match={report['target_match']})")
        print(f"All pages text-extractable: {report['all_pages_text_extractable']}")
        for page in report["pages"]:
            print(
                f"  - page {page['page']}: words={page['words']}, "
                f"characters={page['characters_no_whitespace']}, "
                f"extractable={page['text_extractable']}"
            )
        if "output_pdf" in report:
            print(f"Output PDF: {report['output_pdf']}")
        print(f"Compile diagnostics clean: {report['compile_diagnostics']['clean']}")
        if report.get("layout", {}).get("status") == "skipped":
            print(f"Layout analysis: skipped ({report['layout']['reason']})")
        elif report.get("layout"):
            print(
                f"Layout status: {report['layout']['status']} "
                f"({report['layout']['summary']['errors']} errors, {report['layout']['summary']['warnings']} warnings)"
            )
            for page_break in report["layout"]["page_breaks"]:
                print(f"  - break after page {page_break['after_page']}: {page_break['status']}")
        print("Inspect every rendered page and page boundary; automation cannot prove visual quality or ATS behavior.")

    layout_summary = report.get("layout", {}).get("summary", {})
    has_errors = bool(layout_summary.get("errors")) or report.get("target_match") is False
    has_warnings = bool(layout_summary.get("warnings")) or not report["compile_diagnostics"]["clean"]
    if args.fail_on == "error" and has_errors:
        raise SystemExit(2)
    if args.fail_on == "warning" and (has_errors or has_warnings):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
