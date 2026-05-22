# План Правок В1 — пошаговая инструкция для Claude Code

> **Контекст для Claude Code, начинающего этот план:**
>
> Это курсовая работа бакалавра по эконометрике панельных данных для рынка труда NBA 2015/16–2023/24. Срок защиты — 1–2 недели. Уровень — 3–4 курс бакалавриата (можно использовать `statsmodels`, `linearmodels`, простой `QuantReg`, bootstrap; **не нужно** Heckman, IV, GMM, Arellano-Bond).
>
> Текущий результат (V0) разобран в `revisions_v1/PROBLEMS.md`. Главные провалы — циркулярность M3c (cy_A определена через salary jump, и затем salary jump регрессируется на неё), бага с experience для всех 612 undrafted = 0, и пропадание 107 наблюдений Toronto.
>
> **Принципы работы:**
> - Каждый run пишет лог в `revisions_v1/logs/<step>_<date>.log`.
> - Не трогать `analysis/` напрямую — все новые файлы в `analysis_v1/`. Старая версия должна оставаться runnable.
> - Все output-таблицы V1 пишутся в `output/tables_v1/` и `output/figures_v1/`.
> - Каждый шаг заканчивается verification (assert / sanity check) и сохранением артефакта.
> - METHODOLOGY переписывается только **в конце**, после всех run'ов, чтобы не править её несколько раз.
> - Если шаг не удался — фиксируй в логе и иди дальше, не блокируй всю цепочку.

---

## Структура нового кода

```
revisions_v1/
├── PROBLEMS.md          ← реестр проблем (готов)
├── IMPLEMENTATION_PLAN.md ← этот файл
├── logs/                ← логи всех run'ов
└── notes/               ← заметки по ходу work

analysis_v1/             ← новый модуль, рядом со старым
├── __init__.py
├── config.py            ← обновлённые константы
├── prep_v1.py           ← фиксы A2, A3, C13
├── contract_year_v1.py  ← фикс A1, A4, C5
├── m1_v1.py             ← фикс B2 (упрощение combined), B5 (collinearity)
├── m2_v1.py             ← фикс A3 (Toronto)
├── m3_v1.py             ← фикс A1
├── robustness_v1.py     ← пересчёт + новые robustness
├── diagnostics.py       ← НОВЫЙ — VIF, BP-test, influence, power analysis
├── quantile.py          ← НОВЫЙ — quantile regression
├── event_study.py       ← НОВЫЙ — CBA 2017 event-study
├── bootstrap.py         ← НОВЫЙ — wild cluster bootstrap (опционально)
├── figures.py           ← НОВЫЙ — все графики
├── utils.py             ← shared helpers (импортируй из analysis/utils.py)
└── run_all_v1.py        ← pipeline orchestrator

output/
├── tables_v1/           ← все CSV/txt V1
└── figures_v1/          ← все PNG/PDF V1

data/clean/
├── data_analysis_v1.csv ← после prep_v1
└── contract_year_v1_diagnostics.csv
```

---

## §1. Фиксы данных (БЛОКЕРЫ — без них дальше нельзя)

### §1.1 Переделать `contract_year` (A1 + A4)

**Файл:** `analysis_v1/contract_year_v1.py`

**Что сделать:**

1. Разделить `cy_A` на два сигнала:
   - `cy_A_up` = `(real_salary_change > 0.25)` — игрок получил повышение сверх инфляции cap.
   - `cy_A_down` = `(real_salary_change < -0.25)` — игрок получил понижение.
   - Старый `cy_A` (модуль) — больше **НЕ использовать** в анализе.

2. Обновить `cy_B`: разделить smooth team change vs trade. Параметризовать через season transitions.
   - `cy_B_offseason` = team changed AND no mid-season movement in either year → free agency / sign-and-trade.
   - `cy_B_trade` = team_abbr_t ∈ {'2TM', '3TM', '4TM'} (mid-season move в году t) → trade.
   - Используй только `cy_B_offseason` как канонический сигнал new contract.

