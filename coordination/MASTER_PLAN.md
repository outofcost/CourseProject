# MASTER PLAN — путь к финальной курсовой

> Полный план движения от текущего draft-состояния к finalized .docx, соответствующему HSE Article Empirical format. Восемь фаз A–H. Каждая фаза имеет concrete deliverable, tasks разделены по lanes (Claude-K / Claude-A). Этот файл — source of truth для следующих 5–10 итераций async-coordination.
>
> **Версия:** v1, 2026-05-22. **Соавторы плана:** Claude-K (initial draft), Claude-A (review pending — см. §Endorsement).

---

## Цель работы

Создать **финальную .docx-курсовую** уровня 3 курса HSE «Quantitative Economics», соответствующую полностью HSE term paper guideline для Article (Empirical) format:

- **Объём:** 55–70 страниц финального документа (Times New Roman 14pt, 1.5 spacing, A4)
- **Структура:** Title page → Abstract (RU + EN) → Chapters 1–6 → AI Disclosure → Bibliography → Appendices
- **Содержание:** ≈ 13 600 слов draft v1 → polished + integrated final
- **Источники:** ~25–30 финальных references в APA-формате
- **Figures:** 7 PDF/PNG (F1–F7) embedded с captions и cross-references
- **Tables:** ~20 regression tables в Appendix; key tables (Shapley, M_full, tier-specific) inline
- **Reproducibility:** ссылка на public GitHub repo + AI disclosure

**Realistic constraint:** "10/10 идеально" — это aspiration. AI-инструменты могут построить **maximally-polished draft**; финальная адjudication качества — за научным руководителем + автором. Наш target — minimize обоснованных правок при review.

---

## Фаза A — Content completion (закрыть TBD-маркеры)

**Goal:** все [TBD: см. {source}] маркеры в chapter_*.md заменены на verified cite'ы либо явно помечены как paywall с paraphrase.

**Текущий статус:** ~12 TBD-маркеров после commits 2baa0eb + f5bfeee + 1bfe314 + d92719c.

**Claude-K tasks:**
- TASK-K-10: Integrate Kopkin (2012) — direct NBA tax migration paper — в chapter_2 §2.6 (Stream 5) + chapter_5 §5.5 (H9 reframe extension)
- TASK-K-11: Integrate Keefer (2021) — sunk-cost + cap-shock methodology — в chapter_3 §3.8 (методологический antecedent) + chapter_5 §5.7 (Limitations)
- TASK-K-12: Integrate Berri & Krautmann (2006) — NBA shirking — в chapter_5 §5.7 (Limitations: contract-year endogeneity)
- TASK-K-13: Integrate White & Sheldon (2014) — CY effect — в chapter_5 §5.7 (Limitations)
- TASK-K-14: Resolve skeleton TBD-маркеры (Mincer, Stiroh, Hill-Groothuis, Krautmann, Kahn) — заменить на verified general cite'ы (Author, Year) без verbatim quotes; если verbatim нужны — добавить paywall caveat
- TASK-K-15: Verified cite Pratt (1987) + Genizi (1993) в Methods §3.6 (alternatives Shapley)
- TASK-K-16: Verified cite Shapley (1953) в Methods §3.6 (foundational theorem)
- TASK-K-17: Verified cite Rosen (1986) в Methods §3.4 + Discussion §5.2 (cap concavity)

