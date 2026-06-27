# Guided User Flow

Use this reference when you want the skill to feel like a guided product flow instead of a one-shot editor.

## Principle

After every meaningful milestone, do two things:

1. briefly state what was completed
2. offer 2 to 4 concrete next-step options

These next-step options are not single-choice by default. Present them as actions the user may choose one or more of, especially when multiple follow-ups can sensibly happen in parallel.

Do not end a milestone with only a status summary when there is an obvious next move.

## Step 0: Skill Installed or First Invocation

When the user has just installed or first invoked the skill, the default next-step prompt should point to workspace creation.

Default language behavior for first workspace bootstrap:

- if the user's install prompt or first invocation prompt is in Chinese, default the new workspace to Chinese
- otherwise, default the new workspace to English
- if the user explicitly requests another language, follow that request
- if the target repo already exists, follow the repo's current language instead of the prompt default

Recommended options:

- create a new archive-and-apply workspace at a chosen path
- point the agent at an existing workspace to inspect its structure
- give a directory, repo, or notes folder to ingest into a workspace

## Step 1: Workspace Created

Immediately after creating a new workspace:

- report the canonical workspace path
- if the agent surface supports memory, store that path as the default archive-and-apply location
- if the agent surface has explicit memory or profile features, prefer persisting the path there
- if persistent memory is unavailable, write the path into the repo README or remind the user to reuse the same path in future requests

Recommended options after bootstrap:

- create entries from a local directory, repo, PDF folder, notes dump, or copied text
- add the first experience manually from raw facts
- inspect TeX availability before the first resume workflow

Special note for OpenClaw / Hermes style surfaces:

- treat the first successful bootstrap as a memory-worthy event
- remember the canonical workspace path so later tasks can say "use my archive-and-apply workspace" without restating the location

## Step 2: First Entries Created

After one or more source entries have been created, the user usually wants one of three things:

- create more entries
- turn existing entries into CV content
- turn existing entries into interview material

Recommended options:

- ingest more materials into additional entries
- create `cv/CV_ENTRY_BANK.md` with bullet-style resume content
- create or update `interview/interview.md`

## Step 3: CV Content Bank Created

After creating a CV content bank:

- tell the user it can now be used to draft `.tex` resumes
- if this is the first CV workflow in the workspace, detect TeX tooling first

Recommended options:

- detect TeX dependencies and local compile tools
- create an English resume from the template
- create a Chinese resume from the template
- create a one-page or two-page variant

## Step 4: First Resume Draft Created

After drafting the first TeX resume:

- check whether TeX tooling is available if that has not already been done
- compile the resume
- report actual page count
- report whether the page is sparse, acceptable, or well-filled

Recommended options:

- tighten content to fit one page
- expand content to better fill a sparse page
- generate another language or another page-count variant
- update the CV entry bank before redrafting

## Step 5: Interview Base File Created

After creating `interview/interview.md`:

- remind the user that this is the reusable base file
- suggest either expanding generic project intros or creating a company-specific pack

Recommended options:

- expand project intros and technical topic notes
- create `interview/<company>/` for a target role
- generate bilingual spoken introductions from the current entries

## Step 6: Company-Specific Directory Created

When `interview/<company>/` is created:

- save the JD first, usually as `jd.md`
- explicitly tell the user that the next natural step is mock generation

Recommended options:

- paste or save the JD into `jd.md`
- generate `mock.md` from the JD plus current source entries
- generate `my-q.md` with closing questions

## Step 7: Source Entry Updated Later

When an existing source entry is changed, do not stop at "updated".

If `cv/CV_ENTRY_BANK.md` already exists, treat "Should I update the CV content bank too?" as the default first follow-up.

Recommended options:

- sync the CV entry bank
- refresh the relevant TeX resume
- refresh `interview/interview.md`
- refresh a company-specific mock pack that depended on this entry
