# Coursework — task queue

> Async task queue between Claude-K (Karolina's Claude) and Claude-A (Artem's Claude). Rules — `coordination/PROTOCOL.md`. Update from your own side only; do not edit other Claude's tasks.

**Last sync:** 2026-05-22 (Claude-K initial setup).

---

## Claude-K queue (Karolina's Claude)

### TASK-01: Introduction skeleton (~1800 слов)
**Status:** in_progress
**Deliverable:** `analysis_v2/reports/chapter_1_introduction.md`
**Confidence:** medium (для motivation, RQ, contribution preview — ok; для цитат — TBD-маркеры, ждут библиографии)
**Dependencies:** none (можно начинать; TBD-cite'ы потом)
**Outline:**
- 1.1 Motivation (общая значимость NBA как labor market lab, Kahn 2000)
- 1.2 Тема и Research Question
- 1.3 Contribution preview (количественная декомпозиция через Shapley — новое для NBA-литературы)
- 1.4 Структура работы

### TASK-02: Literature Review skeleton (~2400 слов)
**Status:** pending (после TASK-01)
**Deliverable:** `analysis_v2/reports/chapter_2_literature.md`
**Confidence:** medium-low (нужны источники из `bibliography/sources/`; пока могу написать skeleton с TBD-маркерами для конкретных cite'ов)
**Dependencies:** требует TASK-A-02 (rest of batch sources from Claude-A) для полного content
**Outline:**
- 2.1 Stream 1: Mincer / productivity (Rosen 1981, Mincer 1974, Hill & Groothuis 2001, Hausman & Leonard 1997, Krautmann 1999)
- 2.2 Stream 2: Institutional / CBA (Coon FAQ, Hinton & Sun 2019, Berri & Schmidt 2010)
- 2.3 Stream 3: Awards / signaling (Lazear & Rosen 1981, Stiroh 2007)
- 2.4 Stream 4: Market / team context (Hembre 2021 — с caveat про NBA-only insignificant, Berri et al. 2007, Kahn 2000)
- 2.5 Stream 5: Externalities / health (Yang & Lin 2012, Robst et al. 2011)
- 2.6 Hypotheses H1-H10 (привязка к streams)

### TASK-03: Discussion skeleton (~1800 слов)
**Status:** pending (после TASK-01, TASK-02 + достаточно sources)
**Deliverable:** `analysis_v2/reports/chapter_5_discussion.md` (переписать существующий)
**Confidence:** medium (структура ясна, нужны источники для cite'ов)
**Dependencies:** TASK-A-02, TASK-A-03 batches от Claude-A
**Outline:**
- 5.1 Shapley decomposition interpretation (главный finding)
- 5.2 Institutional layer (H3) — Rosen 1986 cap-truncation
- 5.3 Awards channel timing (H5, H6) — Lazear-Rosen tournaments + Stiroh contract-cycle
- 5.4 Anti-marketability (H7) — Hembre channel с caveat
- 5.5 Team controls null (H8) — informative null
- 5.6 Tax null (H9) — Hembre context
- 5.7 Durability (H10)
- 5.8 Limitations / threats to internal validity

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

### TASK-A-02: Mid-priority sources (next batch)
**Status:** pending (Claude-A работает в фоне, согласно user)
**Deliverable:** заполненные шаблоны для:
- Mincer (1974), Lazear & Rosen (1981), Hausman & Leonard (1997)
- Krautmann (1999), Hill & Groothuis (2001), Stiroh (2007)
- Berri et al. (2007), Hinton & Sun (2019)
**Confidence (Claude-K's request):** для каждого шаблона — особенно проверить numeric claims (R², coefficients, sample sizes), которые мы будем цитировать. Если что-то выглядит подозрительным — verify в исходнике или флагуй HUMAN_REVIEW.

### TASK-A-03: Low-priority + methods sources
**Status:** pending
**Deliverable:** шаблоны для Yang & Lin (2012), Robst et al. (2011), Kahn (2000), Rottenberg (1956), Oster (2019), Benjamini-Hochberg (1995), MacKinnon-Webb (2018)

### TASK-A-04: Hembre published title verification
**Status:** pending (open question from Claude-A's batch 1)
**Deliverable:** verified APA cite (либо preprint title, либо real published title в JSE)
**Confidence:** high (механическая verification через Sage / JSE site)
**Notes from Claude-K:** preprint title — *State Income Taxes and Team Performance* (SSRN 2946169). Если published version в JSE имеет другой title — заменить в bibliography_proposal.md и proposed-cite в chapter_6_conclusion_v2.md §6.2 Вывод 3.

---

## HUMAN_REVIEW queue

(empty — currently no blocking questions)

---

## Done (recent, last 20)

- 2026-05-22 — `chapter_3_methods.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `chapter_4_results.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `chapter_6_conclusion_v2.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `ai_disclosure.md` written (Claude-K, commit c244bde)
- 2026-05-22 — `bibliography/README.md` + TEMPLATE.md (Claude-K, commit b225641)
- 2026-05-22 — Hembre fix applied to chapter_6 + bibliography_proposal (Claude-K, commit e17b8bd)
- 2026-05-22 — `bibliography/findings_log.md` batch-1 (Claude-K, commit e17b8bd)
- 2026-05-22 — top-5 sources reviewed (Claude-A → Claude-K, commit 64d4405)
- 2026-05-22 — repository initialized + pushed to GitHub (Claude-K, commit f946f2d)
