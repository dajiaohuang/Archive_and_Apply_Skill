#!/usr/bin/env python3
"""Inspect resume PDF geometry, page breaks, fonts, links, and rendered pages."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import median
from typing import Dict, List, Optional, Sequence, Tuple

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:
        raise SystemExit("Install pypdf to run this script: python -m pip install pypdf") from exc


SECTION_NAMES = {
    "education", "experience", "work experience", "professional experience",
    "selected projects", "projects", "research", "research experience",
    "publications", "skills", "technical skills", "awards", "honors",
    "certifications", "leadership", "activities", "summary", "profile",
    "教育背景", "教育经历", "工作经历", "实习经历", "经历", "项目经历",
    "项目", "科研经历", "研究经历", "论文与成果", "论文", "技能",
    "专业技能", "获奖经历", "荣誉奖项", "证书", "个人总结",
}
BULLET_PREFIXES = ("•", "●", "▪", "◦", "‣", "∙", "·", "- ", "– ", "— ")
TERMINAL_PUNCTUATION = (".", "!", "?", ";", ":", "。", "！", "？", "；", "：")
YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def find_executable(name: str, explicit: Optional[Path] = None) -> Optional[Path]:
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        if not candidate.is_file():
            raise SystemExit(f"{name} not found: {candidate}")
        return candidate
    found = (shutil.which(f"{name}.exe") or shutil.which(name)) if os.name == "nt" else shutil.which(name)
    return Path(found).resolve() if found else None


def run_external(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess:
    actual = list(command)
    if os.name == "nt" and Path(actual[0]).suffix.lower() in {".cmd", ".bat"}:
        actual = [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/s", "/c", subprocess.list2cmdline(actual)]
    return subprocess.run(actual, **kwargs)  # type: ignore[arg-type]


def line_text(words: Sequence[ET.Element]) -> str:
    return " ".join("".join(word.itertext()).strip() for word in words if "".join(word.itertext()).strip())


def merge_physical_lines(fragments: List[Dict[str, object]]) -> List[Dict[str, object]]:
    merged: List[Dict[str, object]] = []
    for fragment in sorted(fragments, key=lambda item: (float(item["y_min"]), float(item["x_min"]))):
        center = (float(fragment["y_min"]) + float(fragment["y_max"])) / 2
        match = None
        for candidate in reversed(merged[-4:]):
            candidate_center = (float(candidate["y_min"]) + float(candidate["y_max"])) / 2
            height = min(
                float(fragment["y_max"]) - float(fragment["y_min"]),
                float(candidate["y_max"]) - float(candidate["y_min"]),
            )
            if abs(center - candidate_center) <= max(2.5, height * 0.4):
                match = candidate
                break
        if match is None:
            merged.append(dict(fragment))
            continue
        parts = list(match["parts"]) + list(fragment["parts"])  # type: ignore[arg-type]
        parts.sort(key=lambda item: float(item["x_min"]))
        match.update(
            {
                "x_min": min(float(match["x_min"]), float(fragment["x_min"])),
                "x_max": max(float(match["x_max"]), float(fragment["x_max"])),
                "y_min": min(float(match["y_min"]), float(fragment["y_min"])),
                "y_max": max(float(match["y_max"]), float(fragment["y_max"])),
                "parts": parts,
                "text": " | ".join(str(part["text"]) for part in parts),
            }
        )
    return merged


def parse_bbox_layout(data: bytes) -> List[Dict[str, object]]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise SystemExit(f"Could not parse pdftotext bbox-layout XML: {exc}") from exc

    pages: List[Dict[str, object]] = []
    for page_number, page in enumerate(
        (node for node in root.iter() if local_name(node.tag) == "page"), start=1
    ):
        fragments: List[Dict[str, object]] = []
        for line in (node for node in page.iter() if local_name(node.tag) == "line"):
            words = [node for node in line.iter() if local_name(node.tag) == "word"]
            text = line_text(words)
            if not text:
                continue
            fragment = {
                "x_min": float(line.attrib["xMin"]),
                "y_min": float(line.attrib["yMin"]),
                "x_max": float(line.attrib["xMax"]),
                "y_max": float(line.attrib["yMax"]),
                "text": text,
            }
            fragment["parts"] = [dict(fragment)]
            fragments.append(fragment)
        pages.append(
            {
                "page": page_number,
                "width_points": float(page.attrib["width"]),
                "height_points": float(page.attrib["height"]),
                "fragments": fragments,
                "lines": merge_physical_lines(fragments),
            }
        )
    if not pages:
        raise SystemExit("No pages found in pdftotext bbox-layout output")
    return pages


def normalize_heading(text: str) -> str:
    cleaned = re.sub(r"\s*\|\s*.*$", "", text.strip())
    return re.sub(r"[^\w\u3400-\u9fff ]+", "", cleaned).strip().lower()


def is_section_heading(text: str) -> bool:
    return normalize_heading(text) in SECTION_NAMES


def is_bullet(text: str) -> bool:
    stripped = text.lstrip()
    return stripped.startswith(BULLET_PREFIXES)


def likely_entry_heading(text: str) -> bool:
    return bool(YEAR_RE.search(text)) and len(text.split()) <= 16 and not text.rstrip().endswith(TERMINAL_PUNCTUATION)


def add_issue(
    issues: List[Dict[str, object]],
    severity: str,
    code: str,
    message: str,
    page: Optional[int] = None,
    evidence: Optional[str] = None,
) -> None:
    item: Dict[str, object] = {"severity": severity, "code": code, "message": message}
    if page is not None:
        item["page"] = page
    if evidence:
        item["evidence"] = evidence
    issues.append(item)


def inspect_collisions(page: Dict[str, object], issues: List[Dict[str, object]]) -> None:
    fragments = page["fragments"]  # type: ignore[assignment]
    for index, left in enumerate(fragments):
        for right in fragments[index + 1 :]:
            x_overlap = min(float(left["x_max"]), float(right["x_max"])) - max(
                float(left["x_min"]), float(right["x_min"])
            )
            y_overlap = min(float(left["y_max"]), float(right["y_max"])) - max(
                float(left["y_min"]), float(right["y_min"])
            )
            smaller_height = min(
                float(left["y_max"]) - float(left["y_min"]),
                float(right["y_max"]) - float(right["y_min"]),
            )
            if x_overlap > 3.0 and y_overlap > max(2.0, smaller_height * 0.45):
                add_issue(
                    issues,
                    "error",
                    "text_boxes_overlap",
                    "Two extracted text lines overlap; inspect for clipping or collision.",
                    int(page["page"]),
                    f"{left['text']} <> {right['text']}",
                )


def page_geometry(
    page: Dict[str, object],
    page_count: int,
    margin_inch: float,
    tolerance_inch: float,
    issues: List[Dict[str, object]],
) -> Dict[str, object]:
    lines: List[Dict[str, object]] = page["lines"]  # type: ignore[assignment]
    width = float(page["width_points"])
    height = float(page["height_points"])
    page_number = int(page["page"])
    if not lines:
        add_issue(issues, "error", "blank_page", "The page contains no extractable text.", page_number)
        return {"page": page_number, "status": "empty", "line_count": 0}

    x_min = min(float(line["x_min"]) for line in lines)
    x_max = max(float(line["x_max"]) for line in lines)
    y_min = min(float(line["y_min"]) for line in lines)
    y_max = max(float(line["y_max"]) for line in lines)
    gaps = [
        max(0.0, float(lines[index + 1]["y_min"]) - float(lines[index]["y_max"]))
        for index in range(len(lines) - 1)
    ]
    typical_gap = median(gaps) if gaps else 0.0
    largest_gap = max(gaps) if gaps else 0.0
    margin = margin_inch * 72
    tolerance = tolerance_inch * 72
    intrusion = 0.10 * 72
    bottom_gap = height - y_max
    right_gap = width - x_max
    usable_height = max(1.0, height - 2 * margin)
    fill_ratio = max(0.0, min(1.5, (y_max - y_min) / usable_height))

    if bottom_gap < margin - intrusion:
        add_issue(issues, "error", "bottom_margin_intrusion", "Text enters the expected bottom-margin safety band.", page_number)
    elif bottom_gap > margin + tolerance:
        severity = "error" if page_number < page_count else "warning"
        add_issue(
            issues,
            severity,
            "page_ends_too_high",
            "Content ends well above the target bottom band; reconsider the page break or page count without adding filler.",
            page_number,
            f"bottom gap {bottom_gap / 72:.2f} in",
        )
    if x_min < margin - intrusion:
        add_issue(issues, "error", "left_margin_intrusion", "Text enters the expected left-margin safety band.", page_number)
    if right_gap < margin - intrusion:
        add_issue(issues, "error", "right_margin_intrusion", "Text enters the expected right-margin safety band.", page_number)
    if y_min < margin - intrusion:
        add_issue(issues, "error", "top_margin_intrusion", "Text enters the expected top-margin safety band.", page_number)
    if page_number > 1 and y_min > margin + tolerance:
        add_issue(
            issues,
            "warning",
            "continuation_starts_too_low",
            "A continuation page starts unusually far below the top margin.",
            page_number,
            f"top gap {y_min / 72:.2f} in",
        )
    if largest_gap > max(43.2, typical_gap * 4 if typical_gap else 43.2):
        add_issue(
            issues,
            "warning",
            "large_internal_gap",
            "A large vertical gap may indicate uneven spacing or hidden layout pressure.",
            page_number,
            f"largest gap {largest_gap / 72:.2f} in",
        )

    inspect_collisions(page, issues)
    return {
        "page": page_number,
        "width_points": round(width, 2),
        "height_points": round(height, 2),
        "line_count": len(lines),
        "word_count": sum(len(str(line["text"]).split()) for line in lines),
        "top_gap_points": round(y_min, 2),
        "bottom_gap_points": round(bottom_gap, 2),
        "left_gap_points": round(x_min, 2),
        "right_gap_points": round(right_gap, 2),
        "content_span_points": round(y_max - y_min, 2),
        "fill_ratio": round(fill_ratio, 3),
        "bottom_status": "near-target" if bottom_gap <= margin + tolerance and bottom_gap >= margin - intrusion else (
            "intrudes-margin" if bottom_gap < margin - intrusion else "ends-high"
        ),
        "first_lines": [str(line["text"]) for line in lines[:3]],
        "last_lines": [str(line["text"]) for line in lines[-3:]],
    }


def inspect_page_breaks(pages: List[Dict[str, object]], issues: List[Dict[str, object]]) -> List[Dict[str, object]]:
    breaks: List[Dict[str, object]] = []
    for index in range(len(pages) - 1):
        before: List[Dict[str, object]] = pages[index]["lines"]  # type: ignore[assignment]
        after: List[Dict[str, object]] = pages[index + 1]["lines"]  # type: ignore[assignment]
        if not before or not after:
            continue
        page_number = index + 1
        break_issues: List[str] = []
        last_text = str(before[-1]["text"]).strip()
        first_text = str(after[0]["text"]).strip()

        if is_section_heading(last_text):
            code = "section_heading_stranded"
            break_issues.append(code)
            add_issue(issues, "error", code, "A section heading is stranded at the bottom of the page.", page_number, last_text)
        elif len(before) >= 2 and is_section_heading(str(before[-2]["text"])):
            code = "section_has_one_following_line"
            break_issues.append(code)
            add_issue(
                issues, "warning", code,
                "A section heading has only one following line before the page break.",
                page_number, str(before[-2]["text"]),
            )
        if likely_entry_heading(last_text):
            code = "entry_heading_stranded"
            break_issues.append(code)
            add_issue(issues, "error", code, "An entry heading/date line is stranded without body content.", page_number, last_text)
        elif len(before) >= 2 and likely_entry_heading(str(before[-2]["text"])):
            code = "entry_has_one_following_line"
            break_issues.append(code)
            add_issue(
                issues, "warning", code,
                "An entry heading has only one following line before the break; keep it with the first bullet where practical.",
                page_number, str(before[-2]["text"]),
            )

        next_heading_index = next(
            (position for position, line in enumerate(after[:4]) if is_section_heading(str(line["text"]))),
            None,
        )
        if next_heading_index == 1:
            code = "single_line_at_page_top"
            break_issues.append(code)
            add_issue(
                issues, "warning", code,
                "Only one line appears before the next section heading; this may be a widow or split entry.",
                page_number + 1, first_text,
            )
        if (
            not last_text.endswith(TERMINAL_PUNCTUATION)
            and not is_section_heading(last_text)
            and not likely_entry_heading(last_text)
            and not is_bullet(first_text)
            and not is_section_heading(first_text)
            and not likely_entry_heading(first_text)
        ):
            code = "possible_cross_page_continuation"
            break_issues.append(code)
            add_issue(
                issues, "warning", code,
                "The text appears to continue across the page boundary; visually verify that a bullet or paragraph was not split awkwardly.",
                page_number,
                f"{last_text} / {first_text}",
            )
        if is_bullet(first_text) and len(after) >= 2 and is_section_heading(str(after[1]["text"])):
            code = "single_bullet_at_page_top"
            break_issues.append(code)
            add_issue(
                issues, "warning", code,
                "A lone bullet precedes the next section at the top of the page.",
                page_number + 1, first_text,
            )

        breaks.append(
            {
                "after_page": page_number,
                "status": "review" if break_issues else "no_heuristic_issue",
                "issue_codes": break_issues,
                "before": [str(line["text"]) for line in before[-3:]],
                "after": [str(line["text"]) for line in after[:3]],
            }
        )
    return breaks


def inspect_fonts(pdf: Path, pdffonts: Optional[Path], issues: List[Dict[str, object]]) -> Dict[str, object]:
    if pdffonts is None:
        return {"status": "skipped", "reason": "pdffonts not found"}
    proc = run_external([str(pdffonts), str(pdf)], capture_output=True, text=True, errors="replace", check=False)
    if proc.returncode != 0:
        return {"status": "skipped", "reason": proc.stderr.strip() or f"exit {proc.returncode}"}
    fonts: List[Dict[str, object]] = []
    pattern = re.compile(r"^(.*?)\s{2,}(.*?)\s{2,}(.*?)\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+(\d+)\s+(\d+)\s*$")
    for line in proc.stdout.splitlines()[2:]:
        match = pattern.match(line)
        if not match:
            continue
        font = {
            "name": match.group(1).strip(), "type": match.group(2).strip(),
            "encoding": match.group(3).strip(), "embedded": match.group(4) == "yes",
            "subset": match.group(5) == "yes", "to_unicode": match.group(6) == "yes",
        }
        fonts.append(font)
        if not font["embedded"]:
            add_issue(issues, "error", "font_not_embedded", "A PDF font is not embedded.", evidence=str(font["name"]))
        if not font["to_unicode"]:
            add_issue(
                issues, "warning", "font_without_unicode_map",
                "A font lacks an explicit ToUnicode map; verify copied/extracted text.", evidence=str(font["name"]),
            )
        if "Type 3" in str(font["type"]):
            add_issue(
                issues, "warning", "type3_font",
                "A Type 3 font can render or extract inconsistently in some systems.", evidence=str(font["name"]),
            )
    return {"status": "checked", "fonts": fonts, "all_embedded": all(bool(font["embedded"]) for font in fonts)}


def inspect_pdf_structure(pdf: Path, issues: List[Dict[str, object]]) -> Dict[str, object]:
    reader = PdfReader(str(pdf))
    page_sizes: List[Tuple[float, float]] = []
    links: List[Dict[str, object]] = []
    extraction: List[Dict[str, object]] = []
    for page_number, page in enumerate(reader.pages, start=1):
        page_sizes.append((round(float(page.mediabox.width), 2), round(float(page.mediabox.height), 2)))
        text = page.extract_text() or ""
        replacement_count = text.count("�")
        extraction.append(
            {
                "page": page_number,
                "characters_no_whitespace": len(re.sub(r"\s+", "", text)),
                "text_extractable": bool(text.strip()),
                "replacement_characters": replacement_count,
            }
        )
        if not text.strip():
            add_issue(issues, "error", "text_not_extractable", "No text could be extracted from the page.", page_number)
        if replacement_count:
            add_issue(
                issues, "warning", "replacement_characters",
                "Extracted text contains Unicode replacement characters.", page_number, str(replacement_count),
            )
        annotations = page.get("/Annots") or []
        if hasattr(annotations, "get_object"):
            annotations = annotations.get_object()
        for annotation_ref in annotations:
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A") or {}
            uri = str(action.get("/URI") or "")
            links.append({"page": page_number, "uri": uri})
            if not uri:
                add_issue(issues, "warning", "empty_link_target", "A link annotation has no URI target.", page_number)
    if len(set(page_sizes)) > 1:
        add_issue(issues, "error", "inconsistent_page_size", "Page dimensions are inconsistent across the PDF.")
    return {"page_count": len(reader.pages), "page_sizes": page_sizes, "text_extraction": extraction, "links": links}


def render_pages(pdf: Path, pdftoppm: Path, render_dir: Path, dpi: int) -> List[str]:
    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / f"{pdf.stem}-page"
    proc = run_external(
        [str(pdftoppm), "-png", "-r", str(dpi), str(pdf), str(prefix)],
        capture_output=True, text=True, errors="replace", check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(f"pdftoppm failed: {proc.stderr.strip() or proc.returncode}")
    return [str(path.resolve()) for path in sorted(render_dir.glob(f"{prefix.name}-*.png"))]


def analyze_resume_pdf(
    pdf: Path,
    pdftotext: Path,
    margin_inch: float = 0.5,
    tolerance_inch: float = 0.35,
    pdffonts: Optional[Path] = None,
    pdftoppm: Optional[Path] = None,
    render_dir: Optional[Path] = None,
    dpi: int = 144,
) -> Dict[str, object]:
    bbox = run_external(
        [str(pdftotext), "-bbox-layout", str(pdf), "-"], capture_output=True, check=False
    )
    if bbox.returncode != 0:
        error = bbox.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"pdftotext failed: {error or bbox.returncode}")
    raw_pages = parse_bbox_layout(bbox.stdout)
    issues: List[Dict[str, object]] = []
    structure = inspect_pdf_structure(pdf, issues)
    page_reports = [
        page_geometry(page, len(raw_pages), margin_inch, tolerance_inch, issues)
        for page in raw_pages
    ]
    page_breaks = inspect_page_breaks(raw_pages, issues)
    fill_ratios = [float(page["fill_ratio"]) for page in page_reports if "fill_ratio" in page]
    if len(fill_ratios) > 1 and max(fill_ratios) - min(fill_ratios) > 0.18:
        add_issue(
            issues, "warning", "page_density_imbalance",
            "Content density differs substantially across pages; inspect ordering and the chosen page count.",
            evidence=f"fill ratios {', '.join(f'{value:.2f}' for value in fill_ratios)}",
        )
    fonts = inspect_fonts(pdf, pdffonts, issues)
    rendered: Dict[str, object] = {"status": "not-requested", "manual_review_required": True}
    if render_dir is not None:
        if pdftoppm is None:
            rendered = {"status": "skipped", "reason": "pdftoppm not found", "manual_review_required": True}
        else:
            images = render_pages(pdf, pdftoppm, render_dir, dpi)
            rendered = {
                "status": "rendered", "dpi": dpi, "images": images,
                "manual_review_required": True,
                "review_for": [
                    "clipped or overlapping text", "broken glyphs or black squares",
                    "hierarchy and alignment", "awkward page breaks", "uneven spacing and page balance",
                ],
            }
    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    return {
        "pdf_file": str(pdf),
        "status": "error" if errors else ("warning" if warnings else "pass"),
        "summary": {"errors": errors, "warnings": warnings, "manual_visual_review_required": True},
        "criteria": {"target_margin_inches": margin_inch, "bottom_tolerance_inches": tolerance_inch},
        "structure": structure,
        "pages": page_reports,
        "page_breaks": page_breaks,
        "fonts": fonts,
        "render": rendered,
        "issues": issues,
    }


def print_human(report: Dict[str, object]) -> None:
    print(f"PDF: {report['pdf_file']}")
    print(f"Status: {report['status']} ({report['summary']['errors']} errors, {report['summary']['warnings']} warnings)")  # type: ignore[index]
    for page in report["pages"]:  # type: ignore[assignment]
        if page.get("status") == "empty":
            print(f"  - page {page['page']}: empty")
        else:
            print(
                f"  - page {page['page']}: bottom_gap={page['bottom_gap_points'] / 72:.2f} in, "
                f"fill={page['fill_ratio']:.2f}, bottom={page['bottom_status']}"
            )
    for page_break in report["page_breaks"]:  # type: ignore[assignment]
        print(f"  - break after page {page_break['after_page']}: {page_break['status']}")
        print(f"    before: {' / '.join(page_break['before'])}")
        print(f"    after: {' / '.join(page_break['after'])}")
    for issue in report["issues"]:  # type: ignore[assignment]
        location = f" page={issue['page']}" if "page" in issue else ""
        print(f"[{str(issue['severity']).upper()}] {issue['code']}{location}: {issue['message']}")
    if report["render"]["status"] == "rendered":  # type: ignore[index]
        print("Rendered pages:")
        for image in report["render"]["images"]:  # type: ignore[index]
            print(f"  - {image}")
    print("Manual review is still required for every rendered page and every page boundary.")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Run comprehensive resume PDF layout and page-break checks.")
    parser.add_argument("pdf_file", type=Path)
    parser.add_argument("--margin", type=float, default=0.5, help="Expected edge margin in inches")
    parser.add_argument("--tolerance", type=float, default=0.35, help="Allowed extra bottom whitespace in inches")
    parser.add_argument("--pdftotext", type=Path)
    parser.add_argument("--pdffonts", type=Path)
    parser.add_argument("--pdftoppm", type=Path)
    parser.add_argument("--render-dir", type=Path, help="Render all pages to PNG for required visual review")
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--fail-on", choices=["none", "error", "warning"], default="none")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.margin < 0 or args.tolerance < 0 or args.dpi < 72:
        raise SystemExit("Margins/tolerance must be non-negative and --dpi must be at least 72")
    pdf = args.pdf_file.expanduser().resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        raise SystemExit(f"Expected an existing PDF file: {pdf}")
    pdftotext = find_executable("pdftotext", args.pdftotext)
    if pdftotext is None:
        raise SystemExit("pdftotext was not found; install Poppler or pass --pdftotext")
    render_dir = args.render_dir.expanduser().resolve() if args.render_dir else None
    report = analyze_resume_pdf(
        pdf, pdftotext, args.margin, args.tolerance,
        find_executable("pdffonts", args.pdffonts),
        find_executable("pdftoppm", args.pdftoppm),
        render_dir, args.dpi,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
    if args.fail_on == "error" and report["summary"]["errors"]:  # type: ignore[index]
        sys.exit(2)
    if args.fail_on == "warning" and (report["summary"]["errors"] or report["summary"]["warnings"]):  # type: ignore[index]
        sys.exit(2)


if __name__ == "__main__":
    main()
