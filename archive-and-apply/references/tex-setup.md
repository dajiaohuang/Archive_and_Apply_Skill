# TeX Dependency Setup

Use this reference before compiling a resume when XeLaTeX or supporting tools may be missing.

## Required and recommended dependencies

- Required for bundled bilingual templates: `xelatex`, `pdflatex`, `pdftotext`, and Python `pypdf` or `PyPDF2`.
- Recommended for broader projects and layout QA: `latexmk`, `biber`, `kpsewhich`, `pdftoppm`, `pdffonts`, and `pdfinfo`.
- Chinese templates require the `ctex` package and its language/font support.

## Safe workflow

1. Detect tools without changing the system:

   ```bash
   python scripts/setup_tex_dependencies.py --json
   ```

2. Run English and Chinese smoke compiles when engines exist:

   ```bash
   python scripts/setup_tex_dependencies.py --smoke --json
   ```

3. If dependencies are missing, show the proposed install commands and explain that TeX distributions can be large, take time, prompt for elevation, and change `PATH`.
4. Obtain explicit user confirmation immediately before installation.
5. Only after confirmation, run:

   ```bash
   python scripts/setup_tex_dependencies.py --install --yes
   ```

6. Reopen the terminal if requested, rerun `--smoke`, then compile the actual template.

Never add `--yes` merely to bypass the confirmation boundary.

## Platform behavior

- **Windows:** installs per-machine/user MiKTeX through `winget` when TeX is absent and Poppler when PDF tools are absent. MiKTeX may prompt before downloading missing TeX packages; use MiKTeX Console to choose `Ask me` or `Always install missing packages on-the-fly` and check updates.
- **macOS:** uses Homebrew `mactex-no-gui` plus `poppler`. A new terminal may be required before TeX commands appear.
- **Debian/Ubuntu:** uses `apt-get` for XeLaTeX, common LaTeX packages, Chinese language support, `latexmk`, `biber`, and Poppler. It may require `sudo`.
- **Other platforms:** stop and provide the official TeX Live installer route; do not guess distribution package names.

If the dedicated `latex-doctor` and `texlive-runtime-installer` skills are available, prefer them when the user wants a Codex-managed, isolated full TeX Live runtime. That installer is detect-only by default and its full managed installation also requires explicit confirmation.

## Existing partial installations

Do not silently replace a detected TeX installation. If the smoke test fails:

1. read the diagnostic tail for a missing package or font
2. use the distribution's package manager or console to repair it
3. rerun the smoke test
4. offer a separate managed TeX Live runtime only when the user explicitly requests it

## Authoritative references

- MiKTeX Windows installation: <https://miktex.org/howto/install-miktex>
- MiKTeX package-on-the-fly settings: <https://miktex.org/howto/miktex-console>
- TeX Live quick installation: <https://tug.org/texlive/quickinstall.html>
- MacTeX: <https://tug.org/mactex/>
