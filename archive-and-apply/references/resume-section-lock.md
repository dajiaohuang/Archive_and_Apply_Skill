# Section-Lock Resume Workflow

Read this reference when rewriting a bilingual resume section by section, or when the user wants to lock wording before TeX compilation.

This workflow is for **content lock**. After the full document is locked, switch to `resume-layout-qa.md`. Do not interleave compile-and-tweak with unfinished wording.

## Canonical discussion order

1. Treat the Chinese two-page file (`cv/cv_cn.tex`) as the discussion source when a Chinese two-page resume exists.
2. For each section, show the current locked-candidate wording, map it to the fact layer, and flag only the claims that are unverified, over-scoped, or stylistically blocked.
3. Wait for an explicit lock. “不用改了”, “下一节”, “先不变了”, or a specific wording patch all count as a lock for the section under discussion.
4. After a section is locked, sync the same meaning to:
   - `cv/cv.tex`
   - `cv/cv_cn_1page.tex`
   - `cv/cv_1page.tex`
   - `cv/CV_ENTRY_BANK.md`
5. One-page and English files may be shorter or omit an item. They must not contradict the locked two-page Chinese claim, invent a stronger result, or reuse a sentence that another section already owns.
6. Do not compile, render, or chase page fill until every section scheduled for this pass is locked.

## Section pass

Use the document's own section order. A typical industry resume pass is:

1. Education
2. Experience, one employer at a time
3. Projects, one project or combo block at a time
4. Publications
5. Skills

Inside a combo block (open-source contributions, Agent Skills, multiple papers), lock items in the displayed order. Do not reopen a locked item unless the user asks.

When presenting a section:

- Quote the current Chinese two-page bullets, not a fresh paraphrase.
- Say what the fact layer supports, what must stay out of the resume, and what is still unmarked.
- Ask only the decisions that block the next lock. Do not offer a rewrite menu for a section the user already accepted.

## After the full lock

1. Compile every target TeX with the skill-repo checker and write the PDF beside the source:

   ```bash
   python scripts/check_tex_pages.py path/to/cv_cn.tex --target-pages 2 --output path/to/cv_cn.pdf --render-dir path/to/rendered/cv_cn --json
   ```

2. Prefer this skill script over a stale workspace copy of `cv/tools/check_tex_pages.py`. Older local copies may fail on Windows when `pathlib.Path` is passed into `subprocess`.
3. Adjust layout only after the wording lock. First reduce empty vertical space and the skills block. Follow `resume-layout-qa.md` for the rest of the correction order.
4. Recompile and visually inspect every page after each coherent layout pass.

## Fact-layer pairing

- If a resume change needs a new fact, write the fact first and mark its status (verified, user-reported, design spec, unmarked).
- If the user only changes wording or variant selection, do not rewrite the source to match the resume.
- When a system has replaced an earlier design, keep the old line in the source as history. The resume may summarize the route; it must not pretend the current design was there from the start.
