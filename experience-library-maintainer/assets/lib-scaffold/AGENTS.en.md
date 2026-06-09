# AGENTS.md

This file provides guidance to coding agents when working in this repository.

## Purpose

This is a personal experience documentation library: a source-first archive of experiences, projects, publications, CV artifacts, and interview materials.

## Core Rules

- Treat `experiences/`, `projects/`, and `publications/` as the factual source of truth.
- Create new source entries from `TEMPLATE.md` first, then derive CV and interview artifacts.
- Prefer updating canonical files instead of creating duplicates.
- Use `interview/interview.md` for reusable speaking material.
- Use `interview/<company>/` for company- or role-specific prep.
- When a JD is provided for a company-specific prep pack, save it into that company directory first, typically as `jd.md`.

## Expected Directory Shape

- `experiences/`
- `projects/`
- `publications/`
- `publications/papers/`
- `cv/`
- `interview/`
- `TEMPLATE.md`
- `README.md`

## Resume Workflow

1. Update or create source entries
2. Sync `cv/CV_ENTRY_BANK.md`
3. Update `.tex` resume variants
4. Run local TeX dependency and page checks

## Interview Workflow

1. Keep reusable material in `interview/interview.md`
2. Create `interview/<company>/` for targeted prep
3. Store the JD in that folder
4. After the JD is saved, the next natural step is to generate `mock.md`
