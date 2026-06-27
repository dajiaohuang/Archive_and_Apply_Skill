# CV 条目池

> 用途：集中维护不同岗位方向可复用的 CV bullet，避免每次都从长文 source entry 重新提炼。
> 状态：模板

## 1. 维护规则

- 每条经历尽量维护两版：
  - `短版`：适合 1 页 CV，1 句或 1-2 条 bullet
  - `长版`：适合 2 页 CV，1 段或 2-3 条 bullet
- 每条至少保留 1 个可核验事实：
  - 指标
  - 明确接口 / 模块 / 方法名
  - 工程约束 / 风险边界 / 测试结果
- 条目优先级建议分为：
  - `P0`：主线条目
  - `P1`：备选条目
  - `Drop`：历史保留，不再投入维护
- 先更新这里，再同步 `.tex` CV。

## 2. 当前主线结论

### P0

- `entry_id_a`
- `entry_id_b`

### P1

- `entry_id_c`

### Drop

- `entry_id_d`

## 3. 来源映射

| 条目ID | 主来源文档 | 优先级 | 备注 |
|---|---|---|---|
| entry_id_a | `projects/example-project.md` | P0 | 主线项目 |
| entry_id_b | `experiences/example-experience.md` | P0 | 主线经历 |
| entry_id_c | `publications/example-paper.md` | P1 | 备选成果 |
| entry_id_d | `projects/example-legacy.md` | Drop | 历史保留 |

## 4. 条目池

### 4.1 示例条目（entry_id_a）

- 短版：
  用 1 句写清问题、你的贡献和 1 个硬结果。

- 长版：
  用 1 段或 2-3 条 bullet 写清系统目标、技术方案、职责边界和结果。

- 可核验事实：
  - 示例接口或模块
  - 示例指标
  - 示例测试或约束

### 4.2 示例条目（entry_id_b）

- 短版：
  用更偏研究、工程或业务导向的一句简述。

- 长版：
  展开背景、方法、结果与价值。

- 可核验事实：
  - 示例 benchmark / 数据规模 / 用户规模

## 5. 按岗位方向推荐

### Agent / LLM Engineering

- 必留：
  - `entry_id_a`
  - `entry_id_b`
- 优先强调：
  - tool calling
  - RAG
  - evaluation
  - system boundaries

### Data Science / Applied AI

- 必留：
  - `entry_id_b`
  - `entry_id_c`
- 优先强调：
  - metrics
  - experiment design
  - data pipeline
  - model validation

### CV / Multimodal

- 必留：
  - `entry_id_c`
- 优先强调：
  - datasets
  - benchmarks
  - vision or multimodal modeling

## 6. 同步清单

- [ ] source entry 是否已更新
- [ ] 本文件是否已同步
- [ ] 不同岗位方向的保留 / 弱化是否已重审
- [ ] `.tex` CV 是否已同步
