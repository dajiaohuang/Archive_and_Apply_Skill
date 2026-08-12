#!/usr/bin/env python3
"""Detect and, with explicit confirmation, install resume TeX dependencies."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


REQUIRED_TOOLS = ("xelatex", "pdflatex", "pdftotext")
RECOMMENDED_TOOLS = ("latexmk", "biber", "kpsewhich", "pdftoppm", "pdffonts", "pdfinfo")


def candidate_bin_dirs() -> List[Path]:
    candidates: List[Path] = []
    if os.name == "nt":
        roots = [
            os.environ.get("LOCALAPPDATA"),
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
        ]
        for root_value in roots:
            if not root_value:
                continue
            root = Path(root_value)
            candidates.extend(
                [
                    root / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
                    root / "MiKTeX" / "miktex" / "bin" / "x64",
                ]
            )
        texlive_root = Path("C:/texlive")
        if texlive_root.is_dir():
            candidates.extend(sorted(texlive_root.glob("*/bin/windows"), reverse=True))
    elif platform.system() == "Darwin":
        candidates.extend([Path("/Library/TeX/texbin"), Path("/usr/local/bin"), Path("/opt/homebrew/bin")])
    else:
        texlive_root = Path("/usr/local/texlive")
        if texlive_root.is_dir():
            candidates.extend(sorted(texlive_root.glob("*/bin/*"), reverse=True))
        candidates.extend([Path("/usr/bin"), Path("/usr/local/bin")])
    return candidates


def find_tool(name: str) -> Optional[str]:
    discovered = (
        shutil.which(f"{name}.exe") or shutil.which(name)
        if os.name == "nt"
        else shutil.which(name)
    )
    if discovered:
        return str(Path(discovered).resolve())
    executable_names = [name, f"{name}.exe"] if os.name == "nt" else [name]
    for directory in candidate_bin_dirs():
        for executable in executable_names:
            candidate = directory / executable
            if candidate.is_file():
                return str(candidate.resolve())
    return None


def command_available(name: str) -> bool:
    return bool(shutil.which(name) or shutil.which(f"{name}.exe"))


def python_module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def compile_smoke(engine: str, chinese: bool) -> Dict[str, object]:
    source = (
        "\\documentclass[UTF8]{ctexart}\n"
        "\\usepackage[margin=1in]{geometry}\n"
        "\\begin{document}中文简历依赖测试。\\end{document}\n"
        if chinese
        else "\\documentclass{article}\n\\usepackage[margin=1in]{geometry}\n"
        "\\begin{document}Resume dependency test.\\end{document}\n"
    )
    label = "chinese" if chinese else "english"
    with tempfile.TemporaryDirectory(prefix="archive-apply-tex-smoke-") as temp_dir:
        temp = Path(temp_dir)
        tex_file = temp / f"{label}.tex"
        tex_file.write_text(source, encoding="utf-8")
        proc = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
            cwd=temp,
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
            timeout=180,
        )
        pdf_exists = (temp / f"{label}.pdf").is_file()
        output = (proc.stdout + "\n" + proc.stderr).strip()
        return {
            "status": "passed" if proc.returncode == 0 and pdf_exists else "failed",
            "returncode": proc.returncode,
            "pdf_created": pdf_exists,
            "diagnostic_tail": output[-3000:] if proc.returncode != 0 else "",
        }


def detect(run_smoke: bool) -> Dict[str, object]:
    tools = {name: find_tool(name) for name in REQUIRED_TOOLS + RECOMMENDED_TOOLS}
    python_modules = {
        "pypdf": python_module_available("pypdf") or python_module_available("PyPDF2")
    }
    smoke: Dict[str, object] = {"status": "not-run"}
    if run_smoke:
        smoke = {}
        if tools["pdflatex"]:
            try:
                smoke["english"] = compile_smoke(str(tools["pdflatex"]), chinese=False)
            except subprocess.TimeoutExpired:
                smoke["english"] = {"status": "timeout"}
        else:
            smoke["english"] = {"status": "skipped", "reason": "pdflatex missing"}
        if tools["xelatex"]:
            try:
                smoke["chinese"] = compile_smoke(str(tools["xelatex"]), chinese=True)
            except subprocess.TimeoutExpired:
                smoke["chinese"] = {"status": "timeout"}
        else:
            smoke["chinese"] = {"status": "skipped", "reason": "xelatex missing"}

    missing_required = [name for name in REQUIRED_TOOLS if not tools[name]]
    missing_recommended = [name for name in RECOMMENDED_TOOLS if not tools[name]]
    smoke_passed = (
        run_smoke
        and isinstance(smoke.get("english"), dict)
        and isinstance(smoke.get("chinese"), dict)
        and smoke["english"].get("status") == "passed"  # type: ignore[index]
        and smoke["chinese"].get("status") == "passed"  # type: ignore[index]
    )
    if not missing_required and python_modules["pypdf"] and (not run_smoke or smoke_passed):
        status = "ready"
    elif any(tools.values()):
        status = "partial"
    else:
        status = "missing"
    return {
        "status": status,
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "tools": tools,
        "python_modules": python_modules,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
        "smoke": smoke,
    }


def sudo_prefix() -> Tuple[List[str], Optional[str]]:
    if hasattr(os, "geteuid") and os.geteuid() == 0:  # type: ignore[attr-defined]
        return [], None
    if command_available("sudo"):
        return ["sudo"], None
    return ["sudo"], "sudo was not found; install as root or add sudo before using the apt plan."


def install_plan(report: Dict[str, object]) -> Tuple[List[List[str]], List[str]]:
    tools = report["tools"]
    modules = report["python_modules"]
    assert isinstance(tools, dict) and isinstance(modules, dict)
    needs_tex = not tools.get("xelatex") or not tools.get("pdflatex")
    needs_poppler = any(not tools.get(name) for name in ("pdftotext", "pdftoppm", "pdffonts", "pdfinfo"))
    commands: List[List[str]] = []
    notes: List[str] = []
    system = platform.system()

    if system == "Windows":
        if (needs_tex or needs_poppler) and not command_available("winget"):
            notes.append(
                "winget was not found. Install MiKTeX from https://miktex.org/download "
                "or TeX Live from https://tug.org/texlive/acquire-netinstall.html, then rerun detection."
            )
        elif needs_tex:
            commands.append(
                [
                    "winget",
                    "install",
                    "--id",
                    "MiKTeX.MiKTeX",
                    "--exact",
                    "--accept-source-agreements",
                    "--accept-package-agreements",
                ]
            )
        if needs_poppler and command_available("winget"):
            commands.append(
                [
                    "winget",
                    "install",
                    "--id",
                    "oschwartz10612.Poppler",
                    "--exact",
                    "--accept-source-agreements",
                    "--accept-package-agreements",
                ]
            )
    elif system == "Darwin":
        if (needs_tex or needs_poppler) and not command_available("brew"):
            notes.append(
                "Homebrew was not found. Install MacTeX from https://tug.org/mactex/ "
                "and Poppler separately, then rerun detection."
            )
        elif needs_tex:
            commands.append(["brew", "install", "--cask", "mactex-no-gui"])
        if needs_poppler and command_available("brew"):
            commands.append(["brew", "install", "poppler"])
    elif command_available("apt-get"):
        prefix, privilege_note = sudo_prefix()
        if privilege_note:
            notes.append(privilege_note)
        if needs_tex or needs_poppler:
            commands.append(prefix + ["apt-get", "update"])
        packages: List[str] = []
        if needs_tex:
            packages.extend(
                [
                    "texlive-xetex",
                    "texlive-latex-recommended",
                    "texlive-latex-extra",
                    "texlive-fonts-recommended",
                    "texlive-lang-chinese",
                    "latexmk",
                    "biber",
                ]
            )
        if needs_poppler:
            packages.append("poppler-utils")
        if packages:
            commands.append(prefix + ["apt-get", "install", "-y"] + packages)
    elif needs_tex or needs_poppler:
        notes.append(
            "Automatic installation is currently supported for Windows/winget, macOS/Homebrew, "
            "and Debian/Ubuntu apt. Use the official TeX Live installer for this platform: "
            "https://tug.org/texlive/quickinstall.html"
        )

    if not modules.get("pypdf"):
        commands.append([sys.executable, "-m", "pip", "install", "--user", "pypdf"])
    return commands, notes


def display_command(command: Sequence[str]) -> str:
    return subprocess.list2cmdline(list(command)) if os.name == "nt" else " ".join(command)


def execute_plan(commands: List[List[str]]) -> None:
    for command in commands:
        print(f"Running: {display_command(command)}", flush=True)
        try:
            proc = subprocess.run(command, check=False)
        except OSError as exc:
            raise SystemExit(f"Could not start install command: {display_command(command)}\n{exc}")
        if proc.returncode != 0:
            raise SystemExit(f"Install command failed with exit code {proc.returncode}: {display_command(command)}")


def print_report(report: Dict[str, object]) -> None:
    print(f"Status: {report['status']}")
    print(f"Platform: {report['platform']}")
    print("Tools:")
    for name, path in report["tools"].items():  # type: ignore[union-attr]
        print(f"  - {name}: {path or 'MISSING'}")
    print("Python modules:")
    for name, available in report["python_modules"].items():  # type: ignore[union-attr]
        print(f"  - {name}: {'available' if available else 'MISSING'}")
    if report["missing_required"]:
        print("Missing required: " + ", ".join(report["missing_required"]))  # type: ignore[arg-type]
    if report["missing_recommended"]:
        print("Missing recommended: " + ", ".join(report["missing_recommended"]))  # type: ignore[arg-type]
    if report["smoke"] != {"status": "not-run"}:
        print("Smoke tests:")
        for name, result in report["smoke"].items():  # type: ignore[union-attr]
            print(f"  - {name}: {result.get('status')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect and optionally install XeLaTeX, PDF tools, and Python dependencies."
    )
    parser.add_argument("--smoke", action="store_true", help="Compile minimal English and Chinese documents")
    parser.add_argument("--install", action="store_true", help="Install missing dependencies")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm that the displayed package-manager commands may modify the system",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON before any installation")
    args = parser.parse_args()

    report = detect(run_smoke=args.smoke and not args.install)
    plan, install_notes = install_plan(report)
    report["install_plan"] = [display_command(command) for command in plan]
    report["install_notes"] = install_notes
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
        if plan:
            print("Install plan:")
            for command in plan:
                print(f"  - {display_command(command)}")
        else:
            print("Install plan: no missing installable dependencies detected.")
        if install_notes:
            print("Install notes:")
            for note in install_notes:
                print(f"  - {note}")

    if not args.install:
        return
    if install_notes:
        raise SystemExit(
            "Automatic setup cannot safely satisfy every missing dependency; "
            "follow the install notes above, then rerun detection."
        )
    if not plan:
        print("Nothing to install.")
        return
    if not args.yes:
        raise SystemExit(
            "Refusing to install without --yes. Review the plan, obtain explicit user confirmation, "
            "then rerun with --install --yes."
        )
    execute_plan(plan)
    print("Installation commands completed. Reopen the terminal if PATH changed, then rerun with --smoke.")


if __name__ == "__main__":
    main()
