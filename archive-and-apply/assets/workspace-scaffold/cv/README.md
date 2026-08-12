# CV 工作区

- `CV_ENTRY_BANK.md`：可复用、带来源的候选 bullet
- `CV_ENTRY_AUDIT.md`：特定目标的需求—证据矩阵与取舍
- `*.tex`：实际简历 / CV 源文件
- `tools/`：TeX 依赖、页数、PDF 边界框与文本提取检查

先确认行业 resume、学术 CV 或其他格式，再遵循目标方的页数和文件要求。版面检查是诊断，不是“必须填满页面”的硬规则。

写条目前先在 `CV_ENTRY_AUDIT.md` 记录预计阅读链。首条应让招聘 / HR 和非同领域负责人理解问题、范围、ownership 与价值；后续条目再给 team leader、技术面试官和未来同组 / 跨职能人员提供方法取舍、验证、接口、质量与团队杠杆。每个 claim 都应能在面试中准确解释，不能把团队结果全部归为个人成果。

```powershell
python cv/tools/setup_tex_dependencies.py --json
python cv/tools/setup_tex_dependencies.py --smoke --json
python cv/tools/detect_tex_dependencies.py cv/cv_cn.tex --json
python cv/tools/check_tex_pages.py cv/cv_cn.tex --target-pages 1 --output cv/check.pdf --render-dir cv/rendered --json
python cv/tools/check_resume_layout.py cv/check.pdf --render-dir cv/rendered --json
```

排版验收不只看页数：逐个检查换页前后各三行、孤立标题/条目、跨页 bullet、每页是否接近底边但未侵入安全边距、各页密度是否平衡、编译警告、字体嵌入、链接与文本提取。随后逐页查看 `cv/rendered/` 的 PNG，确认没有裁切、重叠、缺字、黑框、层级或间距问题。调整顺序应是删减/改写冗余内容、移动完整语义块、增加防断页控制、微调一致间距，最后才考虑边距或字号；禁止用填充内容或散落的负间距硬凑页底。

安装助手默认只检测。仅在审阅安装计划并取得用户明确确认后，才能运行 `python cv/tools/setup_tex_dependencies.py --install --yes`。TeX 发行版体积可能较大，也可能需要管理员权限和重启终端；不要静默替换已有但不完整的 TeX 安装。
