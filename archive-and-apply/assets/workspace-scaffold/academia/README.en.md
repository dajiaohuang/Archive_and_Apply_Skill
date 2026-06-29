# Academic Applications Workspace

This directory manages the complete materials system for graduate and professional school applications, supporting PhD, research master's, professional master's, and fellowship applications.

## Directory Structure

- `SOP.cn.md` / `SOP.en.md`: Statement of Purpose draft
- `RESEARCH_STATEMENT.cn.md` / `RESEARCH_STATEMENT.en.md`: Research Statement (PhD / research master's)
- `PERSONAL_STATEMENT.cn.md` / `PERSONAL_STATEMENT.en.md`: Personal narrative (required by some programs)
- `PUBLICATION_SUMMARY.cn.md` / `PUBLICATION_SUMMARY.en.md`: Publication abstract bank
- `REC_TRACKER.cn.md` / `REC_TRACKER.en.md`: Recommendation letter tracker
- `writing-samples/`: writing sample storage
- `<school-name>/`: per-school customized materials (subdirectory by school name)

## Recommended Workflow

1. First, flesh out source entries under `experiences/`, `projects/`, `publications/`
2. Generate `PUBLICATION_SUMMARY.md` from source entries
3. Choose the right narrative template based on application type (PhD / research / professional)
4. Generate SOP draft from source entries
5. If applying for PhD, generate Research Statement
6. Build recommender relationships, fill in `REC_TRACKER.md`
7. Customize per school: copy the general version to `<school>/`, swap school / professor / lab names

## Per-School Directories

Each school typically contains:

```
<school-name>/
  sop.md           ← customized SOP
  research_statement.md  ← if needed
  notes.md         ← school selection reasoning, professor research notes
  deadline.md      ← deadline tracking
```

## Notes

- SOP / Research Statement / Personal Statement must be differentiated — do not write them as the same file
- All claims must be traceable to source entries; do not write about uncertain things
- Reach out to recommenders 1-2 months in advance — do not wait until right before deadline
- SOP customization: school name, professor name, course name, research group name must all be changed
