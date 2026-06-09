#!/usr/bin/env python3
import argparse
import json
import re
import shutil
from pathlib import Path


PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}")
CLASS_RE = re.compile(r"\\documentclass(?:\[[^\]]*\])?\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")


def parse_tex(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    packages = []
    for match in PACKAGE_RE.findall(text):
        packages.extend([p.strip() for p in match.split(",") if p.strip()])
    docclasses = [c.strip() for c in CLASS_RE.findall(text) if c.strip()]
    inputs = [i.strip() for i in INPUT_RE.findall(text) if i.strip()]
    return {
        "file": str(path),
        "documentclass": sorted(set(docclasses)),
        "packages": sorted(set(packages)),
        "inputs": sorted(set(inputs)),
    }


def detect_tools():
    tools = {}
    for tool in ["pdflatex", "xelatex", "tectonic", "pdfinfo"]:
        tools[tool] = shutil.which(tool)
    return tools


def main():
    parser = argparse.ArgumentParser(description="Detect LaTeX package and tool dependencies.")
    parser.add_argument("tex_file", help="Path to a .tex file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    tex_path = Path(args.tex_file).resolve()
    if not tex_path.exists():
        raise SystemExit(f"Missing file: {tex_path}")

    result = parse_tex(tex_path)
    result["tools"] = detect_tools()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"TeX file: {result['file']}")
    print("Document class:")
    for item in result["documentclass"] or ["<none found>"]:
        print(f"  - {item}")
    print("Packages:")
    for item in result["packages"] or ["<none found>"]:
        print(f"  - {item}")
    print("Included files:")
    for item in result["inputs"] or ["<none found>"]:
        print(f"  - {item}")
    print("Local tools:")
    for tool, found in result["tools"].items():
        status = found if found else "MISSING"
        print(f"  - {tool}: {status}")


if __name__ == "__main__":
    main()
