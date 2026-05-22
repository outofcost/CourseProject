# Master bibliography table — 32 sources

Сводная сегментированная таблица всех найденных и обработанных источников. Группировка: 5 категорий из `bibliography_proposal.md` (A, Б, В, Г, Д) + категория **NEW** (12 источников из `Промпт 1/Анализ статей - Лист1 (6).csv`, которых не было в proposal).

**Status легенда:**
- ✅ Full — PDF в `pdfs/` + полностью заполненный шаблон в `sources/`
- 📝 Skeleton — шаблон есть, PDF за paywall (заполнено на основании abstract + secondary sources)
- 🌐 Web — web reference, snapshot в `pdfs/`

**Recommended priority для финальных ~25-30 references (HSE 3rd-year norm):**
- ⭐⭐⭐ ВЫСШИЙ — without it ключевой аргумент не подкрепить
- ⭐⭐ СРЕДНИЙ — strengthens Lit Review stream, рекомендуется
- ⭐ НИЗКИЙ — nice-to-have, для context only
- ❌ SKIP — рекомендация выкинуть из финальной библиографии (либо не подкрепляет наши H, либо topic mismatch)

---

## Категория А — Методы (5 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| A1 | Cameron, Gelbach & Miller (2011) | JBES 29(2) | ✅ Full | All H (SE methodology) | ⭐⭐⭐ | Cluster-robust SE foundation для всех regressions |
| A2 | Lipovetsky & Conklin (2001) | ASMBI 17(4) | 📝 Skeleton (Wiley paywall) | All H (Shapley R²) | ⭐⭐⭐ | Foundation для главного методологического вклада |
| A3 | Oster (2019) | JBES 37(2) | ✅ Full | Robustness all H | ⭐⭐ | δ-sensitivity для OVB; используется в M_full Oster analysis |
| A4 | Benjamini & Hochberg (1995) | JRSS-B 57(1) | 📝 Skeleton (Wiley paywall) | All H (multiple testing) | ⭐⭐⭐ | BH-FDR для 10 hypotheses, headline 7/10 pass |
| A5 | MacKinnon & Webb (2018) | Econometrics J 21(2) | ✅ Full | H7 (interactions) | ⭐⭐ | Wild-cluster bootstrap для H7 top5×allstar interaction |

---

## Категория Б — NBA / sport-specific (6 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| Б1 | Hembre (2021) | International Tax & Public Finance ⚠ | ✅ Full (preprint) | H7, H9 | ⭐⭐⭐ | **⚠ Title/journal mismatch в proposal**: реальный journal — ITPF, не JSE. Preprint Nov 2019 "State Income Taxes and Team Performance". NBA-only coefficient не значим — caveat для H7. |
| Б2 | Hinton & Sun (2019) | Empirical Economics 59 | 📝 Skeleton | (sunk-cost, not supermax) | ❌ | **⚠ TOPIC MISMATCH**: указанный в proposal "supermax" paper НЕ СУЩЕСТВУЕТ. Найденный paper — "Sunk-cost fallacy in NBA" — другая тема. Не подкрепляет H3. Skip; см. Keefer 2021 (sunk-cost) или Coon FAQ (institutional). |
| Б3 | Stiroh (2007) | Economic Inquiry 45(1) | 📝 Skeleton (Wiley paywall) | H6 (dynamics), Limitations | ⭐⭐ | Classic contract-year effect. **⚠ DOI variant в proposal** — проверить. |
| Б4 | Berri, Brook & Schmidt (2007) | IJSF 2(4) | 📝 Skeleton (IJSF paywall) | H1 (perf criticism) | ⭐⭐ | "Score-only" critique; motivates наш inclusion WS/BPM в Performance block |
| Б5 | Yang & Lin (2012) | JSE 13(1) | 📝 Skeleton (Sage paywall) | Demographics block | ⭐⭐ | Foundation для continent dummies в INTL_BLOCK |
| Б6 | Robst, VanGilder, Coates & Berri (2011) | (mismatch) | 📝 Skeleton | (skin tone, not perf-var) | ❌ | **⚠ TITLE MISMATCH**: указанный paper НЕ СУЩЕСТВУЕТ. Реальный Robst-VanGilder-Coates-Berri 2011 = "Skin tone and wages" (JSE 12(2)). Skip; для perf-variability argument — Bodvarsson & Brastow (1998) "Do Employers Pay for Consistent Performance?" JSE 1(2) как замена. |

---

