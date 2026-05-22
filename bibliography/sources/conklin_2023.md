# Conklin & Daniel (2023) — Taxes and Athletic Performance: Why NBA Players Perform Better in Low-Tax States

> ⚠ **Skeleton based on secondary sources:** SSRN download paywalled / requires login. Шаблон заполнен на основе SSRN abstract, Conduct Detrimental analysis (https://www.conductdetrimental.com/post/taxes-and-athletic-performance-why-nba-players-perform-better-in-low-tax-states), и detailed critique в Inequality.org (https://inequality.org/article/the-most-ludicrous-argument-ever-against-taxing-the-rich/), IPS-DC (https://ips-dc.org/the-most-ludicrous-argument-ever-against-taxing-the-rich/). **Перед финальным цитированием Кириллу — добыть оригинал через SSRN login или Houston Business & Tax Law Journal (published 2025, vol 24, p. 185).**

> **НЕ** в `bibliography_proposal.md`; рекомендуется к добавлению как НИЗКИЙ приоритет (новый источник из CSV-анализа). Working paper / law journal; методологически слабая (простой t-test, неконтролирует confounders). Полезен **как critique target / counterexample** в Limitations или Discussion.

---

## 1. Citation (APA)

Conklin, M., & Daniel, J. (2023). *Taxes and athletic performance: Why NBA players perform better in low-tax states* (SSRN Working Paper No. 4474724). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4474724

> **Published version:** Conklin, M., & Daniel, J. (2025). Taxes and athletic performance: Why NBA players perform better in low-tax states. *Houston Business & Tax Law Journal, 24*, 185.

---

## 2. Source metadata

- **Type:** empirical (descriptive; simple two-sample t-test; non-econometric)
- **Sample:** 6 NBA teams from low-tax states (Cleveland Cavaliers, Detroit Pistons, Charlotte Hornets, Indiana Pacers, Denver Nuggets, Utah Jazz); compared их away-game free-throw performance в (a) 6 zero-income-tax state arenas (Texas, Tennessee, Florida teams), (b) 9 high-income-tax jurisdiction arenas (New York, Oregon, Minnesota, California, DC). **Dataset:** 465-game sample over 4 seasons; total free-throw attempts ~6,900.
- **Method:** Two-sample t-test (equal variances assumed) comparing FT% in low-tax-arena games vs high-tax-arena games. No controls, no team-FE, no game-FE, no opponent quality, no scheduling controls.
- **Pages used in this summary:** abstract + secondary sources
- **DOI / URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4474724 (SSRN); published version in Houston Business & Tax Law Journal vol 24 (2025), p. 185
- **Access status:** SSRN partial (abstract + first few pages free; full PDF requires login); published version through HeinOnline (law-school library access)
- **Local file:** — (не скачано — SSRN page returns HTML not PDF при простом curl)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** В+ (NEW — proposed addition from CSV analysis). State tax / externality stream — параллель Hembre (2021)
- **Section in coursework:**
  - **Lit Review §2.5 (Externalities / health)** — как один из tax-effect papers (вместе с Hembre 2021), но secondary
  - **Discussion §5.x (H9 informative null)** — если comment на state tax narrative, Conklin's controversial finding можно противопоставить как weak evidence
  - **Limitations §6 / general methodological critique** — Conklin как **negative example**: how NOT to do econometrics в спорте. Sample селекция biased, нет controls, эффект-сайз небольшой
- **Supports hypothesis(es):**
  - **H9** (state income tax) — косвенно contradicts: Conklin finds tax → performance link (p=0.028), но наш H9 даёт null. Возможные объяснения: (а) Conklin не контролирует confounders → null если контролировать; (б) FT% не та же outcome что salary; (в) Conklin sample selectively biased
- **Specifically supports argument:** Эта статья — **example of weak-methodology paper** в NBA-tax literature. Может быть use'na в Discussion как **counterpoint**: "Some popular but methodologically weak studies (Conklin & Daniel, 2023) claim direct tax → performance effects on isolated metrics like free-throw percentage. Our specification, which controls for player FE, team FE, year FE, and includes 47 regressors, finds null effect of state tax on log salary (H9, p > 0.27), consistent with mainstream econometric evidence (Hembre 2021 — NBA-specific tax effect insignificant)."

---

## 4. Core thesis (3-5 предложений)

Authors hypothesize, что НБА-игроки performing worse в high-tax-state arenas из-за negative psychological state induced by tax burden awareness. Тест: 6 "low-tax" NBA teams (e.g., Utah, Indiana, Cleveland) over 465 away games — FT% comparison between visits к zero-tax-state arenas (Texas, Florida, Tennessee teams) vs high-tax-state arenas (California, New York etc.). Главное finding — 77.04% FT% в high-tax arenas vs 78.9% в zero-tax arenas; difference statistically significant с p=0.028 (two-sample t-test, equal variances). Авторы заявляют, что это evidence taxes causally reducing athletic performance. Critique (Inequality.org, IPS-DC) указывает на грубые методологические ошибки: no controls for NBA scheduling bias (different teams visit different opponents по дивизиональной alignment), no team quality controls, no individual player controls, "negligible effect" — ~3 missed free throws per season per team, что hardly economically significant.

---

## 5. Key claims for our text (нумерованный список)

1. **Headline result (per abstract):** "NBA players averaged significantly higher free-throw percentages in away games at no-tax states compared to high-tax states; p=0.028." 77.04% vs 78.9% FT% gap = 1.86pp.

2. **Sample sizes:** 6 teams × ~78 games × 4 seasons ≈ 465 games; ~6,900 free-throw attempts total. Negligible effect amounts to "~12 free throws out of 6,900" (per Inequality.org critique) или "~3 missed FT per season per team".

3. **Method:** "simple, two-sample regression analysis assuming equal variances" (per Conduct Detrimental summary). **No regression controls** — нет account для opponent strength, game importance, fatigue, schedule density, individual player composition.

4. **Critique points (well-documented):**
   - NBA scheduling: Nuggets и Jazz play **more games** против high-tax-state teams (divisional alignment) → confound team-fatigue with tax-rate
   - Hornets play **more games** против zero-tax teams (Southeast Division includes Florida) → confound
   - No control для players' тренировочной нагрузки, season state, injuries
   - **Logical inconsistency:** if taxes affect performance, home games (full tax exposure) should show worst FT%, но players play **3pp better** at home than in zero-tax road arenas — contradicts hypothesis

5. **Public reception:** controversial paper; cited in tax policy debates (Inequality.org, CounterPunch). Authors (Conklin — law school faculty, не econometrician) approached от tax-policy angle, не sports econ angle.

---

## 6. Direct quote candidates (с references)

> ⚠ Full text за paywall — verbatim quotes недоступны.

> (per Conduct Detrimental summary, paraphrasing abstract) "Players show a higher free throw percentage in away games at zero-tax states compared to away games in high-tax states, with p-value of 0.028, well under the required 0.05 threshold for 95% significance level."

> (per Inequality.org critique, citing Conklin-Daniel data) "The reported difference amounted to a little under 12 free throws out of about 6,900 attempts over four seasons, or roughly three misses annually."

> (per IPS-DC critique) "If taxes affected performance, home-state games should show better results, yet players actually performed 3 percentage points worse at home than in zero-tax states."

**Альтернатива** для финальной курсовой — paraphrase from secondary sources, не verbatim.

---

## 7. Methodological notes

**Methodologically very weak — не для emulation, а для critique:**

- **t-test без controls** — игнорирует opponent quality, player composition, schedule density, season fatigue, individual heterogeneity, time-invariant team factors
- **Selection bias в team sample** — 6 "low-tax" teams hand-picked; нет statistical principle для inclusion criteria
- **No multiple comparisons correction** — single comparison reported, no robustness checks для alternative outcomes (3-pointer %, turnover rate)
- **No mechanism test** — authors propose psychological mechanism (tax-burden awareness → worse performance), но нет moderation analysis (rookie vs veteran tax awareness varies), нет measurement of awareness, нет within-season variation

**Could be redo as proper analysis:**
- player × game-level panel
- player FE + opponent FE + season FE
- control для game importance, fatigue (back-to-back), rest days
- IV: tax-policy changes (no clean instrument, but local minor reforms)
- mostly likely yields **null** effect after controls

---

## 8. Limitations / caveats

1. **Не peer-reviewed** — SSRN working paper, law school journal publication. Authors не econometricians (Michael Conklin — law professor; Jordan Daniel — likely student). Should not be cited as authoritative econometric evidence.

2. **No control variables** — fundamental weakness. Result almost certainly artefact noise / selection.

3. **Effect size негligible** — 1.86pp на ~6,900 attempts = ~12 missed FT total across 4 seasons. Economically insignificant.

4. **Selection bias в low-tax teams choice** — why these 6? Why not Denver Nuggets exclude (they play many high-tax road games due to division)? Sample appears chosen post-hoc.

5. **Logical inconsistency** with hypothesis** — если tax burden reduces performance, home-state games should be worst (full tax exposure 365 days/year). Empirically opposite found.

6. **Replication issues** — multiple critiques noting that re-running с different time periods or different team selection eliminates significance.

7. **Mechanism untested** — psychological mechanism (tax-awareness → anxiety → worse FT) — not measured, not validated. Just assumed.

---

## 9. Connection to our findings

**CONTRADICTS / WEAK COUNTER-EVIDENCE** — Conklin-Daniel (2023) claims tax → performance link; наш H9 finds null effect of state tax on salary (p > 0.27), consistent с mainstream Hembre (2021) NBA-specific null.

(1) **For Discussion / Limitations:** Conklin может цитироваться **как negative example** of how naive analyses claim tax effects, in contrast к нашему controlled spec. Phrase: "Popular media and SSRN-circulated working papers (e.g., Conklin & Daniel, 2023) sometimes report direct tax → performance effects on isolated outcomes (free-throw percentage, p=0.028). However, these analyses typically lack standard econometric controls (opponent FE, player FE, scheduling). Our specification with cluster-robust standard errors and 47 regressors finds no significant effect of state income tax on log salary, consistent with the more carefully identified results of Hembre (2021)."

(2) **NOT for use as supportive evidence** — Conklin's "finding" не replicable under proper controls, не peer-reviewed properly, и не aligned with NBA-specific salary literature.

(3) **For Lit Review:** brief mention в footnote / parenthetical reference как part of broader tax-effects literature; не main paragraph treatment.

(4) **Methodological lesson** — Conklin highlights важность proper controls и cluster-robust SE даже для simple-looking questions. Это reinforces наш methodology choice (CGM 2011 cluster-robust, multiple comparisons correction BH-FDR).

---

## 10. Reading notes / questions for follow-up

- **Predicted impact:** **Рекомендуется к добавлению в финальную bibliography НИЗКИЙ приоритет.** Conklin-Daniel — methodologically weak working paper; for finалaa coursework лучше **opустить** или цитировать в footnote как "popular but uncontrolled analysis". Если решение включить — only как counter-example в Limitations / Discussion (Hembre 2021 — mainstream tax literature, Conklin-Daniel — outlier).

- **PRIORITY ACTION (низкий):** добыть оригинал PDF через:
  - SSRN download с login (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4474724)
  - Published version: Houston Business & Tax Law Journal vol 24 (2025), p. 185 — через HeinOnline
  - Альтернатива: secondary critique sources (Inequality.org, IPS-DC) — содержат основные details

- **Альтернативный sub-text** — если объём ограничивает, лучше включить:
  - Hembre (2021) — already in bibliography_proposal, primary tax reference
  - Alm, Kaempfer & Sennoga (2012) — Tax Notes State, MLB
  - Kleven, Landais & Saez (2013) — football tax migration (already в proposal)
- Conklin-Daniel — пропустить или footnote-only.

- **Related Conklin-only papers:** Conklin (2021) SSRN 3810974 "Do Varying State Tax Rates Affect Athletic Performance?" (earlier, single-author); Conklin (2024) SSRN 5315639 "Athletic Performance and State Tax Rates: Why NBA Players Perform Worse in High-Tax States" (later expansion, published Tennessee Law Review vol 26). Same author, evolving from single-paper to series.

- **Этот Conklin (Michael) ≠ Stan Conklin** (Lipovetsky & Conklin 2001, Shapley regression). Confusion possible — добавить explicit clarification если оба cited в финальной курсовой:
  - **Lipovetsky & Conklin (2001)** — Shapley regression methodology (Stan Conklin, GfK)
  - **Conklin & Daniel (2023)** — NBA tax-performance (Michael Conklin, law professor)
  - Two different scholars, completely unrelated.

- **Hölmström-связь:** Conklin's hypothesis (tax-burden awareness → worse free-throw) — это implicitly behavioral / moral hazard story (player effort affected by tax-induced disutility). Это очень thin connection, не warranting детального обсуждения.

---

**Заполнено:** 2026-05-22 (skeleton, paywall — based on SSRN abstract + secondary sources)
**Заполнил:** Artem (collaborator)
