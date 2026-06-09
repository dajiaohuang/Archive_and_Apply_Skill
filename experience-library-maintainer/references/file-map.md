# Experience Library File Map

Use this reference when the repo appears to be an experience archive that feeds resume and interview outputs.

## Source-of-truth layers

### Source experiences

- `internships/`
- `projects/`
- `publications/`

These hold detailed factual material and should be updated first when experience content changes.

### Resume derivatives

- `cv/CV_ENTRY_BANK.md`
- `cv/RESUME_ENTRY_AUDIT.md`
- `cv/cv_cn.tex`
- `cv/cv_cn_1page.tex`
- `cv/cv.tex`
- optional draft files in `cv/`

### Interview derivatives

- `interview/interview.md` for general reusable speaking materials
- `interview/<company>/` for company-specific prep

Current known company-specific pattern:

- `interview/binance/crypto.md`
- `interview/binance/mock.md`
- `interview/binance/my-q.md`

## Maintenance conventions

- Keep Chinese as the default for repo-authored archival and interview notes unless the artifact is explicitly English or bilingual.
- Generic interview material belongs in `interview/interview.md`, not `cv/`.
- Company-specific prep belongs under `interview/<company>/`.
- If a README mentions files that no longer exist, verify against the filesystem before copying the reference forward.

## Typical update order

1. Source entry
2. `cv/CV_ENTRY_BANK.md`
3. Resume variants in `cv/`
4. `interview/interview.md`
5. company-specific interview files
6. `README.md` or `AGENTS.md` if needed

## Signals that derivative docs are stale

- references to deleted files
- stronger claims than the source entries support
- duplicated interview files in multiple folders
- old workflow notes that point to the wrong canonical file