3. Финальный `contract_year` = `max(cy_A_up, cy_B_offseason, cy_C)`. **БЕЗ cy_A_down**.
   Это ключевое: контрактный год — это «игрок ожидает повышения», а не «любая флуктуация».

4. Дополнительная переменная для М3c: `cy_exogenous = max(cy_B_offseason, cy_C)`. Это сигнал контрактного года, **не использующий** будущую зарплату. Регрессия Δlog_salary на cy_exogenous будет настоящим canonical test.

5. Документировать в шапке файла все 4 определения (cy_A_up, cy_A_down, cy_B_offseason, cy_B_trade, cy_C, contract_year, cy_exogenous), формулы и интуицию.

**Verification:**

```python
df = pd.read_csv("data/clean/data_analysis_v1.csv")
# 1. cy_A_up ⊂ cy_A_up ∪ cy_A_down должны быть disjoint
assert ((df["cy_A_up"]==1) & (df["cy_A_down"]==1)).sum() == 0
# 2. cy_exogenous НЕ должна коррелировать с salary_next/salary_t
sub = df.dropna(subset=["salary_next","cy_exogenous"])
corr = np.corrcoef(sub["cy_exogenous"], np.log(sub["salary_next"]/sub["salary_usd"]))[0,1]
print(f"corr(cy_exogenous, dlog_salary) = {corr:.4f}")
assert abs(corr) < 0.30, "cy_exogenous still suspicious"
# 3. Распределение должно быть в разумных рамках:
print(df["contract_year"].value_counts(dropna=False))
```

**Ожидаемые результаты:** `cy_exogenous = 1` доля ~25–30% (меньше, чем V0 contract_year = 58%, потому что cy_A исключён).

---

### §1.2 Исправить `experience` для undrafted (A2)

**Файл:** `analysis_v1/prep_v1.py`

**Что сделать:**

1. Заменить блок:
   ```python
   df["experience"] = df["experience"].fillna(0)
   ```

2. Для **drafted** оставить как есть: `experience = season - draft_year`.

3. Для **undrafted** считать experience через `cumcount` по player_id:
   ```python
   df = df.sort_values(["player_id", "season"])
   undrafted_mask = df["undrafted"] == 1
   df.loc[undrafted_mask, "experience"] = (
       df[undrafted_mask].groupby("player_id").cumcount() + 1
   )
   # +1 потому что first NBA season = experience 1 (как у drafted)
   ```

4. Проверить, что для drafted конвенция: rookie season (1-й год) = experience 1 (как в текущей версии — min=1).

5. Создать также `experience_career_total` для каждого игрока — общий стаж карьеры (для альтернативной спецификации).

**Verification:**

```python
df = pd.read_csv("data/clean/data_analysis_v1.csv")
# VanVleet должен иметь experience 1..8 за 2017-2024
vv = df[df["player_name"].str.contains("VanVleet")].sort_values("season")
print(vv[["player_name","season","experience"]])
assert vv["experience"].tolist() == [1,2,3,4,5,6,7,8]

# experience>0 group уже не должен совпадать с drafted-only
exp0_n = (df["experience"]==0).sum()
und_n = (df["undrafted"]==1).sum()
print(f"exp=0 count: {exp0_n}, undrafted count: {und_n}")
assert exp0_n < und_n, "experience fix failed"
```

---

### §1.3 Добавить Toronto в state_tax (A3)

**Файл:** `data/lookups/state_tax.csv` (вручную / через скрипт)

**Что сделать:**

1. Добавить строку для TOR в `state_tax.csv`:
   ```csv
   TOR,Toronto Raptors,Toronto,Ontario,0,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%,53.53%
   ```
   - `no_income_tax = 0` (есть income tax).
   - `state_tax_rate ≈ 0.5353` для всех сезонов (Ontario top marginal 53.53% in 2024, изменялся незначительно — для бакалавра можно усреднить).
   - **Источник:** Ontario top marginal rate by year, https://www.ontario.ca/page/personal-income-tax. Для большей точности по годам можешь взять:
     - 2016: 49.53%, 2017: 53.53%, 2018: 53.53%, ..., 2023: 53.53%, 2024: 53.53%.

