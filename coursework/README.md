# Coursework — final .docx output

## Build

```bash
bash analysis_v2/build_docx.sh
```

Produces `coursework/coursework_draft.docx` (~1.1 MB) from the latest
chapter sources in `analysis_v2/reports/`.

## Pipeline

1. `analysis_v2/build_manuscript.sh` concatenates source files in HSE
   Article (Empirical) order:

   1. `title_page.md` (placeholder fields to be filled by author)
   2. `abstract.md` (RU + EN)
   3. `chapter_1_introduction.md` через `chapter_6_conclusion_v2.md`
   4. `ai_disclosure.md`
   5. `references_apa.md` (32 APA-7 entries)
   6. Списки рисунков + таблиц (static)
   7. Приложения A–D pointers

   Output: `analysis_v2/reports/manuscript_master.md` (~20 800 words).

2. Pandoc converts master → docx with:
   - `--from=markdown+tex_math_dollars+raw_tex --to=docx`
   - `--toc --toc-depth=3 -V toc-title="Содержание"`
   - `--reference-doc=coursework/hse_template.docx` (HSE template)
   - `-V lang=ru`

## HSE template specs (`hse_template.docx`)

Generated via `python3 coursework/build_template.py`. Per HSE SPB SoEM
guideline §6.1:

- Times New Roman 12pt body, межстрочный интервал 1.5
- A4 page, поля: left 35mm, right 10mm, top/bottom 20mm
- Heading 1/2/3 — TNR 12pt bold, centered
- Footnotes — TNR 10pt single-spaced
- Page numbers in footer (center)
- First-line indent 1.25cm, justified main text

## Sources of truth

Chapter markdown files в `analysis_v2/reports/`. The .docx is a
reproducible artifact and is git-ignored (см. `coursework/.gitignore`).

## Status (2026-05-23)

После 18+ итераций dual-agent hostile review (Claude-K + Claude-A):

- ✅ Manuscript: 6 глав + abstract RU/EN + AI Disclosure + refs + lists + appendices = 20.8k слов
- ✅ Math expressions render as OMML (Word + LibreOffice compatible)
- ✅ 7 figures (F1-F7) embedded with Russian captions
- ✅ 14 tables (Т4.1-Т4.14) с подписями «Источник: расчёты автора»
- ✅ 10 formulas pronumerated (1)-(10)
- ✅ Bibliography 32 entries APA-7 alphabetical
- ✅ HSE template applied (TNR 12pt, поля 35-10-20-20, TOC «Содержание»)

## Outstanding для Karolina-human

См. `coursework/SUBMISSION_CHECKLIST.md` (10-step pre-submission
checklist) и `coursework/FINAL_STATUS.md` (comprehensive state
summary). Главное:

- Заполнить плейсхолдеры в `coursework/title_page.md`
- Прогнать pre-submit checklist (visual check в Word)
- Опционально: AI-detector check через gptzero.me

## Files

- `coursework_draft.docx` — output (git-ignored)
- `title_page.md` — title page draft с плейсхолдерами
- `hse_template.docx` — HSE-compliant template
- `build_template.py` — генератор HSE template
- `SUBMISSION_CHECKLIST.md` — pre-submission checklist
- `FINAL_STATUS.md` — comprehensive status snapshot
- `Примеры вкр папка/` — 5 примеров ВКР (gitignored, study material)
