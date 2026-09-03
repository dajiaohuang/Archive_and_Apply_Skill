# Evidence-Backed, Multi-Reader Resume Writing

Read this reference whenever drafting, rewriting, selecting, or auditing resume bullets. A resume is a compact decision aid and an interview agenda—not an autobiography, project README, or stack inventory.

## Start with the reader path

Do not assume one universal reader or hiring sequence. Infer the likely path from the employer, role, seniority, locale, and job description; state assumptions when the path is unknown.

| Reader or system | Decision they are trying to make | Evidence to surface | Common failure |
|---|---|---|---|
| ATS / application parser | Can the document be parsed and does it contain supported role signals? | standard titles/sections, exact defensible terminology, dates, skills in context | keyword stuffing, graphics/tables, synonyms that hide the required skill |
| Recruiter / HR / talent partner | Does this person plausibly meet the role, level, domain, and basic constraints? | recognizable problem, scope, ownership, relevant outcome, transferable signal | jargon before context, unclear seniority, responsibilities with no evidence |
| Hiring manager / team leader | Is this evidence of performance in the actual job, at the expected level? | end-to-end scope, prioritization, judgment, impact, reliability, stakeholder or user value | impressive technology with no reason, outcome, or ownership boundary |
| Technical interviewer / domain reviewer | Is the claimed depth real and worth probing? | architecture/method, constraints, tradeoffs, evaluation, failure handling, concrete tools when material | shallow tool lists, unexplained metrics, claims the candidate cannot defend |
| Potential teammate / peer | Will this person execute clearly and improve the team's work? | interfaces, debugging, testing, maintainability, documentation, handoff, collaboration and conflict resolution | “collaborated” with no personal contribution or team outcome |
| Cross-functional partner | Can this person translate needs and make useful tradeoffs across functions? | customer/problem framing, requirements, communication artifact, decision, measurable effect | internal implementation detail with no shared objective |
| Senior leader / hiring committee, when relevant | Does the candidate show leverage, trajectory, and appropriate risk judgment? | organizational scope, strategic choice, multiplier effect, durable outcome | inflated leadership language or activity counts without consequence |

These are lenses, not stereotypes. Recruiters can be technical; managers may inspect implementation; peers may care about user impact. Future teammates may not screen the initial application, but often participate later. Optimize first for the actual gate sequence, then ensure the document remains credible to all later readers.

## Use progressive disclosure inside each entry

Make the first meaningful clause understandable without specialized context. Add only enough technical specificity to distinguish the work and support a useful interview question. End with evidence of outcome, validation, or operating consequence.

Default bullet shape:

`ownership/action + recognizable problem or scope + discriminating method/decision + outcome or validation`

The order may change for readability. Do not force every element into one crowded bullet.

For a major entry, use bullets with distinct jobs:

1. **Orientation:** what was built, changed, or studied; for whom or why; and the candidate's ownership.
2. **Judgment/depth:** a consequential design choice, constraint, tradeoff, experiment, or failure mode.
3. **Evidence:** measured result, validated behavior, release/adoption, reliability, cost, learning, or external artifact.
4. **Team leverage, only when material:** clarified requirements, aligned stakeholders, improved review/testing/docs, unblocked others, or owned an interface/handoff.

The first bullet must survive a non-specialist scan. Later bullets may become more technical, but each still needs a clear purpose.

## Gather facts before writing

Capture these fields from source material or explicit user statements:

- target role, level, locale, and likely reader path
- problem, user, research question, or operating need
- candidate's personal ownership boundary versus team output
- scale and constraints: traffic, data, latency, cost, safety, deadline, regulation, ambiguity
- action and consequential decision—not every implementation step
- why that method was selected and what alternative/tradeoff mattered
- result, output, validation method, baseline, and time window
- team topology: collaborators, interfaces, dependencies, review/handoff, disagreement or coordination when material
- source path, evidence status, confidentiality boundary, and unresolved questions

If a key fact is unknown, ask for it or omit the claim. Do not turn an intended outcome into an achieved result.

## Choose signals by reader value

### Recruiter-readable signal

Answer in plain language: What kind of work was this, how large or important was it, what did the candidate own, and why is it relevant? Introduce uncommon product names and acronyms only after the problem is clear.

### Manager-readable signal

Show judgment and consequence: what priority or constraint shaped the work, what changed because of it, and what level of ownership is supported? For senior roles, show leverage through systems, standards, decisions, or people enabled—not just a longer technology list.