**Claude-A tasks:**
- TASK-A-10: Update references.bib bibkey `johnson_2017` → `johnson_2018` (per bib-check finding)
- TASK-A-11: Remove `hinton_2019` и `robst_2011` из references.bib (dropped per K commit 2baa0eb)
- TASK-A-12: Add `berri_schmidt_2010` как `@book{...}` entry (Stumbling on Wins, FT Press 2010)
- TASK-A-13: HSE library proxy attempt для top-priority paywall sources (Lipovetsky-Conklin 2001, Mincer 1974, Hill-Groothuis 2001, Stiroh 2007, Johnson-Hall 2018) — upgrade skeleton templates до FULL где получится
- TASK-A-14: Verify each Crossref DOI в references.bib (после fix'ов K-10..K-17)

**Phase A deliverable:** все chapter_*.md без [TBD] маркеров (либо явно paywall с caveat).

---

## Фаза B — Cross-chapter consistency

**Goal:** terminology, hypothesis numbering, cross-references, цифры — consistent через все 6 глав.

**Specific checks:**
- H1-H10 одинаково именованы и mapped to streams в Introduction, LitRev, Results, Discussion, Conclusion, hypotheses_v2_final.md
- All numerical claims (R² = 0.649, 36.8% Performance share, β = -0.098 etc.) идентичны в Results, Discussion, Conclusion, Abstract
- Figure references (F1, F2, ...) consistent across chapters
- Table numbering consistent
- Terminology: tier names (mid_level / mid-level), market terminology (top5_market / top-5 market), CBA dates (2017 vs 2017/18 vs 2018) unified
- Russian academic style: «выявить, что» vs «обнаружить, что», «представляет собой» vs «является», etc. — выбрать registry и stick

**Claude-K tasks:**
- TASK-K-18: Hypothesis numbering audit (grep H1-H10 across all files, manually verify)
- TASK-K-19: Numerical consistency check (key headline numbers — Shapley shares, R²-values, β-coefficients)
- TASK-K-20: Terminology unification pass
- TASK-K-21: Cross-reference verification (Глава X.Y, Раздел §, Рисунок Fx, Таблица Tx — all working)

**Claude-A tasks:**
- TASK-A-15: Re-run bib_check_report.md после K-10..K-17 — should pass clean
- TASK-A-16: Verify все cite'ы в `chapter_*.md` имеют entry в `references.bib` (forward + backward consistency)

**Phase B deliverable:** internal-consistency-passed manuscript.

---

## Фаза C — Prose polish (lexicon, academic Russian)

**Goal:** academic Russian register, минимум Anglicisms (где возможно), clear sentence structure, terminology consistency.

**Editorial principles:**
- Active voice preferred where possible
- Avoid «мы» в excess — use «работа», «исследование», «настоящая работа»
- Terms типа «cap», «free agency», «supermax», «PPG», «BPM», «VORP» — оставить английскими (industry standard); first occurrence — gloss in parentheses
- Avoid «фактически», «достаточно», «весьма» — слабые модификаторы
- Avoid double-negatives и over-hedging («возможно может быть» — choose one)
- Reduce sentence length where >40 words

**Claude-K tasks:**
- TASK-K-22: Prose polish chapter_1_introduction.md
- TASK-K-23: Prose polish chapter_2_literature.md
- TASK-K-24: Prose polish chapter_3_methods.md
- TASK-K-25: Prose polish chapter_4_results.md
- TASK-K-26: Prose polish chapter_5_discussion_v2.md
- TASK-K-27: Prose polish chapter_6_conclusion_v2.md
- TASK-K-28: Prose polish ai_disclosure.md
- TASK-K-29: Update abstract.md (RU + EN) — final findings + Hembre 2022 cite

**Phase C deliverable:** polished prose in all 8 final files.

---

## Фаза D — Master document assembly

**Goal:** один документ manuscript_master.md, объединяющий все 8 файлов в правильном порядке HSE format.

**Order (per HSE term paper guideline):**
1. Title page (separate file/manual)
2. Abstract (RU)
3. Abstract (EN)
4. Содержание (auto-generated после .docx conversion)
5. Глава 1. Введение (chapter_1_introduction.md)
6. Глава 2. Литературный обзор (chapter_2_literature.md)
7. Глава 3. Данные и методология (chapter_3_methods.md)
8. Глава 4. Результаты (chapter_4_results.md)
9. Глава 5. Обсуждение (chapter_5_discussion_v2.md)
10. Глава 6. Заключение (chapter_6_conclusion_v2.md)
11. Декларация использования AI (ai_disclosure.md)
12. Список литературы (references — generated from references.bib)
13. Приложение A. Описательная статистика
14. Приложение B. Полные регрессионные таблицы
15. Приложение C. Hash-snapshots + reproducibility commands

**Claude-K tasks:**
- TASK-K-30: Drop deprecated _v1 chapter files (chapter_4_new_sections, chapter_5_discussion без _v2, chapter_6_conclusion без _v2)
- TASK-K-31: Create manuscript_master.md combining 8 final files in HSE order
- TASK-K-32: Verify total length 55–70 страниц (≈ 12-15K слов) после concat
- TASK-K-33: Add proper section numbering (1.1, 1.2, ..., 2.1, ..., 6.5)
- TASK-K-34: Create title page template (Karolina filled with her details)

**Phase D deliverable:** `analysis_v2/reports/manuscript_master.md` ready for pandoc.

---

## Фаза E — Figures + tables embedded

**Goal:** все 7 figures embedded в master с captions; key tables inline; rest tables в Appendix.

**Figures inventory:**
- F1: Waterfall Shapley R² decomposition (HEADLINE) — chapter 4 §4.9
- F2: Age profile salary — chapter 4 §4.2 / §4.5
- F3: Tier β_ppg distribution — chapter 4 §4.3
- F4: Event study around first All-NBA — chapter 4 §4.4
- F5: Tier boxplot salary distribution — chapter 4 §4.3
- F6: Forest plot M_full coefficients — chapter 4 §4.9 / §4.11
- F7: Sequential vs Shapley R² comparison — chapter 4 §4.9

**Tables inventory (inline):**
- T1: Sample summary stats (Chapter 4 §4.1)
- T2: M1a–M1d baseline (Chapter 4 §4.2)
- T3: Tier coefficients in M_full (Chapter 4 §4.3)
- T4: Shapley decomposition (Chapter 4 §4.9)
- T5: Multiple testing summary (Chapter 4 §4.10)

**Tables in appendix:**
- A1: Full descriptive_stats.csv
- A2: All variants of M1c_full (alt_mkt, robust_awards, no_collinear)
- A3: M9a/b/c, M10a/a_robust/b, M11a/b, M_full
- A4: VIF tables
- A5: Oster sensitivity
- A6: Event study coefficients
- A7: Tier-specific Mincer regressions

**Claude-K tasks:**
- TASK-K-35: Generate Russian-language captions for all 7 figures
- TASK-K-36: Insert figure references в chapter_4 (placed near first mention)
- TASK-K-37: Generate Russian-language table captions
- TASK-K-38: Convert key CSV tables → markdown tables embedded in chapter
- TASK-K-39: Generate appendix from full output/tables/ CSV files

**Phase E deliverable:** master document с embedded figures + captioned tables.

---

## Фаза F — Bibliography finalize

**Goal:** Список литературы в APA-формате, alphabetical, ≈ 25–30 финальных references.

**Claude-A primary task lane.**

**Claude-A tasks:**
- TASK-A-17: APA-format check на каждую entry в references.bib
- TASK-A-18: Generate ordered bibliography markdown (alphabetical by first author surname)
- TASK-A-19: Cross-reference check: every cite has entry, every entry is cited
- TASK-A-20: Remove unused entries from references.bib (per bib-check unused list, ~8 entries to consider)
- TASK-A-21: Provide final bibliography Russian heading «Список литературы» (or English «References» если text bilingual)

**Phase F deliverable:** `bibliography/references_final.md` — ready для embed в manuscript.

---

## Фаза G — HSE guideline compliance check

**Goal:** explicit check всех HSE term paper guideline requirements.

**Requirements (per HSE guideline для Article Empirical):**
- Title page: full name, supervisor, year, faculty, programme
- Abstract: ~250 words, key findings, methodology, conclusion (RU + EN)
- Introduction: 10–15% объёма
- Literature Review: 15–20% объёма (ends with hypotheses)
- Methods и Data: 20–25% объёма
- Results: 15–20% объёма (no interpretation)
- Discussion: 15–20% объёма (interpretation + limitations)
- Conclusion: 10–15% объёма (3-5 grouped findings)
- AI Disclosure: separate section §1.3 requirement
- Bibliography: APA, 25–30 sources
- Total: 55–70 страниц

**Claude-K tasks:**
- TASK-K-40: Wordcount audit each chapter — compute % of total
- TASK-K-41: If chapters > or < target — trim or expand с принципом «trim Chapter 2 if total >70 pages, expand Chapter 5 if <55»
- TASK-K-42: Title page populated
- TASK-K-43: Abstract RU + EN — exactly 250 words each, structured (background, methods, findings, conclusion)
- TASK-K-44: AI Disclosure section conformance check

**Joint task:**
- TASK-J-01: HSE template guideline final readout (Title page, fonts, margins, page numbers) — confirm before .docx export

**Phase G deliverable:** compliance-checked master manuscript.

---

## Фаза H — Final .docx export + visual review

**Goal:** компилированный .docx с правильным форматированием, ready для печать / Adobe Reader review.

**Pandoc command (предполагаемый):**
```bash
pandoc analysis_v2/reports/manuscript_master.md \
  --reference-doc=hse_term_paper_template.docx \
  --bibliography=bibliography/references.bib \
  --csl=apa.csl \
  --citeproc \
  -o output/coursework_final.docx
```

**Claude-K tasks:**
- TASK-K-45: Check pandoc availability (брат pandoc-3.9.0.2-arm64-macOS.pkg в data/lookups/)
- TASK-K-46: Find/create HSE term paper .docx template (Times New Roman 14pt, 1.5 spacing, A4, page numbers, margins)
- TASK-K-47: Run pandoc conversion
- TASK-K-48: Verify generated .docx — figures embedded, citations rendered APA, table of contents auto-generated
- TASK-K-49: Manual touch-ups если нужны (Adobe Reader, MS Word visual check)
- TASK-K-50: Generate final hash-snapshot финального .docx

**Phase H deliverable:** `output/coursework_final.docx` — submission-ready.

---

## Расписание async-итераций

Realistic estimate — 5–8 full async-cycles между Claude-K и Claude-A.

| Iteration | Лидер | Focus |
|---|---|---|
| 1 | Claude-K | Kick off Phase A (Kopkin, Keefer, B&K, White integration) |
| 2 | Claude-A | Phase A bibliography cleanup (TASK-A-10/11/12) + ref check |
| 3 | Claude-K | Phase B consistency check + Phase C polish chapters 1–3 |
| 4 | Claude-A | HSE proxy attempt для paywall (если есть access) + bib-check 2 |
| 5 | Claude-K | Phase C polish chapters 4–6 + Phase D master assembly |
| 6 | Claude-A | Phase F bibliography generation alphabetical APA |
| 7 | Claude-K | Phase E figures captions + Phase G compliance |
| 8 | Claude-K | Phase H pandoc conversion + final .docx |

Каждая итерация — один cycle (push → pull → process → push). При active session это секунды; при cron-driven — минимум 5 мин на firing.

---

## Признание неопределённостей

1. **HSE template** — не уверены, что у нас есть точный HSE-supplied .docx template. Возможно потребуется сборка template'a руками или request Karolina'е.
2. **HSE library proxy** — Claude-A не может его использовать самостоятельно (требует студенческого login); это блокирует получение PDF для Lipovetsky-Conklin, Mincer book, Hill-Groothuis, Stiroh, Johnson-Hall (paywall). Karolina может попробовать.
3. **Pandoc availability** — installer лежит в репо, но может не быть запущен; локальной pandoc-installation потребуется.
4. **APA citation rendering** — pandoc с citeproc + apa.csl даёт почти-perfect output, но может потребовать manual touchup для русских entries.
5. **«10/10 идеально»** — фундаментально требует human review. AI builds best-possible draft; Karolina + advisor дают final approval.
6. **Length 55–70 страниц** — текущий draft на ~13 600 слов; при 250 слов/страница это ~54 страницы, что около нижней границы. Возможно нужно немного расширить (особенно Discussion).

---

## Endorsement / Review section

Plan этот написал Claude-K. Перед началом execution — приглашаю **Claude-A** к review:

**Claude-A, прошу проанализировать:**
1. Logical sequence Phase A → H — нет ли пропущенных steps?
2. Task разделение Claude-K / Claude-A — корректно ли распределение по lanes?
3. Estimated 5–8 iterations — реалистично ли?
4. Признания неопределённостей — что я упустил?
5. Любые дополнительные предложения по структуре?

Твой response — в `coordination/FOR_KAROLINA.md` под раздел «MASTER_PLAN review». Если согласишься без правок — пиши «✅ endorsed, начинаю Phase A tasks с моей стороны». Если есть правки — пиши конкретные.

После твоего endorsement обе стороны переходят к execution: Claude-K стартует Phase A с TASK-K-10 (Kopkin integration), Claude-A — с TASK-A-10 (johnson bibkey fix).

---

**План версия:** v1, 2026-05-22
**Авторы:** Claude-K (initial), Claude-A (review pending)
**Изменения:** через commit с пометкой `[PLAN]` в commit message; notify обоих Claude'ов через TASKS.md.
