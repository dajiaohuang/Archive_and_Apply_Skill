# Resume Bullet Writing

Use this reference when drafting or auditing resume bullets, especially for technical roles where both recruiters and domain engineers will read the same page.

## Reader Contract

Write every entry for two readers:

- A recruiter should understand what was built, who it served, and why it mattered without knowing internal class names.
- A domain engineer should still find a concrete problem, technical decision, boundary, or measurable result worth discussing.

Each bullet must stand on its own. Do not require the reader to decode a previous bullet or an internal architecture diagram.

## Default Entry Structure

For a major experience or project with two or three bullets:

1. **Overview** — state ownership, the system or research output, its user/problem, and the main capability delivered.
2. **Technical highlight** — name a concrete failure mode or constraint, then explain the design used to solve it and the behavior it produced.
3. **Technical highlight or result** — cover a second hard problem, engineering boundary, evaluation, scale, or outcome.

For a compact project with only one bullet, use:

`what was built -> key approach -> result`

Do not turn the overview into an architecture inventory. Detailed frameworks, internal services, and metrics belong in later bullets unless they are essential to understanding the project.

## Writing Rules

- Start with an ownership verb such as built, designed, implemented, led, trained, evaluated, or shipped.
- Keep one main idea per bullet.
- State the user-visible or engineering problem before specialized implementation names.
- Use internal component names as evidence, not as the subject of the sentence.
- Prefer plain-language outcomes such as “prevented cross-branch memory leakage” over unexplained abstractions such as “implemented revision ancestry filtering.”
- Attach metrics to the behavior they validate; do not append test counts or model names only to make a bullet look quantitative.
- Keep claims traceable to source entries. Preserve contribution boundaries such as independently built, led, contributed, or supported.
- Expand uncommon abbreviations on first use or remove them when they do not help the target role.
- Remove tool and framework laundry lists. Keep only technologies that explain the design choice or establish role relevance.
- For a one-page CV, prefer one or two readable lines per bullet. Shorten wording before shrinking typography.

## AI / LLM / Agent Emphasis

For AI Agent roles, make the system overview legible before naming orchestration internals. Strong technical highlights usually explain one of these problems:

- tool discovery, selection, exposure, or authorization
- retrieval quality, versioning, evidence, or hallucination control
- long-term memory, identity, branch, or audience isolation
- workflow orchestration, retries, idempotency, or state ownership
- evaluation, observability, latency, cost, or launch safety

Describe the failure that was prevented. “Rejected unauthorized calls at the MCP boundary” is clearer than listing permission-service classes. “Prevented other characters' or GM-only knowledge from entering the response” is clearer than listing knowledge-model fields.

## Readability Check

Before accepting a bullet, verify:

1. Can a recruiter explain the project after reading only the first bullet?
2. Can an engineer identify the hard technical problem in each later bullet?
3. Does every acronym or internal name earn its space?
4. Is the outcome tied to the solution rather than appended as an unrelated metric?
5. Can every claim be traced back to a source entry?
