#!/usr/bin/env python3
"""Check whether PDF content fills the page to the bottom margin."""

import argparse
import re
import shutil
import subprocess
from pathlib import Path


def find_pdftotext(explicit_path: Path | None = None) -> Path:
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


def analyze_pdf(
    pdf_path: Path,
    pdftotext: Path,
    target_margin_inch: float = 0.42,
) -> None:
    result = subprocess.run(
        [str(pdftotext), "-bbox", str(pdf_path), "-"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"pdftotext failed: {error or result.returncode}")
    data = result.stdout.decode("utf-8", errors="replace")

    m = re.search(r'height="([\d.]+)"', data)
    if not m:
        raise SystemExit("No page height found in pdftotext output")
    page_h = float(m.group(1))

    ymins = [float(x) for x in re.findall(r'yMin="([\d.]+)"', data)]
    ymaxs = [float(x) for x in re.findall(r'yMax="([\d.]+)"', data)]

    if not ymins or not ymaxs:
        raise SystemExit("No word position data found in pdftotext output")

    first_top = min(ymins)
    last_bottom = max(ymaxs)

    margin_pts = target_margin_inch * 72
    top_gap = first_top
    bottom_gap = page_h - last_bottom
    content_h = last_bottom - first_top
    usable_h = page_h - 2 * margin_pts

    print(f"PDF:               {pdf_path.name}")
    print(f"Page:              {page_h:.0f} pts ({page_h/72:.1f}\")")
    print(f"Target margin:     {target_margin_inch:.2f}\" ({margin_pts:.0f} pts)")
    print()
    print(f"  First word:      yMin={first_top:.0f} ({first_top/72:.2f}\" from top)")
    print(f"  Last word:       yMax={last_bottom:.0f} ({last_bottom/72:.2f}\" from top)")
    print(f"  Content height:  {content_h:.0f} pts ({content_h/72:.1f}\")")
    print(f"  Usable height:   {usable_h:.0f} pts ({usable_h/72:.1f}\")")
    print(f"  Vertical fill:   {content_h/usable_h*100:.0f}% (content / usable)")
    print()
    print(f"  Top gap:         {top_gap:.0f} pts ({top_gap/72:.2f}\")")
    print(f"  Bottom gap:      {bottom_gap:.0f} pts ({bottom_gap/72:.2f}\")")
    print(f"  Bottom excess:   {bottom_gap - margin_pts:.0f} pts beyond margin"
          f" ({(bottom_gap - margin_pts)/72:.2f}\")")

    if bottom_gap > margin_pts + 5:
        print("\n  ❌ NOT filled to bottom margin")
        print(f"     Last content is {bottom_gap - margin_pts:.0f} pts"
              f" ({(bottom_gap - margin_pts)/72:.2f}\") above bottom margin edge")
    elif bottom_gap >= margin_pts - 5:
        print("\n  ✅ Content fills to bottom margin edge")
    else:
        print(f"\n  ⚠️ Content extends {margin_pts - bottom_gap:.0f} pts below bottom margin edge")


def main():
    parser = argparse.ArgumentParser(description="Check PDF fill to bottom margin")
    parser.add_argument("pdf_file", type=Path, help="Path to PDF file")
    parser.add_argument("--margin", type=float, default=0.42, help="Target margin in inches")
    parser.add_argument(
        "--pdftotext",
        type=Path,
        help="Explicit path to the Poppler pdftotext executable",
    )
    args = parser.parse_args()

    pdf = args.pdf_file.resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")
    analyze_pdf(pdf, find_pdftotext(args.pdftotext), args.margin)


if __name__ == "__main__":
    main()
