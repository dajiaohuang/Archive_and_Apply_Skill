# CV 条目审计

> 用途：按岗位方向审计“哪些条目该保留、哪些该弱化、Skills 板块该突出什么”。
> 状态：模板

## 1. 审计目标

- 不同岗位方向使用不同的条目组合
- 不同岗位方向使用不同的 Skills 板块重点
- 让 1 页版、2 页版和不同投递方向的 CV 有明确取舍逻辑

## 2. 评估维度

- `完整度`：背景、职责、技术、结果、复盘是否齐全
- `可直接上 CV`：是否已经能稳定压成强 bullet
- `岗位相关性`：对目标岗位方向的帮助
- `Skills 相关性`：是否值得进入 Skills 板块，还是只应体现在项目描述里
- `维护优先级`：
  - `P0`
  - `P1`
  - `Drop`

## 3. 条目总表

| 条目 | 来源文档 | 当前是否在 CV | 完整度 | 可直接上 CV | 岗位相关性 | Skills 相关性 | 维护优先级 | 结论 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| 示例条目A | `projects/example-project.md` | 是 | 5 | 4 | 5 | 4 | P0 | 必留 |
| 示例条目B | `experiences/example-experience.md` | 是 | 4 | 4 | 3 | 3 | P1 | 备选 |
| 示例条目C | `projects/example-legacy.md` | 否 | 2 | 2 | 1 | 1 | Drop | 放弃维护 |

## 4. 不同岗位方向推荐

### 4.1 Agent / LLM Engineering

- 推荐保留条目：
  - 示例条目A
  - 示例条目B
- 推荐弱化条目：
  - 示例条目C
- Skills 板块优先项：
  - Agent systems
  - RAG
  - tool calling
  - evaluation
  - APIs / systems / testing

### 4.2 Data Science / Applied AI

- 推荐保留条目：
  - 示例条目A
  - 示例条目B
- 推荐弱化条目：
  - 更偏 infra 但缺少量化结果的条目
- Skills 板块优先项：
  - experimentation
  - metrics
  - modeling
  - retrieval / ranking / classification
  - Python / SQL / data tooling

### 4.3 CV / Multimodal

- 推荐保留条目：
  - 数据集、benchmark、视觉、多模态相关条目
- 推荐弱化条目：
  - 与视觉无关的通用工程条目
- Skills 板块优先项：
  - computer vision
  - multimodal modeling
  - dataset construction
  - evaluation metrics

## 5. Skills 板块审计

### 应该进入 Skills 板块的内容

- 跨多个条目重复出现
- 对目标岗位是关键词级别的重要能力
- 能在面试中快速自证

### 不应该塞进 Skills 板块的内容

- 只在单个项目里偶然用过
- 很难自证
- 更适合放在项目描述里的细节模块

## 6. 审计结论输出格式

- 当前目标岗位方向：
- 必留条目：
- 备选条目：
- 建议删除或弱化条目：
- Skills 板块建议保留：
- Skills 板块建议删除或弱化：
- 1 页版建议：
- 2 页版建议：

## 7. 下一步

- [ ] 更新 `CV_ENTRY_BANK.md`
- [ ] 更新对应 `.tex` CV
- [ ] 更新 `interview/interview.md`
- [ ] 针对某公司 JD 再做一次定向审计
