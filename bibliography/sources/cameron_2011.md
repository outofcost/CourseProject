# Cameron, Gelbach & Miller (2011) — Robust Inference with Multiway Clustering

---

## 1. Citation (APA)

Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust inference with multiway clustering. *Journal of Business & Economic Statistics, 29*(2), 238–249. https://doi.org/10.1198/jbes.2010.07136

---

## 2. Source metadata

- **Type:** methodological (econometric theory + Monte Carlo + applied replication)
- **Sample (Monte Carlo):** 2,000 simulations per condition; designs varying G, H from 25 × 25 до 100 × 100
- **Sample (applied):** replications of Hersch (1998) — 5,960 CPS men, 211 industries × 387 occupations; и one more (Bertrand-Mullainathan setting)
- **Method:** extension of one-way cluster-robust variance estimator (Liang–Zeger 1986; Arellano 1987; Rogers 1993) на nonnested multi-way clustering; key formula eq. (2.15): V̂ = V_G + V_H − V_{G∩H}
- **Pages used in this summary:** 1 (abstract), 2 (intro + use cases), 6 (one-way formula 2.7), 7–8 (two-way formula 2.14–2.15), 15 (Monte Carlo setup), 32 (Hersch replication)
- **DOI / URL:** https://doi.org/10.1198/jbes.2010.07136 (Taylor & Francis paywall); preprint May 2008 на сайте Cameron, UC Davis
- **Access status:** preprint open access (UC Davis); published JBES paywall
- **Local file:** `bibliography/pdfs/cameron_2011.pdf` (preprint version, May 2008)

---

## 3. Use mapping (КРИТИЧНО для интеграции)

