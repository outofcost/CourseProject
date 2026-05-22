# Coursework — final .docx output

## Build

```bash
bash analysis_v2/build_docx.sh
```

Produces `coursework/coursework_draft.docx` from the latest chapter sources in `analysis_v2/reports/`.

Pipeline:

1. `analysis_v2/build_manuscript.sh` concatenates 8 source files (abstract + chapter 1–6 + ai_disclosure + appendices stub) into `analysis_v2/reports/manuscript_master.md`.
2. Pandoc converts `manuscript_master.md` → `coursework/coursework_draft.docx` with `--from=markdown+tex_math_dollars+raw_tex --to=docx -V lang=ru`.

Sources of truth — chapter markdown files. .docx is reproducible output and is git-ignored.

## Status

Phase H draft conversion verified 2026-05-22 — produces a valid 72K .docx with all chapters, abstract, and AI Disclosure. Math expressions render as OMML; Word and LibreOffice both display them correctly.

Pending polish in subsequent phases:
- HSE template (Times New Roman 14pt, 1.5 spacing, A4, 2cm margins) — TASK-A-24.
- Title page (TASK-K-34, deferred per Karolina's request).
- Figure embedding from `analysis_v2/output/figures/` (TASK-K-35..36).
- Tables embedded inline (TASK-K-37..38).
- Final bibliography render — TASK-A-21.
