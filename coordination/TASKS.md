# Coursework — task queue

> Async task queue between Claude-K (Karolina's Claude) and Claude-A (Artem's Claude). Rules — `coordination/PROTOCOL.md`. Update from your own side only; do not edit other Claude's tasks.

**Last sync:** 2026-05-22 (Claude-K initial setup).

---

## Claude-K queue (Karolina's Claude)

### TASK-01: Introduction skeleton — ✅ done
**Status:** done (commit aafbac6, 2026-05-22)
**Deliverable:** `analysis_v2/reports/chapter_1_introduction.md` (~1800 слов)
**Notes:** 4 TBD-маркеров на cite'ы (Berri-Schmidt 2010, Hinton-Sun 2019, Stiroh 2007). Финальная привязка после batch-2 от Claude-A.

### TASK-02: Literature Review skeleton — ✅ done
**Status:** done (commit d0bf4b2, 2026-05-22)
**Deliverable:** `analysis_v2/reports/chapter_2_literature.md` (~2400 слов)
**Notes:** 5 streams + Research gap + H1-H10 formulation. 14 TBD-маркеров на cite'ы. Использует verified cites: Rosen (1981), Hembre (2021) с caveat, Coon (n.d.).

### TASK-03: Discussion skeleton — ✅ done
**Status:** done (commit 369757c, 2026-05-22) — `chapter_5_discussion_v2.md` (~1850 слов)
**Deliverable:** заменяет старый `chapter_5_discussion.md` (3300 слов сырья → будет dropped после ready финального текста)
**Notes:** 7 sections + Limitations. 7 TBD-маркеров. Hembre framing следует findings_log batch-1 (NBA-only insignificant caveat).

### TASK-04: Update abstract.md after content fixes
**Status:** pending
**Deliverable:** `analysis_v2/reports/abstract.md` (RU + EN)
**Confidence:** high (механическая правка после Hembre cite)
**Dependencies:** только final-draft проход

### TASK-05: Прочитать новые шаблоны от Claude-A когда придут (batch 2+)
**Status:** standby (continuous)
**Deliverable:** integrate findings into chapter drafts, update `bibliography/findings_log.md`
**Confidence:** high (это процедурная задача)
**Dependencies:** ждёт push'ей от Claude-A

---

## Claude-A queue (Artem's Claude)

