# Academic Applications / 学术申请工作区

这个目录用于管理硕博申请的完整材料体系，支持 PhD、研究型硕士、职业型硕士和各类奖学金申请。

## 目录结构

- `SOP.cn.md` / `SOP.en.md`：Statement of Purpose 初稿
- `RESEARCH_STATEMENT.cn.md` / `RESEARCH_STATEMENT.en.md`：研究陈述（PhD / 研究型硕士）
- `PERSONAL_STATEMENT.cn.md` / `PERSONAL_STATEMENT.en.md`：个人成长叙事（部分项目要求）
- `PUBLICATION_SUMMARY.cn.md` / `PUBLICATION_SUMMARY.en.md`：论文摘要库
- `REC_TRACKER.cn.md` / `REC_TRACKER.en.md`：推荐信追踪表
- `writing-samples/`：写作样本存放
- `<school-name>/`：各学校定制材料目录（按学校名建子目录）

## 推荐工作流

1. 先完善 `experiences/`、`projects/`、`publications/` 下的 source entries
2. 从 source entries 生成 `PUBLICATION_SUMMARY.md`
3. 根据申请方向（PhD / 研究型 / 职业型），选择合适的叙事模板
4. 生成 SOP 初稿（基于 source entries）
5. 如申请 PhD，生成 Research Statement
6. 建立推荐信关系，填写 `REC_TRACKER.md`
7. 按学校定制：复制通用版到 `<school>/`，替换学校 / 教授 / 实验室名

## 各学校定制目录

每个学校通常包含：

```
<school-name>/
  sop.md           ← 定制版 SOP
  research_statement.md  ← 如需要
  notes.md         ← 选校理由、教授研究笔记
  deadline.md      ← Deadline 追踪
```

## 注意事项

- SOP / Research Statement / Personal Statement 三者内容要有区分，不要写成同一份文件
- 所有 claims 必须可回溯到 source entries，不确定的不要写
- 推荐信提前 1-2 个月联系，不要等到 deadline 前才找人
- SOP 定制：学校名、教授名、课程名、研究组名都要改
