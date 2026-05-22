# Журнал критических находок из bibliography

> Записываются «surprising» находки от коллеги при разборе источников — те, что меняют наши claims, citations или интерпретацию. Это **не** полный лог библиографии (для этого есть `sources/`), а только substance-affecting items.

---

## Batch 1: top-5 источники (2026-05-22, PR #1)

### Hembre (2021) — CITE ERROR + NBA-only INSIGNIFICANT

**Что было:** в `bibliography_proposal.md` источник был обозначен как:
- Title: *Tax Competition in Professional Sports: A Theoretical and Empirical Analysis*
- DOI: 10.1177/1527002520968551

**Что найдено:**
- DOI возвращает 404 в Crossref (проверено 2026-05-22).
- Preprint доступен на SSRN 2946169 под title *State Income Taxes and Team Performance* (revised February 2021).
- Возможно published title в JSE отличается; нужно verify через Sage.

**Что важнее (substance):**
- **NBA-specific coefficient в Hembre НЕ значим** (β_NBA ∈ [−0.143, −0.069], SE > 1.1, Table 3, p. 20).
- Главный effect Hembre — pooled across 4 leagues (NFL/NBA/NHL/MLB), не специфически про NBA.

**Применённые правки в драфтах:**
- `analysis_v2/reports/bibliography_proposal.md` — title + DOI + caveat исправлены.
- `analysis_v2/reports/chapter_6_conclusion_v2.md` §6.2 Вывод 3 — формулировка изменена: теперь не "согласуется с Hembre" а "Hembre даёт theoretical channel, совместимый с направлением; NBA-specific coefficient у него imprecise".
- `analysis_v2/reports/chapter_6_conclusion_v2.md` §6.4 — добавлен пункт 6 про market vs tax channel не разложение.

**Не правлены (исторические/устаревшие):**
- `analysis_v2/reports/SHIPPING_SUMMARY.md`, `phase3_summary.md`, `h8_notes.md`, `chapter_4_new_sections.md` — internal notes, не идут в финальный текст.
- `analysis_v2/reports/chapter_5_discussion.md` — будет переписан целиком при работе над Discussion (после получения остальных источников); править сейчас по точке не имеет смысла.
- `analysis_v2/reports/abstract.md` — потребуется правка перед финалом, отметить в TODO.

**Open question от Артёма:** есть ли у нас joint spec с continuous `state_tax_rate` + `top5_market` в одной модели?
**Ответ:** нет. В `analysis_v2/m1_full.py:159` `STRUCT_BLOCK = ["post_cba_2017", "post_covid", "no_income_tax"]` — только бинарный `no_income_tax`. Continuous `state_tax_rate` использовался только в v1 M2c (без top5_market). Прямая декомпозиция market vs tax channels — future robustness work, отмечена в §6.4 пункт 6.

---

### Lipovetsky & Conklin (2001) — PAYWALL

**Что:** Wiley paywall, preprint / open access version не найден.

**Применённые правки:** пока никаких — методологическое описание Shapley в `chapter_3_methods.md` §3.6 опирается на standard formula (Shapley 1953), не требующую verbatim из L&C 2001. Caveat о paywall будет отмечен при подготовке Bibliography.

**Альтернативный source если verbatim quotes понадобятся:** Grömping, U. (2007). Estimators of relative importance in linear regression based on variance decomposition. *American Statistician, 61*(2), 139–147. — open access secondary review с подробным описанием Shapley R² method.

**Action:** Karolina может попробовать через HSE library proxy (Wiley доступ).

---

### Cameron-Gelbach-Miller (2011) — OPEN QUESTION

**Что:** полный PDF + точные page-references есть. Артём отметил open question: используем ли мы two-way clustering где-то?

**Ответ:** проверено в коде: only one-way clustering на `player_id` (см. `analysis_v2/m1_full.py`, `analysis_v2/h_decomposition.py`). Two-way (player + season) НЕ используется. CGM 2011 цитируется per their **general framework + eq. (2.7) one-way formula**, не per two-way innovation.