### TASK-A-01: Top-5 priority bibliography sources
**Status:** done (PR #1, merged 2026-05-22)
**Deliverable:** `bibliography/sources/{hembre,lipovetsky,cameron,rosen,coon}.md`
**Notes from Claude-K:** все 5 шаблонов прочитаны и применены. Hembre — substance fix применён. См. `bibliography/findings_log.md` batch 1.

### TASK-A-02: Mid-priority sources (next batch) — ✅ done
**Status:** done (PR #2 merged 2026-05-22; см. FOR_KAROLINA.md для подробностей)
**Deliverable:** все 8 шаблонов в `bibliography/sources/`:
- mincer_1974.md (skeleton — NBER только ToC PDF доступен)
- lazear_1981.md (FULL — NBER WP w0401, полный текст)
- hausman_1997.md (FULL — MIT DSpace WP)
- krautmann_1999.md (skeleton — Wiley paywall)
- hill_2001.md (skeleton — Sage paywall)
- stiroh_2007.md (skeleton — Wiley paywall; ⚠ DOI typo в proposal: было `.00010.x`, реально `.00004.x`)
- berri_2007.md (skeleton — IJSF/FIT paywall)
- hinton_2019.md (skeleton; ⚠ **TOPIC MISMATCH**: указанный в proposal "supermax" paper НЕ СУЩЕСТВУЕТ. Реальный Hinton-Sun 2019 = "Sunk-cost fallacy in NBA" — другая тема. Skip из финальной biblio для supermax-аргумента.)
**Notes from Claude-A:** numeric claims в FULL templates verified из PDF; в skeleton — из abstracts + secondary sources с маркером ⚠. См. `bibliography/findings_log.md`.

### TASK-A-05: Hill & Groothuis (2001) template — ✅ done (в TASK-A-02)
**Status:** done (PR #2 merged 2026-05-22)
**Deliverable:** `bibliography/sources/hill_2001.md` (skeleton — Sage paywall)
**Confidence answer:** Hill-Groothuis (2001) per abstract обсуждает median-voter model и Robin Hood rent redistribution в новом CBA (post-1995). Direct тестирование structural break как такового в abstract не упоминается — нужен full text для verification. Использовать осторожно как **theoretical antecedent** для H4 post-CBA-2017, не как direct empirical parallel. HSE proxy для Sage был бы полезен.

### TASK-A-06: Mincer (1974) template — ✅ done (в TASK-A-02)
**Status:** done (PR #2 merged 2026-05-22)
**Deliverable:** `bibliography/sources/mincer_1974.md` (skeleton — только ToC доступен; book chapter PDFs partial)
**Confidence answer:** earnings function $\ln(W) = f(\text{schooling}, \text{experience}, \text{experience}^2)$ — canonical Mincer formulation, **широко** подтверждена в secondary literature (Heckman, Lochner & Todd 2003; Lemieux 2006). Foundational claim — solid. Полный текст книги нужен для verbatim quotes; HSE library access (book ISBN 978-0-870-14265-9).

### TASK-A-07: Kahn (2000) template — ✅ done (в TASK-A-03)
**Status:** done (PR #2 merged 2026-05-22)
**Deliverable:** `bibliography/sources/kahn_2000.md` (skeleton — AEA captcha-blocked для direct download)
**Confidence answer:** title "The Sports Business as a Labor Market Laboratory" — verified через Crossref (DOI 10.1257/jep.14.3.75, JEP 14(3), 75-94). Точная цитата p. 75 — нужен full PDF для verbatim. AEA формально open access; нужен HSE library proxy либо AEA account.

### TASK-A-03: Low-priority + methods sources — ✅ done
**Status:** done (PR #2 merged 2026-05-22)
**Deliverable:** все 7 шаблонов:
- yang_2012.md (skeleton — Sage paywall)
- robst_2011.md (skeleton; ⚠ **TOPIC MISMATCH**: указанный perf-variability paper НЕ СУЩЕСТВУЕТ. Real Robst-VanGilder-Coates-Berri 2011 = "Skin tone and wages" — другая тема. Для perf-variability аргумента — заменить на Bodvarsson & Brastow (1998), см. `additional_proposals.md`)
- kahn_2000.md (skeleton — см. TASK-A-07)
- rottenberg_1956.md (skeleton — JSTOR/UChicago paywall)
- oster_2019.md (FULL — Emily Oster's site)
- benjamini_1995.md (skeleton — Wiley paywall, no preprint)
- mackinnon_2018.md (FULL — Queen's University WP)

### TASK-A-04: Hembre published title verification — ✅ done
**Status:** done (verified via Crossref query 2026-05-22; `references.bib` updated)
**Found:**
- DOI: `10.1007/s10797-021-09685-y`
- Journal: **International Tax and Public Finance** (НЕ Journal of Sports Economics как в proposal)
- Year: 2022 (online first 2021)
- Volume/issue/pages: 29(3), 704–725
- Title: "State Income Taxes and Team Performance" (та же, что у preprint)
**Notes from Claude-A:** bibkey в `references.bib` изменён `hembre_2021 → hembre_2022`. Если у тебя в `chapter_*.md` уже стоит `\cite{hembre_2021}` — нужна замена. Скажи в FOR_KAROLINA.md, могу подготовить PR с alias entry для compatibility.

### TASK-A-08: Master deliverables (PR #2 final batch) — ✅ done
**Status:** done (PR #2 merged 2026-05-22)
**Deliverable:**
- `bibliography/MASTER_TABLE.md` — сегментированная таблица 32 source'ов с priority + status
- `bibliography/references.bib` — BibTeX для всех 32 + ⚠ markers для DOI/title issues
- `bibliography/additional_proposals.md` — 12 NEW из CSV "Анализ статей" с priority recommendations (просьба к Karolina: решить какие добавить в `bibliography_proposal.md`)
**Action for Claude-K:** см. `coordination/FOR_KAROLINA.md` «Что нужно от тебя» — особенно решение по NEW sources + HSE proxy для top-priority paywall'нутых.

### TASK-A-09: Stand-by для следующих циклов
**Status:** standby (continuous)
**Deliverable:** реакция на новые задачи из Claude-K queue, запросы в FOR_ARTEM.md, или ручные prompt'ы от Artem.
**Confidence:** high (процедурная задача)
**Dependencies:** ждёт push'ей от Claude-K или ручных prompt'ов.

---

## HUMAN_REVIEW queue

(empty — currently no blocking questions)

---

## 🚀 NEW: Phase-driven tasks per MASTER_PLAN.md

User goal: maximally-polished .docx coursework ready for HSE submission. Plan in `coordination/MASTER_PLAN.md`. Phases A–H. Below — full task list. Both Claudes execute on their lanes.

### Phase A — Content completion

**Claude-K queue:**
- **TASK-K-10:** ✅ done (commit f7cecbd) — Kopkin (2012) integrated в chapter_2 §2.6 + chapter_5 §5.5
- **TASK-K-11:** ✅ done (commit ea6b1d3) — Keefer (2021) integrated в chapter_5 §5.7
- **TASK-K-12:** ✅ done (commit ea6b1d3) — Berri & Krautmann (2006) integrated в chapter_5 §5.7
- **TASK-K-13:** ✅ done (commit ea6b1d3) — White & Sheldon (2014) integrated в chapter_5 §5.7
- **TASK-K-14:** ✅ done (commit ea6b1d3) — TBD body markers cleaned via sed across chapters 1/2/3/5
- **TASK-K-15:** ✅ done (Pratt 1987 + Genizi 1993 уже в Methods §3.6)
- **TASK-K-16:** ✅ done (Shapley 1953 уже в Methods §3.6)
- **TASK-K-17:** ✅ done (Rosen 1986 уже в Methods §3.4 + Discussion §5.2)

**Claude-A queue:**
- **TASK-A-10:** ✅ done (commit de3be58) — bibkey renamed johnson_2017 → johnson_2018
- **TASK-A-11:** ✅ done (commit de3be58) — hinton_2019 + robst_2011 removed
- **TASK-A-12:** ✅ done (commit de3be58) — berri_schmidt_2010 @book added (Stumbling on Wins, FT Press, ISBN 978-0-13-235778-5)
- **TASK-A-13:** 🚫 BLOCKED — HSE library proxy требует student login; Claude-A не может self-execute. Karolina (human) — нужна твоя сторона. Top-priority paywall: lipovetsky_2001, mincer_1974 (full book), hill_2001, stiroh_2007, johnson_2018, kopkin_2012. Karolina ответила «пока нет доступа» 2026-05-22 — пропускаем для draft v2, ждём финальной верификации перед защитой.
- **TASK-A-14:** ✅ done — verified 25 DOIs via Crossref; 3 typos fixed (kopkin_2012, krautmann_donley_2009, simmons_2011 — все близкие но неверные digits). Все 25 теперь валидны.
- **TASK-A-15a:** ⏳ Endorsed (Artem suggestion #1) — после K-10..K-17 запустить `grep -r '\[TBD' analysis_v2/reports/` чтобы убедиться нет упущенных маркеров. (Claude-K side: проверка сделана 2026-05-22, 0 body markers.)

### Phase B — Cross-chapter consistency

**Claude-K queue:**
- **TASK-K-18:** ✅ done (commit pending) — H1-H10 numbering audit; H11 leftovers only in deprecated _v1 files (drop in K-30)
- **TASK-K-19:** ✅ done (commit pending) — fixed peak age (29.5 not 28-29), post_cba_2017 (+24.5% not +26%), 10 hypotheses (not 11), Hembre 2022 в abstract
- **TASK-K-20:** ✅ done (commit pending) — 8-tier list в chapter_1 §1.2 расширен (добавлен high-mid), терминология консистентна
- **TASK-K-21:** ✅ done (commit pending) — Глава/§/Рисунок/Таблица cross-refs verified в v2 chapters

**Claude-A queue:**
- **TASK-A-15:** Re-run bib_check_report.md после K-10..K-17
- **TASK-A-16:** Forward + backward cite consistency check

### Phase C — Prose polish

**Claude-K queue:**
- **TASK-K-22..27:** Prose polish chapters 1–6 (по одной за task)
- **TASK-K-28:** Prose polish ai_disclosure.md
- **TASK-K-29:** Update abstract.md (RU + EN) — final findings + Hembre 2022

### Phase D — Master document assembly

**Claude-K queue:**
- **TASK-K-30:** Drop deprecated _v1 chapter files (chapter_4_new_sections.md, chapter_5_discussion.md, chapter_6_conclusion.md без _v2 suffix)
- **TASK-K-31:** Create manuscript_master.md combining 8 files in HSE order
- **TASK-K-32:** Length 55–70 страниц check
- **TASK-K-33:** Section numbering (1.1, 1.2, …)
- **TASK-K-34:** Title page template (Karolina человек ответила «пока проскипать» — defer до final pass)

**Claude-A queue:**
- **TASK-A-23:** ⏳ Endorsed (Artem suggestion #3) — prepare Reproducibility appendix: bundle coordination/ files (PROTOCOL, TASKS, FOR_*, MASTER_PLAN, findings_log) как evidence of process для Приложение C. Strengthens AI Disclosure.

### Phase E — Figures + tables

**Claude-K queue:**
- **TASK-K-35:** Russian-language figure captions (F1–F7)
- **TASK-K-36:** Insert figure references в chapter_4
- **TASK-K-37:** Russian-language table captions
- **TASK-K-38:** Key tables → markdown tables inline
- **TASK-K-39:** Generate appendix from full output/tables/ CSV

### Phase F — Bibliography finalize

**Claude-A queue:**
- **TASK-A-17:** APA-format check per bib entry
- **TASK-A-18:** Generate alphabetical ordered bibliography markdown
- **TASK-A-19:** Forward + backward cite consistency v2
- **TASK-A-20:** Remove unused entries from references.bib
- **TASK-A-21:** Final bibliography Russian heading + format
- **TASK-A-22:** ⏳ Endorsed (Artem suggestion #2) — prepare list of Claude commits для AI Disclosure (explicit log с commit references, что было сделано). Pair с Claude-K's TASK-K-28 (ai_disclosure prose polish).

### Phase G — HSE compliance

**Claude-K queue:**
- **TASK-K-40:** Wordcount audit per chapter, % of total
- **TASK-K-41:** Trim/expand chapters per HSE targets
- **TASK-K-42:** Title page populated
- **TASK-K-43:** Abstract RU + EN exactly 250 words, structured
- **TASK-K-44:** AI Disclosure §1.3 compliance check

**Joint:**
- **TASK-J-01:** HSE template guideline readout (fonts/margins/page numbers) — BLOCKED: у Karolina пока нет HSE template; используем generic.
- **TASK-J-02:** ⏳ Endorsed (Artem suggestion #4) — pre-final read-through на single chunk (после конкатенации в master). Может выявить cross-chapter awkwardness, которые grep не найдёт.

### Phase H — Pandoc → .docx

**Claude-K queue:**
- **TASK-K-45..50:** Pandoc setup → conversion → visual check → hash-snapshot final .docx

**Claude-A queue:**
- **TASK-A-24:** ⏳ Endorsed (Artem suggestion #5) — prepare generic `hse_term_paper_template.docx` (Times New Roman 14pt, 1.5 spacing, A4, поля 2cm, page numbers) как fallback. Karolina ответила «нет HSE template» 2026-05-22 — generic становится primary, не fallback.

---

## Done (recent, last 20)

- 2026-05-22 — `chapter_5_discussion_v2.md` written (Claude-K, commit 369757c, TASK-03)
- 2026-05-22 — `chapter_2_literature.md` written (Claude-K, commit d0bf4b2, TASK-02)
- 2026-05-22 — `chapter_1_introduction.md` written (Claude-K, commit aafbac6, TASK-01)
- 2026-05-22 — coordination/ infrastructure (Claude-K, commit 9675059)
- 2026-05-22 — `chapter_3_methods.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `chapter_4_results.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `chapter_6_conclusion_v2.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `ai_disclosure.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `bibliography/README.md` + TEMPLATE.md (Claude-K, commit b225641)
- 2026-05-22 — Hembre fix applied to chapter_6 + bibliography_proposal (Claude-K, commit e17b8bd)
- 2026-05-22 — `bibliography/findings_log.md` batch-1 (Claude-K, commit e17b8bd)
- 2026-05-22 — top-5 sources reviewed (Claude-A → Claude-K, commit 64d4405)
- 2026-05-22 — repository initialized + pushed to GitHub (Claude-K, commit f946f2d)
