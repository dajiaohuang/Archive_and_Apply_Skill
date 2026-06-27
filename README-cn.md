# Archive and Apply Skill

一个可发布的 Codex skill，用于从零搭建并维护“个人 archive-and-apply 工作区”，把源经历条目持续转化为 CV、面试材料和公司定制申请材料。

这个 skill 基于真实工作流设计，目标仓库通常包含：

- `experiences/` 或历史 `internships/`
- `projects/`
- `publications/`
- `cv/`
- `interview/`

核心思路很简单：

1. 需要时先创建一个可用的 archive-and-apply 仓库。
2. 把详细 source entry 作为事实层。
3. 从 source entry 提炼 CV bullet、面试介绍和定制材料。
4. 随着工作流演进，持续保持整库一致。

## 这个 Skill 能做什么

- 在用户指定路径创建一个新的 archive-and-apply 工作区
- 探索本地目录、repo、材料文件夹，并把内容转成 source entry
- 先更新 source entry，再同步下游 `cv/` 和 `interview/`
- 从模板开始创建 source entry，而不是每次从空白文件写起
- 维护 `CV_ENTRY_BANK.md` 和 `CV_ENTRY_AUDIT.md`
- 维护中英文 `.tex` CV，并检测 TeX 依赖、编译结果、页数和页面填充
- 维护通用面试文件和公司定制面试目录
- 先保存 JD，再生成 `mock.md`
- 每个阶段结束后，用可多选的 next-step 菜单提示用户下一步可以做什么

## 中英文模板支持

这个 skill 现在同时提供中文和英文模板，适用于：

- source entry
- `CV_ENTRY_BANK.md`
- `CV_ENTRY_AUDIT.md`
- `interview/interview.md`
- `interview/<company>/jd.md`
- `interview/<company>/mock.md`
- `interview/<company>/my-q.md`

推荐约定：

- 如果用户想把整个工作区 都写成中文，就优先使用 `*.cn.md` 模板
- 如果用户想把整个工作区 都写成英文，就优先使用 `*.en.md` 模板
- 如果用户没有特别说明，优先沿用目标仓库现有语言

## 仓库结构

```text
archive-and-apply-skill-repo/
|-- README.md
|-- README-cn.md
|-- LICENSE
`-- archive-and-apply/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    |-- assets/
    |   |-- workspace-scaffold/
    |   |-- cv-templates/
    |   |-- interview-templates/
    |   |-- source-templates/
    |   `-- tex-templates/
    |-- scripts/
    `-- references/
```

## 安装

把 `archive-and-apply/` 复制到你的 Codex skills 目录：

```powershell
Copy-Item -Recurse .\archive-and-apply `
  $HOME\.codex\skills\archive-and-apply
```

如果设置了 `CODEX_HOME`，则使用：

```powershell
Copy-Item -Recurse .\archive-and-apply `
  $env:CODEX_HOME\skills\archive-and-apply
```

## 触发方式

示例：

```text
Use $archive-and-apply to create or maintain my archive-and-apply workspace, CV materials, and interview docs consistently.
```

首次建库的默认语言规则：

- 如果用户给 agent 的安装 prompt 或第一次调用 prompt 是中文，则默认按中文建库
- 否则默认按英文建库
- 如果用户明确指定了语言，以用户明确指定为准
- 如果目标 repo 已存在，则优先沿用该 repo 或目标目录已有语言，而不是按 prompt 默认值

## 典型用法

- “在这个目录里创建一个新的 archive-and-apply 工作区。”
- “探索这个 repo，把相关项目整理成 source entry。”
- “基于现在的条目生成 `CV_ENTRY_BANK.md`。”
- “按 data science 方向审计这版 CV 应该保留哪些条目和 Skills。”
- “给这个岗位建一个 `interview/<company>/` 目录，并保存 JD。”

## 许可证

MIT