**Применённые правки:** в `chapter_3_methods.md` §3.5.1 цитата CGM 2011 уже корректна — обоснование cluster-robust SE. Никаких изменений не требуется.

**Action:** если будет финальное предложение от Артёма попробовать two-way (для robustness), можно добавить как `M1c_full_2wayCluster` спецификацию. Пока — не делаем.

---

### Rosen (1981) — OK

**Что:** полный PDF, верифицированные quotes, p. 845/849/857.

**Применённые правки:** никаких — в Methods/Results я не цитировал Rosen, он пойдёт в Introduction (motivation про superstar economics) и Lit Review Stream 1, когда сяду за них.

**Notes для future use:**
- Quote "A person who is twice as talented as another earns four times more money" (p. 849) — отличный кандидат в Introduction.
- Marshall quote (p. 857) — кандидат на эпиграф к Discussion.

---

### Coon CBA FAQ — OK

**Что:** полный snapshot HTML, Q-numbers (Q23 max tiers, Q24 Designated Player, Q32 Bird rights, Q18 luxury tax).

**Применённые правки:** никаких сейчас. Будут добавлены в Methods §3.4 при финальной редактуре (конкретные ссылки на Q-numbers вместо общего "(Coon, n.d.)" cite).

**Important context:** Larry Coon retired May 2025, FAQ frozen. Snapshot сохранён локально (`bibliography/pdfs/coon_cbafaq_snapshot_2024.html`) для reproducibility.

---

## Batch 2/3/4: PR #2 — 27 новых templates (2026-05-22)

Артём + Claude-A прислали огромный batch: 27 новых templates, MASTER_TABLE, references.bib, additional_proposals. См. `coordination/FOR_KAROLINA.md` для overview.

### Hembre (2021 → 2022) — CITE FULLY CORRECTED

**Что найдено в batch-2:** через Crossref verification — published version имеет другой journal и DOI чем proposal указывал:
- **Journal:** International Tax and Public Finance (НЕ Journal of Sports Economics)
- **DOI:** 10.1007/s10797-021-09685-y
- **Year:** 2022 (online first 2021)
- **Volume:** 29(3), 704–725
- **Bibkey:** hembre_2022

**Применено:** все упоминания «Hembre (2021)» / «Hembre, 2021» заменены на «Hembre (2022)» / «Hembre, 2022» в chapter_1, 2, 5_v2, 6_v2. `bibliography_proposal.md` Б1 entry обновлён (commit 2baa0eb).

### Hinton & Sun (2019) — TOPIC MISMATCH, DROPPED

**Что найдено:** указанный в proposal "supermax NBA" paper НЕ СУЩЕСТВУЕТ. Реальный Hinton-Sun (2019) — "Sunk-cost fallacy in NBA" (*Empirical Economics, 59*), другая тема.

**Применено:** удалены все cite'ы Hinton-Sun (2019) из chapter_1 §1.2, chapter_2 §2.3, §2.8 H3/H4 formulations, hypotheses_v2_final.md, bibliography_proposal.md Б2 (commit 2baa0eb). Для supermax-аргумента остаётся Coon (n.d., Q24) как primary institutional reference.

### Robst et al. (2011) — TOPIC MISMATCH, DROPPED

**Что найдено:** указанный в proposal "performance variability" paper НЕ СУЩЕСТВУЕТ. Реальный Robst-VanGilder-Coates-Berri (2011) — "Skin tone and wages", другая тема. Replacement candidate: Bodvarsson & Brastow (1998), но PDF и template отсутствуют.

**Применено:** удалены все cite'ы Robst (2011) из chapter_2 §2.6, chapter_5 §5.6, §2.8 H10 formulation, hypotheses_v2_final.md, bibliography_proposal.md Б6 (commit 2baa0eb).

### Stiroh (2007) — DOI TYPO

