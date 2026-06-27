#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PyPDF2 import PdfReader


def choose_engine(preferred: str | None = None) -> str:
    if preferred:
        found = shutil.which(preferred)
        if found:
            return found
        raise SystemExit(f"Requested engine not found: {preferred}")
    for candidate in ["pdflatex", "xelatex", "tectonic"]:
        found = shutil.which(candidate)
        if found:
            return found
    raise SystemExit("No TeX engine found. Expected one of: pdflatex, xelatex, tectonic")


def compile_tex(tex_file: Path, engine_path: str):
    with tempfile.TemporaryDirectory() as td:
        build_dir = Path(td)
        work_tex = build_dir / tex_file.name
        work_tex.write_text(tex_file.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")

        cmd = [engine_path]
        engine_name = Path(engine_path).name.lower()
        if "tectonic" in engine_name:
            cmd += ["--outdir", str(build_dir), work_tex.name]
        else:
            cmd += [
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={build_dir}",
                work_tex.name,
            ]

        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=build_dir)
        if proc.returncode != 0:
            raise SystemExit(
                "TeX compile failed.\n"
                f"Command: {' '.join(cmd)}\n"
                f"STDOUT:\n{proc.stdout}\n"
                f"STDERR:\n{proc.stderr}"
            )

        pdf_path = build_dir / f"{tex_file.stem}.pdf"
        if not pdf_path.exists():
            raise SystemExit(f"Expected PDF not found: {pdf_path}")

        final_pdf = tex_file.with_suffix(".compiled-check.pdf")
        final_pdf.write_bytes(pdf_path.read_bytes())
        return final_pdf


def inspect_pdf(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    pages = []
    char_counts = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chars = len(re.sub(r"\s+", "", text))
        char_counts.append(chars)
        pages.append({"page": idx, "chars": chars})

    max_chars = max(char_counts) if char_counts else 0
    for page in pages:
        ratio = page["chars"] / max_chars if max_chars else 0.0
        page["fill_ratio"] = round(ratio, 3)
        if ratio >= 0.85:
            label = "well-filled"
        elif ratio >= 0.55:
            label = "acceptable"
        else:
            label = "sparse"
        page["fill_label"] = label

    return {"page_count": len(reader.pages), "pages": pages}


def main():
    parser = argparse.ArgumentParser(description="Compile a TeX resume and inspect page count and fill heuristics.")
    parser.add_argument("tex_file", help="Path to a .tex file")
    parser.add_argument("--engine", help="TeX engine to use, e.g. pdflatex or xelatex")
    parser.add_argument("--target-pages", type=int, choices=[1, 2], help="Expected page count")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    tex_file = Path(args.tex_file).resolve()
    if not tex_file.exists():
        raise SystemExit(f"Missing file: {tex_file}")

    engine_path = choose_engine(args.engine)
    compiled_pdf = compile_tex(tex_file, engine_path)
    report = inspect_pdf(compiled_pdf)
    report["tex_file"] = str(tex_file)
    report["compiled_pdf"] = str(compiled_pdf)
    report["engine"] = engine_path

    if args.target_pages is not None:
        report["target_pages"] = args.target_pages
        report["target_match"] = report["page_count"] == args.target_pages

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"TeX file: {report['tex_file']}")
    print(f"Engine: {report['engine']}")
    print(f"Compiled PDF: {report['compiled_pdf']}")
    print(f"Page count: {report['page_count']}")
    if "target_pages" in report:
        print(f"Target pages: {report['target_pages']}")
        print(f"Target match: {report['target_match']}")
    print("Per-page fill:")
    for page in report["pages"]:
        print(
            f"  - page {page['page']}: chars={page['chars']}, "
            f"fill_ratio={page['fill_ratio']}, status={page['fill_label']}"
        )


if __name__ == "__main__":
    main()
