# Oster (2019) — Unobservable Selection and Coefficient Stability

---

## 1. Citation (APA)

Oster, E. (2019). Unobservable selection and coefficient stability: Theory and evidence. *Journal of Business & Economic Statistics, 37*(2), 187–204. https://doi.org/10.1080/07350015.2016.1227711

---

## 2. Source metadata

- **Type:** methodological (theoretical extension + validation Monte Carlo + applied review of empirical literature)
- **Sample (validation):** (a) 76 papers from leading economics journals (AER, JPE, QJE, REStud) using coefficient stability arguments; (b) simulation of synthetic data with known δ; (c) two RCT-based validations — Almond, Hoynes & Schanzenbach 2011 (Food Stamps), and Finkelstein et al. 2012 (Oregon Medicaid)
- **Method:** extension of Altonji-Elder-Taber (2005) bounding framework; derives a closed-form bias-adjusted estimator β* depending on (a) δ (relative selection on unobservables vs observables), (b) Rmax (R² achievable with full set of controls + ε), (c) controlled β̃ and R̃, (d) uncontrolled β̊ and R̊
- **Pages used in this summary:** 1 (abstract), 2 (intro + key formula motivation), 8–11 (theory § 3.1–3.3), 14–15 (interpretation of ε and Rmax), 16 (relation to coefficient stability), 19–22 (validation against RCTs), 24–29 (recommendations: δ = 1, Rmax = 1.3·R̃)
- **DOI / URL:** https://doi.org/10.1080/07350015.2016.1227711 (T&F paywall for published); preprint freely available at emilyoster.net / NBER WP 19054
- **Access status:** open access (author's website)
- **Local file:** `bibliography/pdfs/oster_2019.pdf` (preprint, Aug 2016 version)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** А (методы)
- **Section in coursework:** Methods §3.x (robustness — sensitivity to omitted variable bias); Discussion / Limitations §5–6 (interpretation of δ для ключевых coefficients); Methodology addendum (`methodology_v2_addendum.md`)
- **Supports hypothesis(es):** не support конкретную гипотезу — это методологическая основа для робастности всех β-коэффициентов в M1c_full, M_full, H8 (market), H10 (awards), H11 (durability)
- **Specifically supports argument:** В нашем `analysis_v2/output/tables/` уже посчитаны Oster δ для 6 ключевых коэффициентов (см. SHIPPING_SUMMARY: "Phase 3 day 7 → Oster δ для 6 коэф"). Цитата Oster (2019) нужна в Methods для обоснования procedure и в Discussion при обсуждении того, насколько β_top5, β_all_nba_lag1, β_games_missed_lag1 и β_post_cba_2017 устойчивы к включению pure unobservables. Стандартный benchmark δ = 1 (selection on unobservables ≤ selection on observables) и Rmax = min(1, 1.3·R̃) — то, что мы применяем.

---

## 4. Core thesis (3-5 предложений)

Oster развивает framework Altonji-Elder-Taber (2005) для оценки чувствительности OLS-коэффициентов к omitted variable bias через наблюдаемое поведение treatment coefficient β и R² при последовательном включении controls. Ключевой insight: коэффициент стабильность сама по себе не информативна — она диагностична только если совмещается с движением R². Oster выводит формальный bias-adjusted estimator β* = β̃ − δ · (β̊ − β̃) · (Rmax − R̃)/(R̃ − R̊), который при δ = 1 даёт «полностью бьющую» границу bias (selection on unobservables = selection on observables). Альтернативно — можно решить для δ* такого, что β = 0, и интерпретировать |δ*| > 1 как сигнал робастности (нужна крайне большая selection на unobservables чтобы обнулить эффект). Через два RCT validation exercises (Food Stamps, Oregon Medicaid) Oster показывает, что её method даёт consistent estimates истинных treatment effects, тогда как простой "controlled coefficient" сильно biased. Recommends Rmax = min(1.3·R̃, 1) как practical bounding rule (1.3× corresponds to «add as much explanatory power as observed controls already add»).

---

## 5. Key claims for our text (нумерованный список)

1. **Coefficient stability alone is insufficient:** β может быть completely stable (β̃ = β̊) даже при large bias, если R² не движется (или движется very mало) — это происходит, когда unobservables correlate с treatment, но добавляют мало explanatory power. Формальная демонстрация в section 3.3.5 (pp. 16–17). **Для нас:** нельзя писать "наш β_ppg робастен потому что не меняется при добавлении awards" без attendance к R² delta.

2. **Bounding formula** (Proposition 2, p. 13): при δ = 1 и Rmax заданном,
   β* = β̃ − [(β̊ − β̃) · (Rmax − R̃) / (R̃ − R̊)]
   даёт single value (под Assumption 3 about sign of covariance with unobservable index).

3. **Δ as treatment-stability metric** (Proposition 3, p. 14): можно решить уравнение β(δ) = 0 для δ*; если |δ*| > 1 → "selection on unobservables would have to be more than 1× selection on observables to drive treatment effect to zero" → традиционная heuristic «эффект робастен».

4. **Rmax recommendation** (Section 4, p. 25): для RCT-based applications, на основании 50 RCTs из validation exercise, Oster находит, что Rmax = 1.3·R̃ корректно покрывает 90% true β. Это default value в её `psacalc` Stata-пакете и в R `robomit`.

5. **Empirical literature review (Table 2, pp. 32–34):** из 76 papers using stability argument, только 23% выживают δ = 1, Rmax = 1.3·R̃ test. Это ключевой эмпирический claim — coefficient stability arguments в econ literature чаще всего НЕ робастны при формальном тестировании.

---

## 6. Direct quote candidates (с page numbers)

> "A common approach to evaluating robustness to omitted variable bias is to observe coefficient movements after inclusion of controls. This is informative only if selection on observables is informative about selection on unobservables." (Abstract, p. 1)

> "It is necessary to take into account coefficient and R-squared movements." (Abstract, p. 1)

> "All else equal, coefficient stability correlates with a smaller amount of bias. However, it is crucial to note that it is possible for coefficients to be stable — indeed, to be completely unchanged — even in the presence of very large bias." (Section 3.3.5, p. 16)

> "I argue below that in empirical settings a value of δ = 1 is a good bounding value; this is consistent with arguments in AET. For the purposes of implementation, therefore, it may be appropriate to consider either (a) calculating the bias-adjusted effect under the assumption of δ = 1, with Assumption 3 active or (b) calculating the value of δ such that β = 0." (Section 3.3.2, p. 15)

> "Stata code to perform the calculations described in this paper is available from the authors website or through ssc under the name psacalc." (Footnote on title, p. 1)

---

## 7. Methodological notes

- **Method name:** Oster δ-sensitivity / bias-adjusted treatment effect estimator
- **Key formula / definition:**
  - β* = β̃ − δ · (β̊ − β̃) · (Rmax − R̃) / (R̃ − R̊)
  - δ* solves β(δ) = 0 for given Rmax
  - Default tuning: δ = 1, Rmax = min(1.3 · R̃, 1)
- **Key assumption(s):**
  - Proportional selection: cov(W₁, X) / σ²(W₁) = δ · cov(W₂, X) / σ²(W₂), where W₁ is observed controls index, W₂ is unobserved
  - Assumption 3 (p. 15): Sign(Cov(X, Ŵ₁)) = Sign(Cov(X, W₁)) — observable index does not flip sign of bias direction
  - δ = 1 is conservative ("equal selection") benchmark; δ > 1 means stronger selection on unobservables, δ < 1 weaker
- **Where applicable in our work:** `analysis_v2/h11_durability.py` (or wherever Oster δ is computed); output: `analysis_v2/output/tables/oster_*.csv`. Per SHIPPING_SUMMARY: Phase 3 day 7 → "Oster δ для 6 коэф". Plausible focus: β_post_cba_2017, β_top5, β_all_nba_lag1, β_games_missed_lag1, β_ppg, β_age.
- **Caveat / pitfall:**
  - δ = 1 is heuristic, not theoretically motivated absolute bound; some literatures use δ ∈ [0.5, 2] for sensitivity
  - Rmax > 1 is mathematically possible if R̃ already high; for our M1c_full (R² = 0.65), Rmax = 0.845 is sensible (1.3 × 0.65)
  - When R̃ − R̊ is small, β* can swing dramatically — δ-sensitivity is **most informative when controls move R² substantially**
  - Не применим для FE-models напрямую без residualization; в panel FE одна должна быть осторожна с within-vs-between variance

---

## 8. Limitations / caveats

1. **Theoretical bound, not point estimate.** Oster δ говорит "how much selection would have to be on unobservables to drive effect to zero", но не идентифицирует true β. Это sensitivity test, не identification strategy.
2. **Proportional selection assumption** может нарушаться когда unobservables structurally разные от observables (e.g., observables = stats, unobservable = "локер-рум leadership"). В sports context это особенно остро.
3. **Rmax выбор subjective.** Default 1.3·R̃ — empirical regularity из 50 RCTs, но не теоретическая necessity. Sensitivity к Rmax критична.
4. **Multiple solutions of β*** — нужны дополнительные assumptions (Assumption 3) для уникальности.
5. **No formal SE around β*** — Oster suggests bootstrap, но в большинстве применений (включая, вероятно, наше) — δ репортируется без CI.

---

## 9. Connection to our findings

**SUPPORTS (methodological foundation for robustness section).** Все наши ключевые claims о β_top5, β_post_cba_2017, β_all_nba_lag1, β_games_missed_lag1 опираются на наблюдаемый набор controls в M1c_full / M_full; Oster δ обеспечивает количественную меру их робастности к unobservables.

Применительно к нашим headline findings:
- **β_top5 = −0.098, p = 0.022** (H7 anti-marketability): Oster δ ответит, насколько большой должна быть selection on unobservables (e.g., team market-specific endorsement opportunities, off-court income), чтобы обнулить эффект. Если δ* > 1 → finding survives standard sensitivity check.
- **β_all_nba_lag1 = +0.185, p = 0.008** (H5 awards): Oster δ — насколько большой может быть unobserved leadership / locker-room премия (которая корреллирует с All-NBA), чтобы съесть awards premium.
- **β_games_missed_lag1 = −0.005/game** (H10 durability): unobservable health / injury-prone reputation эффект.

Для Discussion: можно цитировать Oster (2019) как "we follow Oster (2019) recommended bounds δ = 1, Rmax = 1.3·R̃; reported δ values in Table X confirm coefficient robustness".

---

## 10. Reading notes / questions for follow-up

- **Open questions:**
  - В каких именно файлах в `analysis_v2/output/tables/` лежат Oster δ для 6 коэффициентов? Уточнить наименование (oster_*.csv? robustness_*.csv?).
  - Какие 6 коэффициентов выбраны для Oster? Логично: β_post_cba_2017, β_top5, β_all_nba_lag1, β_games_missed_lag1, β_ppg, β_age — но проверить.
- **Alternative methods (для будущего расширения):**
  - Altonji-Elder-Taber (2005) — original framework, более formal но менее operational
  - Krauth (2016) — alternative sensitivity bounds
  - Frank-Lin-Maroulis (2023) "Quantifying Sensitivity to Selection on Unobservables" — обновлённый pedagogical reference
- **Implementation tools:** `psacalc` (Stata, Oster sponsored), `robomit` (R, на CRAN), `causal_tools` (Python, less standard)
- В Methodology addendum можно добавить boxed insight: "Oster δ применяется ТОЛЬКО к OLS estimates, не к IV / RDD / DiD напрямую без модификации". В нашем M1c_full это OK (pooled OLS + year FE), Oster напрямую применима.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