2. Добавить дополнительный флаг `is_canada` (= 1 для TOR, 0 для других) — пригодится для робастности.

3. Перезапустить prep_v1 → проверить, что у TOR теперь есть `state_tax_rate`.

**Verification:**

```python
df = pd.read_csv("data/clean/data_analysis_v1.csv")
tor = df[df["team_abbr"]=="TOR"]
print(f"TOR obs: {len(tor)}, state_tax notna: {tor['state_tax_rate'].notna().sum()}")
assert tor["state_tax_rate"].notna().all()
assert tor["state_tax_rate"].between(0.45, 0.56).all()
```

---

### §1.4 Trade vs free-agency в team_change (C5)

Реализовано в составе §1.1 (cy_B_offseason vs cy_B_trade). Дополнительно: при merge с salary_next посчитать, был ли игрок в multi-team в t+1.

---

### §1.5 NaN-флаги вместо `fillna(0)` для shooting % (C13)

**Файл:** `analysis_v1/prep_v1.py`

Для каждого shooting % столбца:
```python
df[f"no_{col}_attempts"] = df[col].isna().astype(int)
df[col] = df[col].fillna(0)
```

И добавить эти дамми в `BASIC_STATS` опционально (через флаг).

---

## §2. Спецификационные фиксы регрессий

### §2.1 VIF и упрощение combined stats (B2)

**Файл:** `analysis_v1/diagnostics.py`

1. Реализовать функцию `vif_table(X, name)` → таблицу VIF для каждого регрессора.
2. Прогнать на X базовой модели M1c. Сохранить в `output/tables_v1/vif_M1c.csv`.
3. Если для какого-то регрессора VIF > 10 — оставить только один advanced stat. **Рекомендация:** оставить `vorp` + `usg_pct`, убрать `per`, `ws`.
4. Создать M1c_v1 как combined_stats_minimal = `["ppg", "rpg", "apg", "mpg", "gp", "vorp", "usg_pct"]`.
5. Сделать таблицу `output/tables_v1/M1c_comparison.csv` — старый (full) vs новый (minimal) — для интерпретации.

**Verification:**
```python
vif_df = pd.read_csv("output/tables_v1/vif_M1c.csv")
assert vif_df["VIF"].max() < 15, "Multicollinearity still present"
```

---

### §2.2 Документировать R²_within (B3)

В `METHODOLOGY_v1.md` (см. §5.7) добавить честное объяснение:
- R²_within = −0.20 в M1d **не артефакт**, а сигнал того, что внутри-игроцкая вариация salary определяется дискретными контрактными ступеньками, а не плавной траекторией stats.
- Это сильное содержательное утверждение: salary changes within-player are not well-tracked by within-player stat changes. Player FE специфика NBA с rookie/max contracts.
- Альтернатива (для master-thesis) — Arellano-Bond GMM. Деферим.

Никакого кода не нужно — только пересмотр интерпретации.

---

### §2.3 Per-36 minutes stats (B4)

**Файл:** `analysis_v1/prep_v1.py`

1. Добавить `ppg_per36 = ppg * 36 / mpg`, аналогично rpg_per36, apg_per36, spg_per36, bpg_per36.
2. Добавить альтернативный config `BASIC_PER36 = ["ppg_per36", "rpg_per36", ..., "fg_pct", ...]`.
3. Прогнать M1a, M1b на per-36 версии → сохранить как M1a_per36, M1b_per36 в `output/tables_v1/`.
4. Сравнить коэффициенты в `M1_comparison_per36.csv`.

**Verification:** коэффициент `mpg` в per-36 версии может стать незначимым (так как PPG уже delated на mpg). Это нормально.

---

### §2.4 Фикс collinearity age/experience (B5)

**Файл:** `analysis_v1/m1_v1.py`, **сразу после фикса A2**.

1. Создать спецификации M1a:
   - M1a_baseline — как раньше (с age, age², experience, undrafted).
   - M1a_age_only — убрать experience.
   - M1a_exp_only — убрать age, age². Использовать experience, experience².
2. Сравнить implied peak возрастной траектории по каждой спецификации. Сохранить в `output/tables_v1/age_peak_comparison.csv`.