## Категория В — Классика labor economics (4 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| В1 | Rosen (1981) | AER 71(5) | ✅ Full | H1 (Mincer foundation), H5/H6 | ⭐⭐⭐ | Superstars — theoretical anchor для tail-concentration |
| В2 | Mincer (1974) | NBER book | 📝 Skeleton (only ToC PDF) | H1, H2 | ⭐⭐⭐ | Mincer earnings function — primary citation для baseline spec. **Альтернатива**: Lemieux (2006) "Mincer Equation 30 years after" (JEL) — review с full text. |
| В3 | Lazear & Rosen (1981) | JPE 89(5) | ✅ Full (NBER WP) | H5, H6 | ⭐⭐⭐ | Tournament theory — foundation для awards channel |
| В4 | Rottenberg (1956) | JPE 64(3) | 📝 Skeleton (JSTOR paywall, 1956) | None directly | ⭐ | Classic antecedent для всей литературы sports labor markets; цитируется в Introduction для historical context |

---

## Категория Г — NBA empirics классика (4 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| Г1 | Hausman & Leonard (1997) | JLE 15(4) | ✅ Full (MIT DSpace WP) | H5 (superstar value) | ⭐⭐⭐ | Первое квантитативное доказательство superstar economic externality в NBA |
| Г2 | Krautmann (1999) | Economic Inquiry 37(2) | 📝 Skeleton (Wiley paywall) | Limitations (MRP) | ⭐⭐ | Methodological critique Scully-estimates — для Limitations §6.x |
| Г3 | Hill & Groothuis (2001) | JSE 2(2) | 📝 Skeleton (Sage paywall) | H3, H4 | ⭐⭐ | Analysis structural effects CBA on salary distribution |
| Г4 | Kahn (2000) | JEP 14(3) | 📝 Skeleton (AEA captcha) | Introduction motivation | ⭐⭐⭐ | "Sports as labor market lab" — нужен для Introduction (мотивация выбора NBA). Open access формально, но curl blocked — нужен HSE proxy. |

---

## Категория Д — Institutional reference (1 source)

| # | Author (year) | Source | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| Д1 | Coon, L. (n.d.) | cbafaq.com (CBA 2017 ed.) | 🌐 Web snapshot | H3, H4 (institutional layer) | ⭐⭐⭐ | Институциональный foundation для классификатора tier, supermax eligibility, Bird rights. **⚠ Larry Coon retired May 2025** — snapshot saved locally. |

---

## Категория NEW — добавления из CSV "Анализ статей" (12 sources)

Эти статьи **не в** `bibliography_proposal.md`, но найдены в `Промпт 1/Анализ статей - Лист1 (6).csv` с rating'ом / описанием. Рекомендация Артема — выбрать ~5-7 из них для финальной библиографии.

### Tax / market cluster (5 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| N1 | **Kleven, Landais & Saez (2013)** | AER 103(5) | ✅ Full | H7, H9 framing | ⭐⭐⭐ | Top-1 journal, ε_foreign ≈ 1.0. **Critical** для framing нашего H9 informative null (tax channel exists in right setting; наш null = sample specifics, not absence of effect). |
| N2 | Alm, Kaempfer & Sennoga (2012) | Tulane WP 1209 / JSE 13(6) | ✅ Full | H9 contrast | ⭐⭐⭐ | MLB +$21-24K/pp tax → individual FA salary. Direct contrast с нашим NBA H9 null. |
| N3 | Kopkin (2012) | JSE 13(6) | 📝 Skeleton (Sage paywall) | H7, H9 (sorting) | ⭐⭐⭐ | Прямо NBA + tax. Sorting mechanism (tax → destination, not salary level в cap-constrained market). |
| N4 | Johnson & Hall (2017) | Applied Economics Letters | 📝 Skeleton (T&F + AWS WAF) | H9 anti-null | ⭐⭐⭐ | Direct counter-evidence нашему H9 null: +$60K/pp ATR в NBA FA. Sample differences (FA-only 2010-14 vs наш full 2015-24) объясняют divergence. |
| N5 | Kahn & Sherer (1988) | JLE 6(1) | 📝 Skeleton (UChicago paywall) | (race, not H1-H10) | ⭐ | Classical NBA discrimination; включать только если в Lit Review есть параграф про historical evolution NBA literature. Otherwise skip. |

### Contract year / shirking / incentives cluster (5 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| N6 | White & Sheldon (2014) | Motivation and Emotion 38 | ✅ Full | Limitations (CY effect) | ⭐⭐ | NBA + MLB contract year effect, SDT framing |
| N7 | Keefer (2021) | Empirical Economics | ✅ Full | Limitations (sunk-cost) | ⭐⭐ | DiD + IV с salary cap shock 2016/17, методологически сильнейшая |
| N8 | Krautmann & Donley (2009) | JSE 10(3) | 📝 Skeleton (Sage paywall) | Limitations | ⭐ | MLB shirking analog; для cross-sport contrast |
| N9 | Berri & Krautmann (2006) | Economic Inquiry | 📝 Skeleton (Wiley paywall) | Limitations (NBA shirking) | ⭐⭐ | Первая NBA shirking work; relevant для Limitations §6.x |
| N10 | Conklin & Daniel (2023) | SSRN WP 4474724 | 📝 Skeleton (SSRN) | None | ❌ | Working paper, simple t-test, methodologically weak. Skip. |

