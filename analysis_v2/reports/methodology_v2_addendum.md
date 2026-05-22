# Methodology v2 — аддендум к Главе 3

Этот файл — текстовая основа для расширения Главы 3 (Методология) в курсовой. Покрывает: (а) новые источники данных, (б) операционализация новых переменных, (в) новые эконометрические спецификации, (г) диагностики.

---

## 3.1 Новые источники данных (расширение)

К существующим источникам v1 (Basketball-Reference per-game/advanced, Hoopshype salaries через Wayback, manual cap & state-tax) добавлены семь блоков:

| Источник | Содержимое | Метод сбора | Покрытие |
|---|---|---|---|
| `awards_panel_full.csv` | All-NBA, All-Defensive, MVP, DPOY (1947–2025) | bbref `/awards/all_league.html` (+ all_defense, mvp, dpoy) | 100% |
| `birth_country.csv` | Дата, город, страна рождения 953 игроков | bbref player meta-block (`#necro-birth`, `/friv/birthplaces.fcgi?country=XX`) | 100% (953/953) |
| `team_season.csv` | W-L, made_playoffs, playoff_round_reached (30×9=270) | bbref team-season pages, регексы по meta-блоку | 100% (1 ATL/2020 — retry после curl-fail) |
| `manual_market_size.csv` | DMA rank Nielsen, MSA population, top5 dummy | Wikipedia "List of US TV markets" + US Census MSA + StatCan для Toronto | 100% (30 команд) |
| `cba_thresholds.csv` | Cap, luxury tax, MLE, max %, min salary | Coon's CBA FAQ + bbref salary-cap-history | 100% (9 сезонов) |
| `awards_features.csv` | Лаги, кумулятивные счётчики, supermax_eligible_loose | Derived из awards_panel_full | 100% |
| `contract_tier.csv` | 9 категорий (minimum → supermax) | Rule-based классификатор + CBA thresholds | 100% |

### 3.1.1 Замечания о coverage

Финальная таблица `data_analysis_v2.csv` содержит 3 660 строк × 153 колонки. После применения фильтров для регрессий M1c-full (must-have-список включает все статистики и lag-переменные) рабочая выборка сокращается до 2 268 строк — теряются:

- 508 строк с pseudo-team `2TM/3TM/4TM` (TOT-rows игроков, поменявших команду внутри сезона) — для них market_size и team_win_pct неопределены;
- ~880 строк сезона 2016 (нет lag-переменных) и игроков-новичков (нет games_missed_lag1).

Эта потеря оформляется как **«by design»** в Главе 3.5; альтернатива (импутация средневзвешенных команд для TOT) была рассмотрена и отвергнута как сильно расширяющая предположения.

---

## 3.2 Операционализация новых переменных

### 3.2.1 Awards block

- `all_nba_lag1` ∈ {0, 1}: индикатор включения в любую (1st/2nd/3rd) All-NBA Team в сезоне t-1.
- `career_all_nba_count`: число попаданий в All-NBA строго ДО сезона t (без утечки таргета).
- `career_allstar_count`: аналогично для All-Star.
- `has_career_all_nba`, `has_career_allstar`, `multi_all_nba` (≥3): бинарные robust-индикаторы, изолирующие "elite в прошлом" эффект от aging-veteran selection bias.

### 3.2.2 Supermax-eligibility (loose)

Согласно CBA 2017 (Designated Veteran Extension):

```
supermax_eligible_loose(t) = 1 iff
    (all_nba(t−1) = 1)
    ∨ (#{s ∈ {t−1, t−2, t−3} : all_nba(s) = 1} ≥ 2)
    ∨ (mvp(t−1) = 1)
    ∨ (dpoy(t−1) = 1)
```

Маскировано к 0 для season < 2018 (CBA 2017 вступила в силу летом 2017 → первый supermax-extension оформлен на сезон 2017/18). Строгий supermax_eligible_strict дополнительно требует experience ∈ [7, 9] и same-team-as-draft (proxy `team_abbr == draft_team`).

### 3.2.3 Contract tier