**Verification:** ожидаемый пик в M1a_age_only — около 30–31 года. Если получился ещё хуже — есть другая проблема.

---

### §2.5 Заменить shooting % на `ts_pct` (B6)

**Файл:** `analysis_v1/config.py`.

В `BASIC_STATS` заменить `fg_pct, fg3_pct, ft_pct` → `ts_pct` (true shooting percentage уже есть в данных).

Сделать прогон M1a с `ts_pct` → `output/tables_v1/M1a_ts_only.txt`. Сравнить с baseline.

---

### §2.6 Cap-deflated DV — alternative (C1)

**Файл:** `analysis_v1/m1_v1.py` дополнительная спецификация.

1. Создать `ln_cap_share = log(salary_usd / cap_t)`.
2. Прогнать M1a, M1b на новой DV. Сохранить в `M1a_cap_share.txt`, `M1b_cap_share.txt`.
3. Year FE становится менее «нагружен» — большая часть структурного тренда уходит в DV.

**Verification:** в M1a_cap_share без year FE коэффициенты `post_cba_2017` и `post_covid` должны существенно сократиться по абс. величине.

---

### §2.7 PG как position reference (C2)

Поменять в `prep_v1.py`:
```python
for p in ["SG", "SF", "PF", "C"]:  # PG как reference, C — отдельный dummy
    df[f"pos_{p}"] = ...
```

Обновить `config.py` соответственно. Прогнать M1a_pg_ref.

---

### §2.8 Multi-position (C3)

```python
df["is_PG"] = df["position"].str.contains("PG").astype(int)
df["is_SG"] = df["position"].str.contains("SG").astype(int)
# ... etc.
```

Это даст игроку SG-SF одновременно is_SG=1 и is_SF=1. Прогнать M1a_multihot. Если результат сильно отличается → обсудить.

---

### §2.9 Interactions stats × post_cba_2017 (C8)

В M1a добавить interactions `ppg × post_cba`, `mpg × post_cba`. Тест: F-test на joint significance → проверка, изменилась ли «оценка единицы PPG» после CBA 2017.

Сохранить в `output/tables_v1/M1a_cba_interactions.txt`.

---

## §3. Перезапуск всех моделей V1

После шагов §1–§2 — перезапустить все 17 моделей (M1*4, M2*4, M3*4, R*5) на новом датасете с фиксами.

### §3.1 Spotrac калибровка contract_year (D3, опционально)

**Файл:** `analysis_v1/spotrac_calibration.py` (НОВЫЙ).

**Что сделать:**

1. Через WebFetch получить таблицы Spotrac для сезонов 2022/23 и 2023/24 (URL: `https://www.spotrac.com/nba/contracts/`). Это даёт contract length для каждого игрока.

2. Загрузить ~150–200 пар (игрок, сезон) — последний год их контракта (true contract year).

3. Создать `data/lookups/spotrac_cy.csv` с колонками: `player_name, season, true_cy`.

4. Merge с твоим cy (из §1.1). Посчитать confusion matrix:
   ```
                  true_cy=1   true_cy=0
   our_cy=1         TP=?       FP=?
   our_cy=0         FN=?       TN=?
   ```

5. Precision / Recall / F1 score для эвристики. Сохранить в `output/tables_v1/spotrac_calibration.csv`.

6. Если recall < 60% или precision < 60% — пересмотреть эвристику. **Это критично для интерпретации M3 в работе.**

**Verification:** Spotrac должен покрывать ≥ 100 наблюдений после merge.

> Если WebFetch заблокирует Spotrac — пропусти этот шаг, отметь в логе. Курсовая бакалавра без этого защищается.

---

### §3.2 Jock tax (C9, опционально на time)

**Файл:** `analysis_v1/jock_tax.py` (НОВЫЙ).

**Что сделать:**

1. Через basketball-reference scrape (опираясь на `nba_scraper/`) собрать schedule каждой команды за каждый сезон — список opponents and home/away.

