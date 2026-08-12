#!/usr/bin/env python3
"""Inspect declared TeX dependencies, recursive includes, and local tools."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Optional


PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}")
CLASS_RE = re.compile(r"\\documentclass(?:\[[^\]]*\])?\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def resolve_include(parent: Path, value: str) -> Path:
    candidate = (parent / value).resolve()
    if candidate.suffix:
        return candidate
    return candidate.with_suffix(".tex")


def parse_project(root: Path) -> dict[str, object]:
    pending = [root]
    visited: set[Path] = set()
    packages: set[str] = set()
    classes: set[str] = set()
    inputs: list[dict[str, object]] = []

    while pending:
        path = pending.pop()
        if path in visited:
            continue
        visited.add(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for match in PACKAGE_RE.findall(text):
            packages.update(part.strip() for part in match.split(",") if part.strip())
        classes.update(value.strip() for value in CLASS_RE.findall(text) if value.strip())
        for raw_value in INPUT_RE.findall(text):
            resolved = resolve_include(path.parent, raw_value.strip())
            exists = resolved.is_file()
            inputs.append(
                {
                    "declared_in": str(path),
                    "value": raw_value.strip(),
                    "resolved": str(resolved),
                    "exists": exists,
                }
            )
            if exists and resolved not in visited:
                pending.append(resolved)

    needs_unicode_engine = bool(packages & {"ctex", "xeCJK", "fontspec"}) or any(
        name in {"ctexart", "ctexrep", "ctexbook"} for name in classes
    )
    preferred_engines = (
        ["xelatex", "tectonic", "pdflatex"]
        if needs_unicode_engine
        else ["pdflatex", "tectonic", "xelatex"]
    )
    return {
        "root_file": str(root),
        "tex_files": sorted(str(path) for path in visited),
        "documentclass": sorted(classes),
        "packages": sorted(packages),
        "inputs": inputs,
        "missing_inputs": [item for item in inputs if not item["exists"]],
        "preferred_engines": preferred_engines,
    }


def detect_tools() -> dict[str, Optional[str]]:
    return {
        tool: shutil.which(tool)
        for tool in [
            "latexmk",
            "pdflatex",
            "xelatex",
            "tectonic",
            "pdfinfo",
            "pdftotext",
            "pdftoppm",
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect declared TeX packages, recursive includes, and local tools."
    )
    parser.add_argument("tex_file", type=Path, help="Root .tex file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    tex_path = args.tex_file.expanduser().resolve()
    if not tex_path.is_file():
        raise SystemExit(f"Missing file: {tex_path}")
    if tex_path.suffix.lower() != ".tex":
        raise SystemExit(f"Expected a .tex file: {tex_path}")

    result = parse_project(tex_path)
    result["tools"] = detect_tools()
    result["available_preferred_engine"] = next(
        (result["tools"][name] for name in result["preferred_engines"] if result["tools"][name]),
        None,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Root TeX file: {result['root_file']}")
    print(f"TeX files found: {len(result['tex_files'])}")
    print("Document classes: " + (", ".join(result["documentclass"]) or "<none>"))
    print("Declared packages: " + (", ".join(result["packages"]) or "<none>"))
    print("Preferred engines: " + " -> ".join(result["preferred_engines"]))
    print(f"Available preferred engine: {result['available_preferred_engine'] or 'MISSING'}")
    if result["missing_inputs"]:
        print("Missing includes:")
        for item in result["missing_inputs"]:
            print(f"  - {item['value']} -> {item['resolved']}")
    print("Local tools:")
    for tool, found in result["tools"].items():
        print(f"  - {tool}: {found or 'MISSING'}")


if __name__ == "__main__":
    main()
