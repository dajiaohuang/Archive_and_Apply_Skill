# Archive and Apply Skill

[English](README-en.md)

一个 source-first 的 Codex skill：把经历证据、职位信息和项目要求转化为可追溯的简历、投递材料、面试包与学术申请材料。

## 核心能力

- 初始化中英文 archive-and-apply 工作区
- 从 repo、笔记、PDF 或原始文本整理经历 / 项目 / 论文条目
- 保存 JD 原文、公司调研、岗位匹配矩阵和投递事件
- 维护带来源映射的 CV 条目池与目标岗位审计
- 按 ATS、招聘 / HR、hiring manager / team leader、技术面试官和未来同组人员的不同判断需求撰写分层可读、可追问的简历条目
- 生成并核验 TeX 简历的页数、文本提取与页面文本边界
- 维护通用面试故事和公司 / 岗位定制 mock
- 按官方 Prompt 维护 SOP、Personal Statement、Research Statement 与推荐信追踪

技能的硬约束是：不编造事实、不把准备材料当成已投递、不把同一模板只替换学校或公司名称后复用。

## 安装

```powershell
$skillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
Copy-Item -Recurse .\archive-and-apply (Join-Path $skillRoot 'skills\archive-and-apply')
```

## 调用示例

```text
Use $archive-and-apply to audit this workspace, preserve source evidence, and update only the application artifacts affected by my request.
```

## 初始化工作区

先预览，再创建：

```powershell
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language zh --dry-run
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language zh
```

初始化器默认拒绝非空目录；确认后可用 `--merge` 只补缺失文件，永不覆盖现有文件。

## 目录

```text
archive-and-apply/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
    ├── source-templates/
    ├── job-templates/
    ├── cv-templates/
    ├── interview-templates/
    ├── academia-templates/
    ├── tex-templates/
    └── workspace-scaffold/
```

## TeX / PDF 依赖安装

先进行无副作用检测和中英文烟测：

```powershell
python .\archive-and-apply\scripts\setup_tex_dependencies.py --json
python .\archive-and-apply\scripts\setup_tex_dependencies.py --smoke --json
```

脚本会按平台给出 XeLaTeX、PDF 工具和 `pypdf` 的安装计划，但默认不会安装。TeX 发行版通常体积较大，也可能要求管理员权限或重启终端；审阅计划并取得用户明确确认后，才可运行 `python .\archive-and-apply\scripts\setup_tex_dependencies.py --install --yes`。已有 TeX 安装不会被静默替换。

## 验证工具

```powershell
python .\archive-and-apply\scripts\detect_tex_dependencies.py path\to\cv.tex --json
python .\archive-and-apply\scripts\check_tex_pages.py path\to\cv.tex --target-pages 1 --output path\to\check.pdf --render-dir path\to\rendered --json
python .\archive-and-apply\scripts\check_resume_layout.py path\to\check.pdf --render-dir path\to\rendered --json
```

综合检查覆盖换页前后文、孤立标题/条目、跨页 bullet、每页底边填充与四边安全区、页面密度、编译警告、字体嵌入、链接和文本提取。仍须逐页检查渲染 PNG；自动检查不能替代视觉审查，也不能保证某个 ATS 的解析结果。

## License

MIT
