# CV Workspace

`cv/` 目录用于维护从经历库到最终简历的中间产物，包括 LaTeX 简历正文、条目池、审计记录，以及辅助检查脚本。

## 主要文件

- `cv.tex` / `cv_cn.tex`：当前英文 / 中文主简历
- `cv_1page.tex` / `cv_cn_1page.tex`：更紧凑的一页版变体
- `CV_ENTRY_BANK.md`：可复用简历条目池
- `CV_ENTRY_AUDIT.md`：不同岗位方向下的条目取舍、保留与放弃理由，以及 Skills 板块审计
- `templates/README.md`：模板来源与使用建议
- `tools/detect_tex_dependencies.py`：检测 TeX 依赖、宏包与编译工具
- `tools/check_tex_pages.py`：检查页数目标与每页是否填得足够满

## 常用命令

```powershell
python cv/tools/detect_tex_dependencies.py cv/cv.tex
python cv/tools/check_tex_pages.py cv/cv.tex --target-pages 1
python cv/tools/check_tex_pages.py cv/cv_cn.tex --target-pages 2
```

## 推荐顺序

1. 先更新 source entries
2. 再更新 `CV_ENTRY_AUDIT.md`
3. 然后更新 `CV_ENTRY_BANK.md`
4. 最后同步目标 `.tex` CV 并检查页数
