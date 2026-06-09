# CV Entry Bank

> Purpose: maintain reusable CV bullets for different role directions in one place instead of re-extracting them from long source entries every time.
> Status: template

## 1. Maintenance Rules

- Try to keep two versions for each entry:
  - `short`: for a 1-page CV, usually 1 sentence or 1-2 bullets
  - `long`: for a 2-page CV, usually 1 paragraph or 2-3 bullets
- Keep at least one verifiable fact per entry:
  - metric
  - named interface / module / method
  - engineering constraint / risk boundary / test result
- Suggested priorities:
  - `P0`: mainline entries
  - `P1`: backup entries
  - `Drop`: historical only, no longer worth polishing
- Update this file before syncing `.tex` CV files.

## 2. Mainline Summary

### P0

- `entry_id_a`
- `entry_id_b`

### P1

- `entry_id_c`

### Drop

- `entry_id_d`

## 3. Source Mapping

| Entry ID | Primary Source | Priority | Notes |
|---|---|---|---|
| entry_id_a | `projects/example-project.md` | P0 | mainline project |
| entry_id_b | `experiences/example-experience.md` | P0 | mainline experience |
| entry_id_c | `publications/example-paper.md` | P1 | optional publication |
| entry_id_d | `projects/example-legacy.md` | Drop | historical only |

## 4. Entry Pool

### 4.1 Example Entry (`entry_id_a`)

- Short:
  Use one sentence to state the problem, your contribution, and one hard result.

- Long:
  Use one paragraph or 2-3 bullets to explain the system goal, approach, scope, and outcome.

- Verifiable Facts:
  - example interface or module
  - example metric
  - example test or constraint

## 5. Recommended by Role Direction

### Agent / LLM Engineering

- Must keep:
  - `entry_id_a`
  - `entry_id_b`

### Data Science / Applied AI

- Must keep:
  - `entry_id_b`
  - `entry_id_c`

### CV / Multimodal

- Must keep:
  - `entry_id_c`

## 6. Sync Checklist

- [ ] source entry updated
- [ ] this file refreshed
- [ ] role-specific keep / weaken decisions revisited
- [ ] `.tex` CV synced