- **Stream:** А (методы)
- **Section in coursework:** Methods §3.x (econometric specification — cluster-robust standard errors)
- **Supports hypothesis(es):** не support конкретную гипотезу — это методологическая основа для **всех** Mincer-регрессий и H1–H10 тестов
- **Specifically supports argument:** Стандартная ошибка коэффициентов в panel-Mincer моделях должна учитывать correlation residuals внутри игрока (повторные наблюдения одного player'а в разных сезонах). CGM 2011 — современный canonical reference для cluster-robust inference; в нашей работе SE кластеризованы на player_id. Цитата нужна в Methods как обоснование выбранной procedure standard errors.

---

## 4. Core thesis (3-5 предложений)

Авторы вводят variance estimator, расширяющий one-way cluster-robust SE (eq. 2.7) на случай non-nested multiway clustering, когда наблюдения могут одновременно принадлежать нескольким группировкам (например, state + year, или industry + occupation). Ключевая идея — формула декомпозиции (eq. 2.15): bV[bβ] = V_G + V_H − V_{G∩H}, где V_G — стандартная one-way cluster-robust SE по первой группировке, V_H — по второй, V_{G∩H} — по их пересечению. Это легко реализуется в стандартных статистических пакетах (Stata, SAS) через три отдельные one-way clustering регрессии и арифметическое объединение. Метод опирается на относительно слабые distributional assumptions (errors independent but not identically distributed across clusters; arbitrary within-cluster correlation allowed). Монте-Карло (2 000 симуляций) и replication Hersch (1998) демонстрируют, что игнорирование двусторонней кластеризации приводит к существенному under-estimation SE и over-rejection нулевых гипотез.

---

## 5. Key claims for our text (нумерованный список)

1. **One-way cluster-robust SE — стандарт для panel data c repeated cross-section / fixed effects** (p. 2, со ссылкой на Liang–Zeger 1986, Arellano 1987, Hansen 2005). Это обоснование, что в Mincer-spec'ах с panel на player_id мы должны использовать cluster-robust SE.

2. **Failure to cluster → массивная under-estimation SE → ложные rejections** (p. 2, со ссылкой на Moulton 1986, 1990; Bertrand-Duflo-Mullainathan 2004; Kezdi 2004). Это даёт основу для нашего выбора cluster-robust в Methods.

3. **Two-way clustering formula** (eq. 2.15, p. 8): V̂_{2W} = V_G + V_H − V_{G∩H}. Применимо для нас, если используется кластеризация на player + season (двусторонняя), что было бы лучше для panel с possible time correlation residuals (например, через cap-cycle).

4. **Small-sample correction** (p. 8): √c × bu_g вместо bu_g, где c = G/(G−1) × (N−1)/(N−K). Стандартная Stata-style correction; relevant для нашего finite-sample (3 660 observations, ≈953 player clusters).

5. **Hersch (1998) replication (p. 32):** наглядная иллюстрация — игнорирование one cluster dimension даёт SE = 0.397 (heteroskedastic-robust), one-way cluster on industry даёт 0.643, two-way clustering — 0.702. Под-оценка SE при игнорировании любой dimension может достигать **40-70%**.

---

## 6. Direct quote candidates (с page numbers)

> "Controlling for clustering can be very important, as failure to do so can lead to massively under-estimated standard errors and consequent over-rejection using standard hypothesis tests." (p. 2)

> "These standard errors generalize those of White (1980) for independent heteroskedastic errors … rely on much weaker assumptions — errors are independent but not identically distributed across clusters and can have quite general patterns of within cluster correlation and heteroskedasticity." (p. 3)

> "For non-nested two-way clustering … Ω = V[u|X] can no longer be written as a block diagonal matrix. … bV[bβ] is computed as the sum of the first and second components, minus the third component." (p. 7–8)

> "[The variance estimator] is easily implemented in any statistical package that provides cluster-robust standard errors with one-way clustering." (p. 2)

---

## 7. Methodological notes

- **Method name:** Cluster-robust (sandwich) variance estimator; two-way / multi-way extension
- **Key formula:**
  - One-way: V̂ = (X'X)⁻¹ · Σ_g X'_g û_g û'_g X_g · (X'X)⁻¹  (eq. 2.7, p. 6)
  - Two-way: V̂_{2W} = V_G + V_H − V_{G∩H}  (eq. 2.15, p. 8)
- **Key assumption(s):** errors uncorrelated across clusters in *all* clustering dimensions; within-cluster arbitrary correlation/heteroskedasticity allowed; ⇒ нужна большая asymptotic в обоих cluster-dimensions (G → ∞, H → ∞).
- **Where applicable in our work:** `analysis_v2/m1_full.py` и все `h_*.py` скрипты — везде, где SE кластеризованы на player_id (one-way). Если в коде встречается `cov_type='cluster'` с `cluster_entity_id=player_id` — это и есть CGM 2011 framework (one-way variant).
- **Caveat / pitfall:** при малом G (≤ 30) cluster-robust SE biased downwards; CGM рекомендуют small-sample correction (p. 8) или wild-cluster bootstrap (см. MacKinnon-Webb 2018). У нас G ≈ 953 (player clusters) — small-sample не bites, использование оригинальной формулы валидно.

---

## 8. Limitations / caveats

1. **Asymptotic theory требует G → ∞ в каждой dimension** — для two-way clustering на small numbers of groups в одной из dimensions (e.g., только 9 сезонов в нашей панели) two-way SE могут быть biased. Поэтому one-way clustering на player_id (G=953) безопаснее.
2. **Не альтернатива wild-cluster bootstrap** для inference при interaction-coefficients с **few treated clusters** (см. MacKinnon-Webb 2018 — Б1 в нашем списке wild-cluster для H7 top5×allstar).
3. **Только linear / GMM extensions** в paper; non-linear (probit, logit) рассматриваются, но Stata implementation для них может отличаться.

---

## 9. Connection to our findings

**SUPPORTS (methodological foundation)** — все наши p-values, CI, и FDR-corrections предполагают валидность cluster-robust SE на player_id.

Без CGM 2011 (или ранних works Liang-Zeger / Arellano) наши standard errors для β_ppg, β_age, β_top5 и т.д. были бы существенно underestimated → false rejections. Поскольку в нашей панели каждый игрок появляется до 9 раз, residuals игроков скорее всего скоррелированы (player-specific heterogeneity, even after FE). Cluster-robust на player_id — стандартный fix.

Open question: используем ли мы two-way clustering (player + season) где-то? Если только player — CGM 2011 цитируется per their general framework и one-way formula (eq. 2.7), не per two-way innovation. Если есть two-way spec в robustness — это сильнее обосновывает прямую ссылку на eq. 2.15.

---

## 10. Reading notes / questions for follow-up

- **Open question:** какая именно spec'а кластеризации в `m1_full.py`? Если только one-way на player_id, можно дополнительно цитировать Liang & Zeger (1986) для maximum-correctness. CGM 2011 всё равно остаётся канонической современной ссылкой для **обоснования необходимости** clustering.
- Для wild-cluster bootstrap (H7 interactions) — параллельно ссылаться на CGM 2011 (motivation) + MacKinnon-Webb 2018 (specific algorithm).
- Не путать с Cameron–Trivedi (2005) textbook — это другой источник, более общий по panel methods.
- Сам paper существует в двух версиях: preprint (May 2008) и published JBES (April 2011). Содержание модели идентично; страницы цитат в шаблоне — preprint. Для финального APA цитировать publication date 2011 + journal.

---

**Заполнено:** 2026-05-22
**Заполнил:** Artem (collaborator)