2. Для каждого игрок-сезон посчитать `effective_tax_rate`:
   ```
   eff_rate = 0.5 * home_state_rate + 0.5 * mean(opponent_state_rates weighted by # games)
   ```
   (упрощение: 41 home + 41 road, не учитывая length of stay).

3. Прогнать M2c_jock_tax с `effective_tax_rate` вместо `state_tax_rate`. Сохранить.

**Verification:** corr(effective_rate, home_state_rate) > 0.7 (преобладает home state), но есть variation от schedule.

> Если scraping не сработает или съест > 1 дня — пропусти. Упомяни в limitations.

---

## §4. Диагностики и SE

### §4.1 Wild cluster bootstrap (B1)

**Файл:** `analysis_v1/bootstrap.py`.

**Что сделать:**

1. Реализовать wild cluster bootstrap по player_id с Rademacher weights, 999 replications.
   ```python
   def wild_cluster_bootstrap(model, cluster_var, n_boot=999, seed=42):
       # ... compute bootstrap p-value for each coefficient
   ```

2. Прогнать на ключевых коэффициентах:
   - M1a: post_cba_2017, post_covid
   - M2c: state_tax_rate
   - M3c (новая cy_exogenous-версия): cy_exogenous
   - R1: contract_year, no_income_tax

3. Сохранить в `output/tables_v1/wild_bootstrap_pvalues.csv` (coefficient | cluster-SE p | bootstrap p).

**Альтернатива (проще):** использовать `linearmodels` two-way clustering (`cov_type="clustered", cluster_entity=True, cluster_time=True`). Это даст почти то же при наличии достаточно year-кластеров. С 9 годами это marginal, но методологически приемлемо для бакалавра. Покажи оба.

---

### §4.2 Heteroskedasticity tests (B9)

**Файл:** `analysis_v1/diagnostics.py`.

1. Breusch-Pagan, White tests на residuals M1a, M2c, M3c_canonical.
2. Сохранить в `output/tables_v1/heteroskedasticity_tests.csv`.

```python
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
```

---

### §4.3 Power analysis для null-results (B7)

**Файл:** `analysis_v1/diagnostics.py`.

Для каждого null-результата (allstar, state_tax_rate, no_income_tax):
1. SE из модели.
2. MDE при power 80% = |β| такая, что power = 0.80 при two-sided test α=0.05 → β = 2.8 × SE.
3. Перевести в экономические единицы: для state_tax_rate (continuous 0–0.535) → MDE × range = effect на end-to-end переходе.
4. Таблица: `output/tables_v1/power_analysis.csv`.

Пример:
| coef | est | SE | MDE (β) | MDE (%-change DV) | Plausibility |
|------|----:|----:|---:|---:|---|
| state_tax_rate | -0.36 | 0.33 | 0.92 | 60% за 50pp tax shift | Очень большой; null неинформативен |

---

### §4.4 Multiple testing correction (B10)

**Файл:** `analysis_v1/diagnostics.py`.

1. Собрать p-values 17 моделей × ключевых регрессоров.
2. Применить Benjamini-Hochberg FDR (`statsmodels.stats.multitest.multipletests(method='fdr_bh')`).
3. Сохранить `output/tables_v1/multiple_testing.csv` (variable | raw p | adjusted p | reject@0.05 raw | reject@0.05 BH).

---

### §4.5 Influence diagnostics / outliers (C10)

**Файл:** `analysis_v1/diagnostics.py`.

1. Cook's distance, leverage hat-values для M1a.
2. Top-10 influential observations → `output/tables_v1/top_influential.csv`.
3. Прогнать M1a без top-10 → коэффициенты не должны измениться сильно. Сохранить как M1a_no_outliers.

---

### §4.6 Sample missingness diagnostics (C14)

**Файл:** `analysis_v1/diagnostics.py`.

1. Сколько игроков выпадают на каждом шаге обработки (start → drop multi-team → drop NaN salary → ...) и почему.
2. Сохранить в `output/tables_v1/sample_attrition.csv`.

---

### §4.7 Minimal tests (E4)

**Файл:** `analysis_v1/tests_v1.py`.