Rule-based классификатор (см. `analysis_v2/classify_tier.py`) с порядком приоритетов:

1. `rookie_scale`: 1st-round, exp ≤ 4, salary < MLE × 1.10
2. `minimum`: salary < min_salary(exp) × 1.15
3. `mid_level`: salary < MLE_nontax × 1.20
4. `max_25` (0–6 yrs), `high_mid` (other), `max_30` (7–9), `max_35` (10+) — пороги ×1.05 для абсорбции pro-rate
5. `supermax`: salary в зоне max_35 (для 7-9 yrs eligible) или выше, с учётом 105% within-contract bumps
6. `overpay`: residual для anomalies

Включает Rose Rule (designated rookie extension): exp ≤ 6 + eligible → max_30 (Luka 2023/24 как пример). Валидировано на 30 топ-игроках вручную (расхождение ≤ 10%).

### 3.2.4 Market size

- `dma_rank_us`: Nielsen 2023/24 (NaN для Toronto);
- `msa_population_millions`: 2020 US Census MSA / StatCan CMA;
- `market_size_rank_nba`: dense-rank по MSA pop (NYK=BRK=1, LAL=LAC=2, …);
- `top5_market` ∈ {NYK, BRK, LAL, LAC, CHI, GSW} (фиксированный список из плана);
- `top10_market`, `media_market_revenue_proxy`.

### 3.2.5 Continent dummies

USA = reference; born_canada, born_europe, born_latam, born_africa, born_asia_oceania. `is_international = sum(born_*)` — омножен из main spec (perfect collinearity); используется только в альтернативной спецификации, где continent dummies дропаются.

### 3.2.6 Durability

- `games_missed_t = season_length − gp`, где season_length = 82 (норма) или 72 (COVID 2019/20 и 2020/21);
- `games_missed_lag1`, `games_missed_3y_cum`, `gp_pct_t = gp/season_length`.

### 3.2.7 Team-level controls

- `wins`, `win_pct`, `made_playoffs`, `playoff_round_reached` (0=missed → 5=champion);
- Лаги: `team_win_pct_lag1`, `team_made_playoffs_lag1`;
- `team_salary_committed_t`: внутри-панельная агрегация salary_usd по (team_abbr, season);
- `team_over_luxury_tax_t = (team_salary_committed_t > luxury_tax_t)` ∈ {0, 1}.

---

## 3.4 Новые эконометрические спецификации

### M1c_full и варианты (Day 1–2 Фазы 3)

| Spec | Регрессоры | R² | N |
|---|---|---|---|
| M1c_full | Stats + Age + Demo + Continent + Market(top5) + Awards + Durability + Team + Struct | 0.651 | 2 268 |
| M1c_full_alt_mkt | top5_market → market_size_rank_nba | 0.651 | 2 268 |
| M1c_full_robust_awards | career_*_count → has_career_*  + multi_all_nba | 0.652 | 2 268 |
| M1c_full_no_collinear | drop experience + ws (VIF > 10) | 0.640 | 2 268 |
| M1d_full | 2-way FE (player + season); time-invariant дропается | 0.151 (within) | 2 268 |

Все спецификации с кластер-робастными SE на `player_id`. Year FE через PanelOLS `time_effects=True`.

### M8 — Market hypothesis

- M8a: M1c + `top5_market` (main)
- M8b: M1c + `market_size_rank_nba` (continuous альтернатива)
- M8c: M1c + `top5 + allstar + top5×allstar` (heterogeneity по звездности)
- M8d: M1c + `top5 + is_international + top5×is_international`

Wild-cluster bootstrap (Rademacher, 1000 reps) на interaction-коэффициенте — Cameron, Gelbach & Miller (2011).

### M9 — Tier structure hypothesis

- M9a: Pure tier (без Performance) — институциональный слой в изоляции (R² = 0.849)
- M9b: M1c + tier dummies (R² = 0.862, ΔR² = +0.21 поверх M1c)
- M9c: M9b + supermax_eligible_loose + tier_max_30 × eligible (только эта interaction имеет ненулевую вариацию — tier_supermax → eligible by classifier design)

