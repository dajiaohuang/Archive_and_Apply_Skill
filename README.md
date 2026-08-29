# Archive & Apply

> 把经历证据变成可追溯、可核验、可继续维护的申请材料。

[English](README-en.md) · [项目网站](https://dajiaohuang.github.io/Archive_and_Apply_Skill/) · [MIT License](LICENSE)

Archive & Apply 是一个中文优先、source-first 的 Codex skill。它接收仓库、笔记、PDF、职位描述或项目官方 Prompt，把事实整理成一套 canonical 证据层，再从中派生简历、岗位材料、面试包与学术申请文书。

它不是“替你编一份更好看的经历”。它的基本约束是：**每个重要 claim 都能回到来源；事实、推断与未知彼此分开；准备材料绝不被误记为已投递。**

```text
repo / 笔记 / PDF / 原始材料
              │
              ▼
经历 · 项目 · 论文（事实层）
       ├──► CV 条目池 ──► 目标简历 ──► TeX / PDF 检查
       ├──► JD 证据映射 ──► 投递材料与状态记录
       ├──► 通用故事库 ──► 岗位定制面试包
       └──► 学术证据映射 ──► 项目定制文书
```

## 为什么需要它

常见的申请工作流把事实散落在旧简历、聊天记录、项目仓库和临时文档里。每次投递都从头改写，容易出现三类问题：

- claim 比来源更强，面试时无法守住贡献边界；
- JD、公司调研、简历和面试答案彼此漂移；
- “已保存”“准备中”“已投递”等状态没有事件证据。

Archive & Apply 把事实层和派生层分开。事实变化先更新 source entry；只是措辞或岗位取舍变化时，只更新受影响的下游材料。

## 能做什么

| 工作流 | 产物 | 核心检查 |
|---|---|---|
| 证据导入 | 经历、项目、论文 source entry | 来源、日期、贡献边界、未知项 |
| 求职投递 | JD 快照、公司调研、匹配矩阵、事件式状态 | 原文与分析分离，状态不靠推测 |
| 简历 / CV | 条目池、岗位审计、目标 TeX/PDF | 多读者可读、claim 可追问、文本可提取 |
| 面试准备 | 通用故事库、目标岗位 mock、反问清单 | 每个答案有证据锚点 |
| 学术申请 | Prompt 记录、SOP、PS、研究陈述、推荐信追踪 | 官方要求优先，项目与院校信息不串用 |
| 版式核验 | PDF 诊断 JSON、逐页渲染 PNG | 页数、边界、断页、字体、链接、阅读顺序 |

## 快速开始

### 1. 安装 Skill

PowerShell：

```powershell
$skillRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
Copy-Item -Recurse .\archive-and-apply (Join-Path $skillRoot 'skills\archive-and-apply')
```

macOS / Linux：

```bash
skill_root="${CODEX_HOME:-$HOME/.codex}"
cp -R ./archive-and-apply "$skill_root/skills/archive-and-apply"
```

### 2. 直接进入流程

```text
$archive-and-apply
```

如果请求明确，Skill 会直接执行；只说“开始”时，它先只读检查当前工作区，指出最有价值的下一里程碑，并最多询问一个必要问题。

也可以让材料本身成为入口：

```text
用 $archive-and-apply 把这个仓库和项目笔记整理成可追溯的经历条目。
用 $archive-and-apply 保存这份 JD，分析匹配度并定制一页英文简历。
用 $archive-and-apply 检查这份 PDF 的断页、页底填充、字体和文本提取，并修正 TeX。
用 $archive-and-apply 根据这个项目的官方 Prompt 开始 SOP 流程。
```

### 3. 初始化独立工作区（可选）

先预览，再创建：

```powershell
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language zh --dry-run
python .\archive-and-apply\scripts\init_workspace.py C:\path\to\workspace --language zh
```

初始化器默认拒绝非空目录。检查后可使用 `--merge` 只补缺失文件；它不会覆盖已有文件。

## 工作区模型

推荐结构不是强制迁移规则。Skill 会先读取仓库内说明和现有 canonical 文件，再决定最小更新范围。

```text
experiences/                经历事实与来源
projects/                   项目事实与贡献边界
publications/               论文记录与状态
jobs/                       JD、公司调研、匹配与投递事件
cv/                         条目池、岗位审计、TeX 与检查工具
interview/                  通用故事与目标岗位面试包
academia/                   项目 Prompt 与学术申请材料
discard/                    明确归档的非 canonical 内容
```

## 简历不是一个读者

Archive & Apply 会根据岗位推断实际阅读路径，而不是只做关键词堆叠：

1. ATS / 解析器需要普通文本、标准结构和有来源的关键词；
2. 招聘 / HR 需要快速识别问题、范围、职责和可迁移信号；
3. hiring manager / team lead 需要判断所有权、决策和结果；
4. 技术面试官需要可以追问的方法、约束和验证；
5. 潜在同事与跨职能伙伴需要看清协作接口和贡献边界。

每条 bullet 都应能回答：你做了什么、为什么这样做、如何验证、谁还参与、什么仍未知。

## TeX / PDF 工具

依赖检测默认无副作用：

```powershell
python .\archive-and-apply\scripts\setup_tex_dependencies.py --json
python .\archive-and-apply\scripts\setup_tex_dependencies.py --smoke --json
```

只有在审阅安装计划并取得明确确认后，才应运行带 `--install --yes` 的系统级安装。已有 TeX 安装不会被静默替换。

检查单个 TeX / PDF：

```powershell
python .\archive-and-apply\scripts\detect_tex_dependencies.py path\to\cv.tex --json
python .\archive-and-apply\scripts\check_tex_pages.py path\to\cv.tex --target-pages 1 --output path\to\check.pdf --render-dir path\to\rendered --json
python .\archive-and-apply\scripts\check_resume_layout.py path\to\check.pdf --render-dir path\to\rendered --json
```

检查覆盖编译诊断、页数与页面尺寸、断页上下文、四边安全区、页底填充、字体嵌入、链接和文本提取。自动检查是诊断，不是视觉证明；生成的每一页 PNG 仍需逐页检查，也不能保证某个特定 ATS 的行为。

## 仓库结构

```text
archive-and-apply/
├── SKILL.md                 工作流入口与硬约束
├── agents/openai.yaml       Skill 界面元数据
├── references/              各工作流的判断与验证规则
├── scripts/                 初始化、依赖与版式检查工具
└── assets/
    ├── source-templates/    事实层模板
    ├── job-templates/       JD、公司与投递模板
    ├── cv-templates/        条目池与岗位审计模板
    ├── interview-templates/ 面试准备模板
    ├── academia-templates/  学术申请模板
    ├── tex-templates/       中英文 TeX 简历模板
    └── workspace-scaffold/  可初始化的完整工作区
```

## 不会做什么

- 不编造指标、日期、头衔、作者顺序、录用状态或贡献范围；
- 不把推断写成已核验事实；
- 不把“材料已准备”当作“申请已提交”；
- 不用同一模板只替换公司、学校或导师名称；
- 未经明确授权，不投递申请、不发送消息、不修改外部账户；
- 不把自动页数和边界检查描述成 ATS 兼容保证。

## 开发与验证

本仓库不要求额外运行时依赖即可阅读和安装 Skill。修改脚本后至少运行：

```powershell
python -m compileall -q .\archive-and-apply\scripts
python .\archive-and-apply\scripts\init_workspace.py .\tmp-workspace --language zh --dry-run
```

修改模板或 TeX 工具时，再按上面的 smoke、编译、渲染和逐页视觉检查流程验证。

## License

[MIT](LICENSE)