Pytest на:
1. `experience > 0` для всех VanVleet seasons.
2. TOR имеет `state_tax_rate ≈ 0.535`.
3. `cy_A_up` и `cy_A_down` disjoint.
4. `contract_year_v1` распределение в разумных границах.
5. На сэмпле — re-run M1a и сравни ключевые коэффициенты с baseline (snapshot).

---

## §5. Расширения (на уровне 3–4 курса бакалавриата)

### §5.1 Quantile regression (C11)

**Файл:** `analysis_v1/quantile.py`.

**Что сделать:**

1. `from statsmodels.regression.quantile_regression import QuantReg`.
2. Прогнать M1a на τ ∈ {0.10, 0.25, 0.50, 0.75, 0.90}.
3. Для каждого τ — сохранить коэффициенты + bootstrap SE (`QuantReg(...).fit(q=tau).bse` уже даёт IID-version; для clustered делай ручной cluster bootstrap).
4. Таблица `output/tables_v1/quantile_M1a.csv`: variable × τ.
5. Фигура `output/figures_v1/quantile_coefficients.png`: для key regressors (ppg, age, allstar, undrafted) — коэффициент vs τ с CI.

**Содержательно ожидать:**
- `ppg` коэффициент **уменьшается** с τ → у max-contract players marginal PPG менее важен (упор в cap).
- `undrafted` эффект **больше** для нижних дециле (там strong selection).
- `state_tax_rate` — посмотри, отличается ли null-result между квантилями.

---

### §5.2 Event-study CBA 2017 (D1)

**Файл:** `analysis_v1/event_study.py`.

**Что сделать (упрощённая версия для бакалавра):**

1. Сезон 2017/18 (season_end = 2018) — event year (`event = 0`).
2. Для каждого сезона t создай `event_time = t - 2018` ∈ {−2, −1, 0, 1, 2, 3, 4, 5, 6}.
3. Регрессия:
   ```
   ln_salary = β_0 + Σ_{τ ≠ -1} β_τ · 1{event_time = τ} + Stats + Controls + ε
   ```
   (исключи τ = −1 как reference period).
4. Plot β_τ с 95% CI vs τ → `output/figures_v1/event_study_cba2017.png`.
5. Тест pre-trends: F-test на joint significance β_{-2} (должен быть ~0, потому что pre-trends отсутствуют, если CBA 2017 — exogenous shock).

**Verification:** pre-period (τ = -2) должен быть статистически неотличим от нуля. Если значим — pre-trends → DiD интерпретация скомпрометирована.

---

### §5.3 F-test / specification tests таблица (C16)

**Файл:** `analysis_v1/diagnostics.py`.

Для каждой основной модели — таблица:
| Model | F (poolability) | p | Hausman vs random | p | Joint sign. year FE | p |

Сохранить в `output/tables_v1/specification_tests.csv`.

---

### §5.4 Расширение hoopshype к 2008 (D2, опционально)

**Файл:** `nba_scraper/extend_to_2008.py`.

**Что сделать:**

1. Используя существующий wayback-подход, scrape salary pages 2008–2015.
2. Аналогично — bbref per-game / advanced.
3. Merge в `data_merged_extended.csv`.
4. Прогнать M1a_extended → подтверждение/опровержение основных эффектов на 17-сезонной выборке.

> Если scraping не сработает / съест > 2 дней — пропусти. Курсовая обоснованно ограничена 2015–2024.

---

### §5.5 Market-size proxy (D4)

**Файл:** `data/lookups/market_size.csv` (новый, заполнить вручную / через WebFetch).

Колонки: `team_abbr, city, city_population_metro, tv_market_rank (1-30, source: Nielsen)`.

Прогнать M1a_market → проверить, остаются ли структурные сдвиги.

---

### §5.6 Все фигуры (E1)

**Файл:** `analysis_v1/figures.py`.

Список обязательных фигур → `output/figures_v1/`:

1. **`fig_1_distribution_salary.png`** — histogram + KDE для `salary_usd` (log scale).
2. **`fig_2_distribution_lnsalary_by_season.png`** — box plot ln_salary by season.
3. **`fig_3_scatter_ppg_vs_salary.png`** — scatter ln_salary vs PPG, colored by season.
4. **`fig_4_age_profile.png`** — mean ln_salary by age (raw, unconditional) с quadratic fit.
5. **`fig_5_age_profile_conditional.png`** — partial regression plot (controlling for stats).
6. **`fig_6_coefficient_plot_M1.png`** — coefficient plot key regressors M1a vs M1b vs M1c vs M1d.
7. **`fig_7_coefficient_plot_M3.png`** — то же для M3 (со старым cy + новым cy_exogenous).
8. **`fig_8_residuals_M1a.png`** — residuals vs fitted, residuals vs PPG.
9. **`fig_9_predicted_vs_actual.png`** — scatter predicted ln_salary vs actual.
10. **`fig_10_correlation_heatmap.png`** — heatmap corr(stats × stats).
11. **`fig_11_quantile_coefficients.png`** — quantile regression β vs τ (см. §5.1).
12. **`fig_12_event_study_cba2017.png`** — event-study coefs (см. §5.2).
13. **`fig_13_tax_distribution.png`** — distribution state_tax_rate by team (now with Toronto).
14. **`fig_14_contract_year_diagnostic.png`** — distribution of Δlog_salary by old cy / new cy_exogenous (visual confirmation A1 fix).

Все фигуры — matplotlib, минимум стиля, axis labels по-русски, title по-английски (consistency с тех. literature).

---

### §5.7 Переписать METHODOLOGY (E5)

**Файл:** `analysis_v1/METHODOLOGY_v1.md`.

**Что переписать:**

1. **Раздел 4.5** (contract_year) — описать новую эвристику cy_A_up / cy_A_down / cy_B_offseason / cy_C / cy_exogenous. Признать, что V0 имела circularity, и V1 это устраняет.

2. **Раздел 5.3** (M3 results) — переписать с новыми числами. Главный результат теперь — **сравнение** cy_exogenous (canonical, без circularity) vs cy_A_up (с circularity, для контраста). Если cy_exogenous даёт null result или слабый эффект — честно признать.

3. **Раздел 6.2** (сводка по гипотезам) — обновить.

4. **Раздел 7.2** (limitations) — переписать честно: «в V0 эвристика имела circularity. В V1 это исправлено. Остаточная проблема — false negatives без Spotrac data.»

5. **Раздел 7.5** (endogeneity) — расширить с учётом B4, B5 обсуждения.

6. Добавить новый **раздел 8** — все диагностики V1: VIF, BP-test, power analysis, multiple testing.

7. Обновить **заключение** — с честными выводами.

> **Это самый длинный текстовый шаг — делать в самом конце, после всех run'ов.**

---

## §6. Что отложено для будущего

В `revisions_v1/PROBLEMS.md` отмечено как 🟡 / 🟢, в плане **не реализуется**, но для магистратуры:

- Heckman two-step (B8) — обсудить в limitations.
- Arellano-Bond / system GMM dynamic panel (C12) — обсудить.
- Endorsement / marketability proxies (D4 advanced).
- Cross-league comparison (NHL, MLB).
- Full Spotrac integration (вся выборка 2015–2024).
- Sample expansion 2008–2014 (если не успеешь — упомяни).

---

## §7. Sequence of execution (рекомендованный порядок выполнения)

> Эта последовательность минимизирует «бруки» — если §1 запорется, дальнейшие шаги не имеют смысла.

**Неделя 1, день 1–2 — БЛОКЕРЫ:**
- §1.1 contract_year_v1.py
- §1.2 prep_v1.py (experience fix)
- §1.3 state_tax с Toronto
- §1.5 shooting % flags
- §4.7 базовые тесты (assert)
- **Промежуточный результат:** `data/clean/data_analysis_v1.csv` с фиксами.

**День 3 — Перезапуск всех 17 моделей:**
- §3 (M1_v1, M2_v1, M3_v1, R_v1)
- **Сохранить в `output/tables_v1/`. Сравнить с V0 в `output/tables_v1/changes_summary.csv`.**

**День 4 — Диагностики:**
- §2.1 VIF
- §4.2 heteroskedasticity
- §4.3 power analysis
- §4.4 multiple testing
- §4.5 influence

