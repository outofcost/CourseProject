# Bibliography findings log

Substance findings от работы с источниками — то, что **меняет интерпретацию** текста курсовой или требует решения от Кирилла. Не routine status updates (для них — `MASTER_TABLE.md`).

Формат: `[YYYY-MM-DD]` `Claude-A: ...` или `Claude-K: ...`. Новые записи **сверху**.

---

## [2026-05-22] Claude-A: финал первого raid'а

32 источника обработаны. PR #1 (open): top-5 + 4 batch-коммита от 3 параллельных агентов + финальный (MASTER_TABLE / references.bib / additional_proposals). Артефакты:

- `bibliography/MASTER_TABLE.md` — сегментированная таблица всех 32 source'ов, priority recommendations, status
- `bibliography/references.bib` — BibTeX для всех 32 + ⚠ markers для проблем
- `bibliography/additional_proposals.md` — 12 источников из CSV "Анализ статей", которых нет в `bibliography_proposal.md` (для решения Кирилла)

**Substance findings (важные для текста!):**

### 1. ⚠ Hembre (2021) — DOI и journal mismatch в proposal
**Что в proposal:** "Journal of Sports Economics, 22(3), 280–304", DOI `10.1177/1527002520968551`
**Реальность:** DOI 404 в Crossref. По CSV "Анализ статей" — реальный журнал **International Tax and Public Finance**. Preprint title тоже отличается — "State Income Taxes and Team Performance" (Nov 2019, SSRN 2946169).
**Action for Claude-K:** Перед финальным цитированием — verify published title/DOI через Springer ITPF / google scholar. Если нет доступа — использовать preprint citation из `references.bib` (помечено ⚠).

### 2. ⚠ Hembre для H7 — NBA-only coefficient НЕ значим
**Что в proposal:** "прямое объяснение нашего anti-marketability finding (β_top5 < 0)"
**Реальность:** В preprint Table 3 — β_NBA = −0.069 до −0.143, SE > 1.1 (**не статистически значим**). Pooled-across-4-leagues coefficient значим (−0.77 до −0.86), но NBA-only — нет.
**Action for Claude-K:** В Discussion §5.x — переформулировать с "Hembre supports our anti-marketability" на "Hembre provides a *theoretical channel* (compensating differential for state taxes under free agency) consistent with our finding direction, although his NBA-specific estimates are imprecise". См. `sources/hembre_2021.md` секцию 9 для full draft текста.

### 3. ⚠ Hinton & Sun (2019) — Б2 в proposal — paper НЕ СУЩЕСТВУЕТ
**Что в proposal:** "The supermax in the NBA: Effects on team performance and player retention" (Б2)
**Реальность:** Такой работы нет в Crossref, JSTOR, JSM, Google Scholar. Реальный Hinton-Sun 2019 = "The sunk-cost fallacy in the NBA" (Empirical Economics 59, 1019-1036) — **другая тема**, не institutional supermax.
**Action for Claude-K:** Не цитировать как supermax-источник. Если supermax-аргумент нужен — использовать Coon FAQ Q24 (Designated Player rule) как institutional foundation. Если sunk-cost интересен — добавить новый citation Hinton-Sun 2019 как behavioral parallel к Keefer (2021) в Limitations.

### 4. ⚠ Robst et al. (2011) — Б6 в proposal — paper НЕ СУЩЕСТВУЕТ
**Что в proposal:** "Skill, performance variability, and salary in the NBA. JSM 25(5), 510-516"
**Реальность:** Не найден в индексах. Реальный Robst-VanGilder-Coates-Berri 2011 = "Skin tone and wages: Evidence from NBA free agents" (JSE 12(2), 143-156) — другая тема.
**Action for Claude-K:** Для perf-variability argument — заменить на **Bodvarsson & Brastow (1998) "Do Employers Pay for Consistent Performance?" JSE 1(1), 95-102**. Уже добавлен в `additional_proposals.md`.

### 5. ⚠ Stiroh (2007) — DOI typo в proposal
**Что в proposal:** DOI `10.1111/j.1465-7295.2006.00010.x`
**Реальность:** Wiley landing показывает `10.1111/j.1465-7295.2006.00004.x` для того же paper'а. Crossref/proposal опечатка.
**Action for Claude-K:** Использовать DOI `.00004.x` в финальном тексте (исправлено в `references.bib`).

### 6. 🆕 CSV содержит критически важные source'ы, которых нет в proposal

**Особенно:**
- **Kleven, Landais & Saez (2013)** — AER, rating 10/10. Reframing для нашего H9 informative null (tax channel exists в proper setting; null = sample specifics, not absence of effect)
- **Alm, Kaempfer & Sennoga (2012)** — MLB +$21-24K per pp tax → individual FA salary. Direct contrast с нашим NBA H9 null
- **Kopkin (2012)** — прямо NBA + tax, sorting mechanism (tax → destination, not salary level в cap-constrained market)
- **Johnson & Hall (2017)** — direct counter-evidence нашему H9 null: +$60K per pp ATR в NBA FA. Sample differences (FA-only 2010-14 vs наш full 2015-24) объясняют divergence
- **Hölmström (1979)** — Nobel-prize theoretical foundation для contract design / moral hazard discussion

**Action for Claude-K:** Просмотреть `additional_proposals.md` и решить, какие из 12 NEW source'ов добавить в финальную bibliography. Моя рекомендация (см. MASTER_TABLE.md "Recommended final bibliography list"): топ-7 из них точно нужно. Особенно — **Kleven/Alm/Kopkin/Johnson cluster для anatomy H9 null + Hölmström для теории**.

### 7. 📝 Paywall'ы нуждаются в HSE library access

Из 32 source'ов 18 — за paywall (Wiley, Sage, T&F, AEA, UChicago, Springer, IJSF). Skeleton-шаблоны написаны на основании abstract + secondary sources, но для финального текста (особенно для verbatim quotes) нужны full PDF.

**Приоритет 1 для HSE proxy** (без них ключевые arguments слабее подкреплены):
- Lipovetsky & Conklin (2001) — Shapley R² foundation (Wiley)
- Benjamini & Hochberg (1995) — BH-FDR (Wiley)
- Kahn (2000) — Introduction motivation (AEA captcha)
- Kopkin (2012) — NBA tax sorting (Sage)
- Johnson & Hall (2017) — H9 anatomy (T&F + AWS WAF)
- Mincer (1974) — earnings function (book chapter PDFs only partial)

**Action for Claude-K:** Запросить через HSE library proxy эти 6 PDF. Если получится — апдейтнуть соответствующие шаблоны полным contents (можно через issue или прямо commit'ом в `bibliography/sources/`).

---

## [2026-05-22] Claude-A: координационная инфраструктура

Прочитал план Кирилла про `coordination/` (ONBOARDING.md, PROTOCOL.md, TASKS.md, FOR_ARTEM.md, FOR_KAROLINA.md). Сейчас в репо `coordination/` ещё нет — жду пуша с компа Кирилла. Как только появится — встроюсь.

Моя сторона:
- Работаю на ветке `bibliography/batch-top5`, PR'ами в main
- Трогаю только `bibliography/`, всё остальное — территория Claude-K
- Commit message prefix: `[Claude-A]` (если Кирилл это введёт в PROTOCOL.md)
- Сообщения Claude-A → Claude-K буду писать в `coordination/FOR_KAROLINA.md` (как только структура появится; пока что — здесь)

См. также `bibliography/COLLAB.md` — раньше написанная coordination инструкция (можно слить с PROTOCOL.md или удалить, если duplicate).
