#!/usr/bin/env python3
"""Report per-page PDF text bounds as a legacy quick diagnostic.

Use check_resume_layout.py for page-break, margin, font, link, and rendering QA.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional


def find_pdftotext(explicit_path: Optional[Path] = None) -> Path:
    if explicit_path is not None:
        path = explicit_path.expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"pdftotext not found: {path}")
        return path
    discovered = shutil.which("pdftotext") or shutil.which("pdftotext.exe")
    if discovered:
        return Path(discovered)
    raise SystemExit(
        "pdftotext was not found on PATH. Install Poppler or pass "
        "--pdftotext /absolute/path/to/pdftotext."
    )


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_bbox_xml(data: bytes, margin_inch: float, tolerance_inch: float) -> dict[str, object]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise SystemExit(f"Could not parse pdftotext bbox XML: {exc}") from exc

    margin_points = margin_inch * 72
    tolerance_points = tolerance_inch * 72
    pages: list[dict[str, object]] = []

    for index, page in enumerate((node for node in root.iter() if local_name(node.tag) == "page"), start=1):
        height = float(page.attrib["height"])
        width = float(page.attrib["width"])
        words = [node for node in page.iter() if local_name(node.tag) == "word"]
        if not words:
            pages.append(
                {"page": index, "width_points": width, "height_points": height, "word_count": 0, "status": "empty"}
            )
            continue

        y_mins = [float(word.attrib["yMin"]) for word in words]
        y_maxs = [float(word.attrib["yMax"]) for word in words]
        top_gap = min(y_mins)
        bottom_gap = height - max(y_maxs)
        excess = bottom_gap - margin_points
        if excess < -5:
            status = "below-target-margin"
        elif excess <= tolerance_points:
            status = "within-target-band"
        else:
            status = "whitespace-heavy"
        pages.append(
            {
                "page": index,
                "width_points": round(width, 2),
                "height_points": round(height, 2),
                "word_count": len(words),
                "top_gap_points": round(top_gap, 2),
                "bottom_gap_points": round(bottom_gap, 2),
                "content_height_points": round(max(y_maxs) - min(y_mins), 2),
                "target_margin_points": round(margin_points, 2),
                "excess_points": round(excess, 2),
                "status": status,
            }
        )
    if not pages:
        raise SystemExit("No pages found in pdftotext bbox output")
    return {
        "target_margin_inches": margin_inch,
        "tolerance_inches": tolerance_inch,
        "pages": pages,
    }


def analyze_pdf_file(
    pdf_path: Path,
    pdftotext: Path,
    margin_inch: float = 0.5,
    tolerance_inch: float = 0.35,
) -> dict[str, object]:
    proc = subprocess.run(
        [str(pdftotext), "-bbox", str(pdf_path), "-"],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        error = proc.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"pdftotext failed: {error or proc.returncode}")
    report = parse_bbox_xml(proc.stdout, margin_inch, tolerance_inch)
    report["pdf_file"] = str(pdf_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report per-page PDF text bounds. Results are diagnostics, not visual pass/fail proof."
    )
    parser.add_argument("pdf_file", type=Path, help="PDF file")
    parser.add_argument("--margin", type=float, default=0.5, help="Expected bottom margin in inches")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.35,
        help="Additional whitespace band above the expected margin in inches",
    )
    parser.add_argument("--pdftotext", type=Path, help="Explicit pdftotext executable")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.margin < 0 or args.tolerance < 0:
        raise SystemExit("--margin and --tolerance must be non-negative")
    pdf = args.pdf_file.expanduser().resolve()
    if not pdf.is_file():
        raise SystemExit(f"PDF not found: {pdf}")
    if pdf.suffix.lower() != ".pdf":
        raise SystemExit(f"Expected a PDF file: {pdf}")

    report = analyze_pdf_file(pdf, find_pdftotext(args.pdftotext), args.margin, args.tolerance)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"PDF: {report['pdf_file']}")
    print(
        f"Target margin: {report['target_margin_inches']:.2f} in; "
        f"tolerance: {report['tolerance_inches']:.2f} in"
    )
    for page in report["pages"]:
        if page["status"] == "empty":
            print(f"  - page {page['page']}: empty")
        else:
            print(
                f"  - page {page['page']}: words={page['word_count']}, "
                f"top_gap={page['top_gap_points']:.1f} pt, "
                f"bottom_gap={page['bottom_gap_points']:.1f} pt, "
                f"status={page['status']}"
            )
    print("Note: run check_resume_layout.py and inspect every rendered page for full layout QA.")


if __name__ == "__main__":
    main()