### Theory / inequality cluster (2 sources)

| # | Author (year) | Journal | Status | H-mapping | Priority | Notes |
|---|---|---|---|---|---|---|
| N11 | **Hölmström (1979)** | Bell J. Econ 10(1) | ✅ Full (gwern.net) | Theory foundation | ⭐⭐⭐ | Moral hazard theory — Nobel-prize-winning. Foundation для contract design discussion в Lit Review §2.x |
| N12 | Simmons & Berri (2011) | Labour Economics | 📝 Skeleton | None directly | ⭐ | NBA salary inequality and performance; nice-to-have для Discussion |

---

## Сводка прогресса

| Status | Количество | Доля |
|---|---|---|
| ✅ Full PDF + template | 13 | 41% |
| 📝 Skeleton (paywall) | 18 | 56% |
| 🌐 Web snapshot | 1 | 3% |
| **Total** | **32** | **100%** |

**Paywall категории, нуждающиеся в HSE library access:**
- Wiley (5): Lipovetsky-Conklin 2001, Benjamini-Hochberg 1995, Stiroh 2007, Krautmann 1999, Berri-Krautmann 2006
- Sage (5): Hill-Groothuis 2001, Yang-Lin 2012, Kopkin 2012, Krautmann-Donley 2009, Hinton-Sun 2019
- T&F (1): Johnson-Hall 2017
- AEA (1): Kahn 2000 (formally OA, technical block)
- UChicago Press (1): Kahn-Sherer 1988, Rottenberg 1956
- Springer (1): Hinton-Sun 2019 (если включаем)
- IJSF (1): Berri-Brook-Schmidt 2007
- Tulane Press / JSM (0)

**Action item для Karolina:** через HSE proxy получить PDF приоритета ⭐⭐⭐ из skeleton'ов: Lipovetsky-Conklin 2001, Benjamini-Hochberg 1995, Kahn 2000, Kopkin 2012, Johnson-Hall 2017, Mincer 1974 (full book).

---

## Recommended final bibliography list (~28 references)

Приоритет ⭐⭐⭐ + ⭐⭐ + Coon = baseline для финального текста. Топ-30 cut:

**Methods (5):**
1. Cameron, Gelbach & Miller (2011) — cluster SE
2. Lipovetsky & Conklin (2001) — Shapley R²
3. Oster (2019) — δ-sensitivity
4. Benjamini & Hochberg (1995) — BH-FDR
5. MacKinnon & Webb (2018) — wild-cluster bootstrap

**Classical labor (4):**
6. Rosen, S. (1981) — Superstars
7. Mincer (1974) — earnings function
8. Lazear & Rosen (1981) — tournaments
9. Hölmström (1979) — moral hazard theory [NEW from CSV]

**NBA empirics (3):**
10. Hausman & Leonard (1997) — superstar externality
11. Hill & Groothuis (2001) — CBA structural
12. Kahn (2000) — sports as labor lab

**NBA / sport empirics specific (5):**
13. Hembre (2021) — tax/team performance
14. Stiroh (2007) — contract year
15. Berri, Brook & Schmidt (2007) — score critique
16. Yang & Lin (2012) — nationality discrimination
17. Krautmann (1999) — MRP methodology

**Tax cluster (3 from NEW):**
18. Kleven, Landais & Saez (2013) — superstar mobility
19. Alm, Kaempfer & Sennoga (2012) — MLB tax
20. Kopkin (2012) — NBA tax sorting
21. Johnson & Hall (2017) — NBA FA tax salary

**Shirking / contract year (2 from NEW):**
22. Keefer (2021) — sunk cost cap shock
23. Berri & Krautmann (2006) — NBA shirking

**Institutional (1):**
24. Coon, L. (n.d.) — CBA FAQ

**Optional / context (4):**
25. Rottenberg (1956) — historical anchor
26. White & Sheldon (2014) — CY psychology
27. Simmons & Berri (2011) — inequality
28. Robst-VanGilder-Coates-Berri (2011) — **REPLACE WITH** Bodvarsson & Brastow (1998)

**SKIP (4):**
- Hinton & Sun (2019) — topic mismatch
- Robst et al. (2011) per proposal — does not exist
- Kahn & Sherer (1988) — only if no discrimination section
- Conklin & Daniel (2023) — methodologically weak

**Final count:** 28 references (close to HSE 25-30 norm). Если Karolina хочет уменьшить — выкинуть в первую очередь optional (25-28).

---

**Обновлено:** 2026-05-22
**Автор:** Artem (collaborator)
