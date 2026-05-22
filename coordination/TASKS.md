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
