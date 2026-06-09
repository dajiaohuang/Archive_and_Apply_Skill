# 个人经历文档库

这个目录用于沉淀和维护我的实习、项目与论文经历，作为简历之外的长期资料库。

## 目录结构

- `experiences/`：实习与科研经历
- `projects/`：课程项目、研究项目与竞赛项目
- `publications/`：论文条目
- `publications/papers/`：论文解析、技术阅读笔记或从 PDF 提取的完整内容
- `cv/`：简历正文、条目池、条目审计和 TeX 检查工具
- `interview/`：通用面试介绍、公司定制材料和 coding 准备
- `TEMPLATE.md`：新增源条目的统一模板

## 推荐工作流

1. 先完善 `experiences/`、`projects/`、`publications/` 下的源条目
2. 再从源条目提炼 `cv/CV_ENTRY_BANK.md`
3. 然后创建或更新 `.tex` 简历，并运行页数检查
4. 最后维护 `interview/interview.md` 和 `interview/<company>/` 下的定制面试包

## `cv/` 目录说明

推荐在 `cv/` 中维护：

- `cv.tex` / `cv_cn.tex`
- `cv_1page.tex` / `cv_cn_1page.tex`
- `CV_ENTRY_BANK.md`
- `CV_ENTRY_AUDIT.md`
- `templates/README.md`
- `tools/detect_tex_dependencies.py`
- `tools/check_tex_pages.py`

## `interview/` 目录说明

- `interview/interview.md`：通用项目介绍和技术 topic bank
- `interview/coding/`：coding 题和实现草稿
- `interview/<company>/`：某公司或某岗位的定制材料目录

公司目录通常可以包含：

- `jd.md`
- `mock.md`
- `my-q.md`
- 其他 domain notes
