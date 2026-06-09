# AGENTS.md

本文件用于指导编码 agent 在这个仓库中的工作方式。

## 目的

这是一个个人经历资料库：以 source-first 为原则，沉淀 experiences、projects、publications、CV 产物和 interview 材料。

## 核心规则

- 把 `experiences/`、`projects/`、`publications/` 视为事实层 source of truth。
- 先从 `TEMPLATE.md` 创建或更新源条目，再派生 CV 和 interview 材料。
- 优先更新规范文件，而不是创建平行重复版本。
- 通用表达放在 `interview/interview.md`。
- 公司或岗位定制材料放在 `interview/<company>/`。
- 如果用户提供了 JD，先把它保存到对应公司目录中，通常命名为 `jd.md`。

## 预期目录结构

- `experiences/`
- `projects/`
- `publications/`
- `publications/papers/`
- `cv/`
- `interview/`
- `TEMPLATE.md`
- `README.md`

## CV 工作流

1. 创建或更新源条目
2. 同步 `cv/CV_ENTRY_BANK.md`
3. 更新 `.tex` 简历版本
4. 运行本地 TeX 依赖与页数检查

## Interview 工作流

1. 通用材料维护在 `interview/interview.md`
2. 为定向准备创建 `interview/<company>/`
3. 先保存 JD
4. 保存 JD 后，下一步通常是生成 `mock.md`