### Technical-interview signal

Include one or two details that distinguish depth: architecture boundary, model/data choice, evaluation design, bottleneck, reliability mechanism, security/safety constraint, or rejected alternative. A technical term earns space only when it helps explain the decision or matches a substantiated target requirement.

### Peer/team signal

Use team evidence only when concrete. Prefer:

- defined an API or ownership boundary that reduced integration ambiguity
- added tests, observability, runbooks, or review gates that changed team behavior
- translated requirements with product/design/research and documented the decision
- diagnosed a cross-service failure and coordinated the repair
- mentored/reviewed/unblocked others with a stated scope or outcome

Avoid unsupported personality labels such as “team player” or “excellent communicator.” Demonstrate the behavior and consequence.

## Evidence hierarchy

Prefer the strongest available evidence:

1. externally verifiable outcome: release, publication, award, patent, public artifact, accepted contribution
2. measured change against a named baseline: quality, latency, cost, scale, coverage, reliability, conversion
3. validated behavior: experiment, test suite, evaluation protocol, incident evidence, safety boundary, reproducible result
4. concrete operational or team outcome: adoption, decision enabled, handoff completed, process/review time changed
5. concrete deliverable: system, model, dataset, analysis, interface, process
6. responsibility only: use only when stronger evidence does not exist

Do not invent numbers. A precise qualitative result is stronger than a fabricated metric. Distinguish team result from individual contribution: “contributed X to a team that achieved Y” when that is the supported scope.

## Do not lead with activity volume

Do not treat raw activity counts—such as numbers of pull requests, commits, tickets, tests, files, meetings, or repositories touched—as the headline result. Preserve them in the evidence layer when they help with auditability, but lead resume bullets with the problem solved, the candidate's substantive contribution or judgment, and the change that was accepted, released, adopted, or validated.

For open-source work, prefer a small number of representative accepted changes and their technical or user consequence over submission volume. Keep open, draft, closed-unmerged, and merged contributions distinct; never present work awaiting review as upstream adoption. A count earns resume space only when it proves meaningful scale, selectivity, adoption, reliability, or organizational scope and the surrounding clause explains that meaning. When a large count competes with a more specific outcome, keep the outcome.

## Introduce notable upstream projects before personal contribution

When a notable external open-source project merits its own resume entry, default to two bullets with separate jobs:

1. **Project orientation and influence:** explain what the project does, the problem or user group it serves, and why it matters in its ecosystem. Use one or two current, publicly verifiable influence signals—such as GitHub Stars/Forks, downstream adoption, releases, or recognized ecosystem role—only when they materially help the reader calibrate the project. Date-stamp volatile repository metrics and recheck them before each resume release.
2. **Candidate's accepted contribution:** identify the candidate as an external contributor when applicable, then summarize a small number of representative merged changes, the technical problem each addressed, and the reliability, compatibility, security, or user consequence. Keep PR links and detailed status counts in the evidence layer.

Never transfer the project's popularity to the candidate: Stars, Forks, users, and ecosystem reach describe the upstream project, not the individual's impact. Do not imply maintainership, adoption, or ownership without evidence. Exclude open, draft, or closed-unmerged PRs from the accepted-contribution bullet unless their status is explicitly stated and there is a separate reason to include them. If popularity metrics are weak or misleading, orient the reader with the project's function and use stronger evidence such as releases, downstream integration, or maintainer-accepted design changes instead.

## Quantify with meaning

Use a number only when the source supports it and the reader can tell what it proves. Prefer:

- change plus baseline: `reduced median latency from A to B under C workload`
- scale plus behavior: `processed N records/day while meeting SLO X`
- evaluation design: `evaluated N models on M examples using metric X`
- selection rate: `selected as 1 of N` when externally supported and relevant
- team/organizational scope when it explains leadership or coordination

Name the denominator, baseline, time window, or condition when needed. Dataset size, test count, team size, or lines of code are not impact by themselves.

## Preserve interview integrity

Treat every bullet as a promise that the candidate can explain:

- What exactly did you own?
- Why did the problem matter?
- Why this approach rather than an alternative?
- What constraint or tradeoff drove the decision?
- How was the outcome measured and against what baseline?
- What failed, changed, or remained unresolved?
- Who else contributed, and how did your work interface with theirs?
- What would you do differently now?