Tier-specific Mincer-регрессии (Performance + Age блок внутри каждого tier) — для проверки cap-truncation гипотезы (β_ppg ниже в max-tiers).

### M10 — Awards channel hypothesis

- M10a (cumulative): M1c — все три awards-регрессора (all_nba_lag1 + career_all_nba_count + career_allstar_count)
- M10a_robust: бинарные индикаторы вместо кумулятивных
- M10b: supermax_eligible_loose substitution — alt-channel без all_nba_lag1 (избегая r=0.78 collinearity)
- **Event study** вокруг первого All-NBA в карьере: τ ∈ {−2, −1, 0, +1, +2, +3, ≥4}; never-treated = baseline

### M11 — Durability + M_full

- M11a: M1c + games_missed_lag1 (main)
- M11b: M1c + games_missed_lag1 + games_missed_lag1 × age (age-mediated discount)
- **M_full**: всё-в-одном (M1c + tier + supermax_elig); R² = 0.862

---

## 3.5 Диагностики

### 3.5.1 Декомпозиция R²

Два метода:

1. **Sequential R²**: добавление блоков в plan-order, ΔR² на каждом шаге + 95% bootstrap CI (200 cluster-resamples на player_id). Дополнительно — **reverse-order** для диагностики порядок-зависимости.
2. **Shapley R²** (order-independent): 2^9 = 512 subset-OLS-фитов, формула Shapley value по теореме Shapley (1953). Sum(shapley_i) = R²_full (efficiency property), что верифицируется до 1e-10.

### 3.5.2 VIF

`statsmodels.stats.outliers_influence.variance_inflation_factor` на M1c_full регрессорах:
- age, age_sq: 147 / 151 (ожидаемо, by construction в Mincer)
- ppg: 44.6, mpg: 26.0, ws: 20.5 (performance-кластер коллинеарности)
- остальные: < 10

Альтернативная spec `M1c_full_no_collinear` дропает experience и ws — R² теряется только −0.011.

### 3.5.3 Oster (2019) δ-sensitivity

Closed-form δ из Oster (2019) eq. (3):

$$\delta \approx \frac{(\tilde\beta - \hat\beta) \cdot (R_{\max} - \hat{R})}{(\dot\beta - \tilde\beta) \cdot (\hat{R} - \dot{R})}$$

с R_max = 1.3 · R²_obs. Применено к шести ключевым новым коэффициентам. **Все δ < 1** — это **ожидаемо** для домена с богатыми observables (Performance + Age дают R²=0.61 в minimal-controls спеке); знак коэффициента стабилен, magnitude чувствительна к спецификации. В Главе 5 это обсуждается как ограничение Oster в наблюдательно-богатых данных.

### 3.5.4 Multiple-testing correction

На 11 ключевых тестах (новые H8/H9/H10/H11):

- **Bonferroni** (α/n = 0.0045): выживают tier_supermax, tier_max_35, tier_minimum, career_allstar_count, games_missed_lag1
- **BH-FDR @ 5%**: дополнительно top5_market, all_nba_lag1

### 3.5.5 Wild-cluster bootstrap

На interaction коэффициентах M8c (`top5 × allstar`) и M8d (`top5 × intl`) — Rademacher weighted, 1000 реплик, restricted model imposes H₀: β_interaction = 0. CI95 шире классических → нет значимой heterogeneity.

---

## 3.6 Регресс-тест воспроизводимости v1

Скрипт `analysis_v2/regress_test_v1.py` запускает M1a, M1b, M1c, M1d на `data_analysis_v2.csv` без новых регрессоров. Сравнение с published `output/tables_v1/*.txt` показывает **max coef diff < 5×10⁻⁵** на всех 4 моделях → расширение датасета НЕ повлияло на v1 результаты. Hash-snapshot базы зафиксирован в `analysis_v2/reports/v1_snapshot.sha256` (SHA256: `cf846b1aaa4a…`).

Это критическая гарантия: новые findings (H8–H11) не контаминированы изменением структуры базовой панели.