**День 5 — Альтернативные спецификации:**
- §2.3 per-36
- §2.4 age/experience disentangle
- §2.5 ts_pct
- §2.6 cap-deflated DV
- §2.7 PG-reference
- §2.8 multi-position
- §2.9 CBA interactions

**День 6–7 — Расширения:**
- §5.1 quantile regression
- §5.2 event-study CBA 2017
- §5.3 specification tests
- §4.1 wild cluster bootstrap (если успеешь — иначе two-way clustering)

**День 8 — Опциональные расширения (если есть время):**
- §3.1 Spotrac calibration
- §3.2 Jock tax
- §5.4 расширение к 2008
- §5.5 market size

**День 9–10 — Фигуры и METHODOLOGY:**
- §5.6 все фигуры
- §5.7 переписать METHODOLOGY

**День 11–12 — Финальные проверки:**
- Прогнать `run_all_v1.py` end-to-end.
- Все output-таблицы воспроизводимы.
- METHODOLOGY соответствует фактическим числам.
- Все звёздочки и интерпретация согласованы.

**День 13–14 — Защита (репетиция):**
- Подготовить slide deck (используй pptx skill).
- Возможные вопросы научного руководителя:
  - «Что вы сделали по сравнению с V0?» → A1, A2, A3 фиксы, новый cy_exogenous, quantile + event-study.
  - «Почему M3c теперь null/смешан?» → cy_exogenous — canonical signal, а cy_A был circular. У вас честная картина.
  - «Почему Toronto важен?» → highest tax burden, highest identification power для H5.
  - «Что показывает quantile regression?» → cap structure делает effect concave: top decile не реагирует на marginal stats.
  - «Где limitations?» → честно: Spotrac не подключен полностью, jock tax — упрощение, Heckman не сделан.

---

## §8. Что должно быть на финише — checklist

- [ ] `data/clean/data_analysis_v1.csv` (3660 rows, новые поля: cy_A_up, cy_A_down, cy_B_offseason, cy_exogenous, experience-fixed)
- [ ] 17+ output-таблиц в `output/tables_v1/` (M1*4 + M2*4 + M3*4 + R*5 + новые)
- [ ] VIF, Breusch-Pagan, power analysis, multiple testing tables
- [ ] Quantile regression results
- [ ] Event-study CBA 2017 results
- [ ] 14 фигур в `output/figures_v1/`
- [ ] `METHODOLOGY_v1.md` — переписан, числа соответствуют
- [ ] `PROBLEMS.md` — каждая проблема либо resolved, либо явно deferred
- [ ] `run_all_v1.py` — end-to-end reproducible
- [ ] Pytest проходит
- [ ] Slide deck для защиты

---

## §9. Ссылки на критически важные файлы V0 (для reference)

- `analysis/contract_year.py:38-41` — формула cy_A (нуждается в перепроектировании).
- `analysis/prep.py:51-53` — баг experience fillna(0).
- `analysis/m3.py:50-61` — Δlog regression (нуждается в новой cy_exogenous).
- `analysis/m2.py:25` — dropna(state_tax_rate) — пропадает Toronto.
- `analysis/robustness.py:53-55` — комментарий «undrafted dropping для experience>0» — на самом деле баг другой природы.
- `analysis/METHODOLOGY.md` §5.3 — результаты M3 (требуют пересмотра).

---

## §10. Контрольная фраза для Claude Code

Когда передашь этот план в Claude Code, начни с:

> «Я хочу выполнить план Правок В1 для курсовой работы по NBA salary regression. Контекст и план: `revisions_v1/PROBLEMS.md` и `revisions_v1/IMPLEMENTATION_PLAN.md`. Действуй строго по плану, начиная с §1.1 (contract_year_v1). На каждом шаге: создавай файл, прогоняй, сохраняй verification, лог пиши в `revisions_v1/logs/`. Не трогай `analysis/` (V0) — работай в `analysis_v1/`. Я буду подтверждать переход между шагами или просить пересмотреть подход. Старт.»

Удачи на защите.