Remove or weaken a claim if the candidate cannot answer likely follow-ups accurately. Do not disclose confidential architecture, customer data, unreleased metrics, security details, or employer-sensitive information merely to sound specific; describe the class of problem or relative effect instead.

## Bilingual and Chinese wording

When the workspace keeps Chinese and English resumes, also read `references/resume-wording-constraints.md` and, for a full rewrite, `references/resume-section-lock.md`.

Do not start every bullet with “独立设计”. Do not nest a second colon after a bold label. Do not hitch a second action with “并以…”. Keep protocol dates, schema versions, unpublished scores, and stacked inventory counts in the fact layer. Preserve an iterative route instead of presenting only the latest architecture. Use official publication titles; if the author list is omitted, write the authorship role.

## Writing rules

- Start with a specific ownership/action verb; avoid “responsible for,” “helped,” or “worked on” unless limited scope is the truth.
- Put the problem, user, or consequence before obscure internal names.
- Keep one main claim per bullet and one distinct purpose per bullet set.
- Prefer concrete nouns and verbs over adjectives such as “novel,” “robust,” “high-performance,” or “significant.”
- Preserve tense, dates, seniority, authorship, and contribution level.
- Expand an uncommon acronym once or remove it.
- Use JD vocabulary only when the source substantiates it; do not copy entire requirement phrases.
- Show interpersonal skills through decisions and outcomes, not a generic soft-skills list.
- Avoid repeating the same evidence in summary, skills, and multiple bullets unless each placement serves a different decision.
- Prefer readable space and hierarchy over aggressive compression.

## Drafting and compression loop

1. Write an evidence-complete version without optimizing line count.
2. Label each clause by function: orientation, ownership, decision/method, outcome, or team leverage.
3. Remove clauses that serve no likely reader or duplicate a stronger bullet.
4. Move the most relevant and differentiating signal earlier.
5. Replace jargon with accessible language; retain only discriminating technical terms.
6. Verify every claim and metric against its source and contribution boundary.
7. Read the entry through each relevant reader lens.
8. Render the resume and revise for actual line breaks; do not sacrifice truth or readability merely to save one line.

## Multi-reader audit

For each major entry, answer:

### Recruiter / HR

- Can a non-specialist name the problem, scope, ownership, and relevance after the first bullet?
- Are level and transferable skills visible without decoding internal terminology?

### Hiring manager / team leader

- Does the entry predict performance in the target job rather than merely list past activity?
- Is there evidence of judgment, prioritization, end-to-end ownership, and consequence at the claimed level?

### Technical reviewer

- Is there at least one concrete technical decision, constraint, or validation method worth probing?
- Are tools connected to an architectural or methodological purpose?

### Potential peer / cross-functional partner

- Is the individual contribution distinguishable from the team's result?
- Where relevant, does the entry show interface ownership, quality practices, communication, or team leverage?

### ATS / document system

- Are required supported terms present in ordinary text and in their expected context?
- Does extracted text preserve headings, dates, bullets, and reading order?

### Evidence and interview

- Is every material claim sourced, correctly scoped, confidentially safe, and defensible under follow-up?
- Does each bullet add a signal that is not already conveyed better elsewhere?

## Research basis

- Microsoft states that applications may move from Recruiting to the hiring team, including hiring managers, screeners, and interviewers; interviews may include potential teammates and cross-functional colleagues: <https://careers.microsoft.com/v2/global/en/hiringfaqs.html> and <https://careers.microsoft.com/v2/global/en/hiring-tips>
- Microsoft asks candidates to connect past examples and transferable skills to the target role, and expects honest representation throughout the process: <https://careers.microsoft.com/v2/global/en/hiring-tips>
- MIT advises writing for recruiters, hiring managers, or committees; making technical work understandable to broader audiences; targeting the job; and using project/action/result evidence: <https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/> and <https://capd.mit.edu/resources/resumes/>
- Yale recommends accomplishment statements that distinguish individual action, project/problem, result, tangible evidence, and team contribution: <https://ocs.yale.edu/resources/writing-impactful-resume-bullets/>
- Harvard recommends specific, active, fact-based language written for people and systems that scan quickly: <https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/>
- Amazon describes interview loops in which different employees assess different aspects of skills and experience; technical hiring considers both technical and behavioral competencies: <https://amazon.jobs/content/en/how-we-hire/interview-loop> and <https://amazon.jobs/content/en/how-we-hire/university/additional-tech>