**Что найдено:** real Crossref DOI ends `.00004.x`, не `.00010.x` как в proposal.

**Применено:** bibliography_proposal.md Б3 entry обновлён (commit 2baa0eb).

### Johnson & Hall (2018) — CRITICAL H9 COUNTER-EVIDENCE

**Что найдено:** прямой NBA + tax + individual salary paper. На 576 FA signings (2010–2014) находят +$60K на pp ATR (Average Tax Rate). **Direct counter-evidence** нашему H9 null в данных 2015–2024.

**Применено в драфтах:**
- `chapter_2_literature.md` §2.6 — добавлен абзац с описанием и paywall caveat (commit f5bfeee).
- `chapter_5_discussion_v2.md` §5.5 — MAJOR REFRAME: вместо «tax channel not detectable», теперь «informative null vs Johnson-Hall evidence», с тремя explanation для divergence (sample composition, CBA 2017 structural break, ATR vs MTR spec) (commit f5bfeee).

### Kleven, Landais & Saez (2013) — Stream 5 main theoretical anchor

**Что:** AER 103(5), 1892–1924. Elasticity foreign players w.r.t. net-of-tax rate ≈ 1.0; domestic ≈ 0.15. Verified quotes p. 1894.

**Применено:** `chapter_2_literature.md` §2.6 + §2.8 H9 formulation (commit f5bfeee).

### Alm, Kaempfer & Sennoga (2012) — MLB analog для H9

**Что:** Tulane WP 1209 / JSE 13(6). 372 MLB FA, 1995–2001. β_MTR = +$21–24k на pp tax. Verified Table 3, p. 11; quote p. 13.

**Применено:** `chapter_2_literature.md` §2.6 + §2.8 H9 (commit f5bfeee).

### Hausman & Leonard (1997) — H5 superstar externality

**Что:** JLE 15(4), 586–624. Verified externality quote p. 9, Jordan $8.6M p. 18, $53M total externality Section V.

**Применено:** `chapter_2_literature.md` §2.2 заменён TBD на verified cite (commit f5bfeee). H1 formulation §2.8 [TBD] removed.

### Lazear & Rosen (1981) — H5/H6 tournament theory

**Что:** JPE 89(5), 841–864 / NBER WP 401. Verified quote p. 2 ("prizes selected... effort efficiently").

**Применено:** `chapter_2_literature.md` §2.4 + §2.8 H5 formulation + chapter_5 §5.3 verified quote (commit f5bfeee).

### Hölmström (1979) — Stream 3 theoretical foundation

**Что:** Bell J. Econ 10(1), 74–91. Verified Proposition 3 quote p. 84 ("informativeness principle").

**Применено:** `chapter_2_literature.md` §2.4 + chapter_5 §5.3 + §2.8 H5 formulation (commit f5bfeee).

### Open questions для Karolina

1. **HSE library proxy для paywall sources** — для Lipovetsky-Conklin (2001), Benjamini-Hochberg (1995), Mincer (1974) book, Hill-Groothuis (2001), Stiroh (2007), Johnson-Hall (2018) — Karolina может попробовать HSE proxy для Wiley / Sage / T&F / NBER access. Для финального текста — этого было бы достаточно, чтобы заменить skeleton-cite'ы на full quotes.

2. **additional_proposals.md merge** — Артём предложил 7 NEW из CSV для добавления в proposal: Kleven 2013, Alm 2012, Kopkin 2012, Johnson 2017, Hölmström 1979, Keefer 2021, Berri-Krautmann 2006. Из них уже verified-applied в драфтах: Kleven, Alm, Johnson, Hölmström (4 из 7). Остальные 3 (Kopkin, Keefer, Berri-Krautmann) — рекомендую согласиться + Артём подготовит PR с обновлённым `bibliography_proposal.md`.

3. **Bib-check после финальной правки** — Артём готов пройтись по всем cite'ам в `chapter_*.md` против `references.bib` после финального текста. Скажу ему когда готовы.
