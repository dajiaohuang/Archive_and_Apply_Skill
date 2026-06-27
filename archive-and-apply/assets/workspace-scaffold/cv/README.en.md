# CV Workspace

The `cv/` folder stores the bridge between long-form experience notes and final resume outputs: TeX resumes, reusable entry banks, audit notes, and helper scripts.

## Key Files

- `cv.tex` / `cv_cn.tex`: current English / Chinese main resume
- `cv_1page.tex` / `cv_cn_1page.tex`: tighter one-page variants
- `CV_ENTRY_BANK.md`: reusable resume bullet bank
- `CV_ENTRY_AUDIT.md`: role-specific keep/drop decisions and Skills-section audit
- `templates/README.md`: template mapping and usage notes
- `tools/detect_tex_dependencies.py`: detect TeX tools and package dependencies
- `tools/check_tex_pages.py`: check actual page count and page-fill heuristics

## Common Commands

```powershell
python cv/tools/detect_tex_dependencies.py cv/cv.tex
python cv/tools/check_tex_pages.py cv/cv.tex --target-pages 1
python cv/tools/check_tex_pages.py cv/cv_cn.tex --target-pages 2
```

## Recommended Order

1. Update source entries first
2. Then update `CV_ENTRY_AUDIT.md`
3. Then update `CV_ENTRY_BANK.md`
4. Finally sync the target `.tex` CV and verify page count
