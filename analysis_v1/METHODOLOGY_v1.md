# Детерминанты заработной платы игроков НБА: методология V1

> **Версия V1 (2026-05-12)** — исправление трёх критических ошибок V0 (см. `revisions_v1/PROBLEMS.md`) и расширение диагностик. Преамбула, постановка задач (раздел 1–2), описание данных (раздел 3) и базовая методология (4.1–4.4) остаются прежними — см. `analysis/METHODOLOGY.md`. Здесь переписаны и расширены разделы, отражающие методологические правки V1: **4.5 (contract_year)**, **5 (результаты)**, **6 (интерпретация)**, **7 (ограничения)**, **8 (новые диагностики)**, **9 (заключение)**.

**Период:** 9 сезонов 2015/16 — 2023/24, 3 660 наблюдений, 953 игрока.

---

## 0. Сводка изменений V0 → V1

| Код | Проблема V0 | Правка V1 | Эффект на интерпретацию |
|---|---|---|---|
| **A1** | Циркулярность `cy_A`: определена через `|Δsalary| > 0.25`, и затем `Δlog_salary` регрессируется на `contract_year` (M3c). | Разделены сигналы: `cy_A_up` (+), `cy_A_down` (−), `cy_B_offseason` (free agency, no mid-season trade), `cy_B_trade` (multi-team), `cy_C` (rookie scale). Канонический сигнал — **`cy_exogenous = max(cy_B_offseason, cy_C)`**, не использующий s_{t+1}. | **M3c canonical: β = −0.005, p = 0.84** (V0 показывал +0.296***). Гипотеза H6 не подтверждается. |
| **A2** | `experience = season − draft_year`, для undrafted (`draft_year = NaN`) → `fillna(0)`: все 612 undrafted получали `exp = 0` независимо от длительности карьеры. | Для undrafted: `experience = cumcount + 1` по player_id (нумерация сезонов в выборке). Добавлен `experience_career_total`. | M1a `experience`: 0.006 (ns) → **+0.057*** (p<0.001)**. age_peak: 34.81 (артефакт V0) → **30.59** (правдоподобно для NBA). undrafted: −0.352*** → −0.203*** (вдвое слабее). |
| **A3** | Toronto Raptors (107 obs) выпадали в M2/M3/R из-за `NaN` в `state_tax_rate`. | В `state_tax.csv` добавлены Ontario combined federal+provincial rates: 46.41% (≤2015), 49.53% (2016), **53.53%** (2017+). Флаг `is_canada`. | M2c `state_tax_rate`: −0.36 (SE=0.33) → **+0.15 (SE=0.14)** — SE упала вдвое, но эффект всё ещё статистически неотличим от нуля. |
| **A4** | `cy_A` засчитывает падения зарплаты как «contract year» — 324 из 1005 — pay cuts. | `cy_A_up` и `cy_A_down` разделены. `cy_A_down` **не входит** в `contract_year`. | Composite `contract_year`-сигнал теперь только pay-up (cleaner pool). |
| C5 | `cy_B` смешивал trade и free agency. | `cy_B_offseason` (single→single между сезонами) vs `cy_B_trade` (mid-season multi-team). | R4 теперь тестирует именно free-agency-сигнал. |
| C13 | Shooting % NaN → `fillna(0)` без флага. | Для каждой % колонки создан `no_<col>_attempts` дамми. | Дамми пока не включены в основные модели, доступны для робастности. |
| B5 | Возрастной пик 34.7 года — артефакт `experience = 0` для undrafted. | Фикс A2 + спецификации `M1a_age_only` (age_peak = 34.8 ≈ V0), `M1a_exp_only` (exp_peak = 12.1), baseline `M1a` с обеими (age_peak = 30.6). | Реалистичный пик NBA-зарплаты идентифицирован. |
| B2 | Мультиколлинеарность в `COMBINED_STATS` (per VIF=67, ws VIF=39). | Введена альтернатива `M1c_minimal = [ppg, rpg, apg, mpg, gp, vorp, usg_pct]` без PER/WS. | Без collinear PER/WS, VORP теряет значимость (p=0.88) — V0 коэффициент был «загрязнён». |
| B1 | SE только player-clustered, с 9 годами two-way был бы консервативнее. | Two-way clustering (player × season) для ключевых коэффициентов + wild cluster bootstrap (999 reps) по player_id. | post_cba_2017 SE ×2.08, p 0.000 → 0.002 (всё ещё значимо). |

---

## 4.5. Эвристика contract_year (V1, переработана)

### 4.5.1. Мотивация изменения

В V0 `cy_A = (|real_salary_change| > 0.25)` определял большую часть наблюдений с `contract_year = 1` (1005 из 1378). Однако в M3c зависимой переменной была `Δlog(salary_{t→t+1})` — то есть та же `real_salary_change`. Регрессия Δsalary на индикатор большого |Δsalary| — арифметическая тавтология (corr ≈ 0.71), а не проверка гипотезы. Кроме того, V0 не различал направление (`|·| > 0.25`), сваливая pay raises и pay cuts в одну категорию.

### 4.5.2. Новые определения

Введены 5 независимых сигналов и 2 композита:

| Сигнал | Формула | Семантика | N=1 | NA |
|---|---|---|---:|---:|
| `cy_A_up` | `real_salary_change > +0.25` | повышение cap-share более 25% (циркулярный) | 607 | 1268 |
| `cy_A_down` | `real_salary_change < −0.25` | падение > 25% (НЕ contract year) | 221 | 1268 |
| `cy_B_offseason` | `team_t ≠ team_{t+1}`, ни у t, ни у t+1 не было mid-season trade | free agency / sign-and-trade в межсезонье (экзогенный) | 505 | 1644 |
| `cy_B_trade` | `team_t ∈ {2TM, 3TM, 4TM, TOT}` | mid-season обмен в году t (информативный, но не cy) | 508 | 0 |
| `cy_C` | (draft_round=1 ∧ exp=3) ∨ (draft_round=2 ∧ exp=1) | rookie-scale endpoint (экзогенный) | 320 | 0 |
| **`contract_year`** | max(`cy_A_up`, `cy_B_offseason`, `cy_C`) | composite (баланс между power и эндогенностью) | 1100 | 1483 |
| **`cy_exogenous`** | max(`cy_B_offseason`, `cy_C`) | **canonical: не использует s_{t+1}** | 768 | 1553 |

Multi-team строки (`team_abbr_t ∈ {2TM, 3TM, 4TM, TOT}`) исключены из `cy_A_up/down` и `cy_B_offseason` (salary attribution неоднозначна); итоговые композиты для них NA.

### 4.5.3. Валидация

Проверки в `analysis_v1/contract_year_v1.py::_verify`:

1. `cy_A_up & cy_A_down` пересекаются на 0 наблюдениях (disjoint by construction).
2. **corr(`cy_exogenous`, Δlog_salary) = −0.040** — нет циркулярности.
3. **corr(`cy_A_up`, Δlog_salary) = +0.712** — циркулярность сохраняется (как и должно быть — для контраста).

Эти числа — главная валидация: новая эвристика разделяет канонический сигнал (без circularity) от циркулярного (для иллюстрации).

---

## 5. Результаты по моделям (V1)

Все таблицы — `output/tables_v1/`. Сравнение V0 ↔ V1 — `output/tables_v1/changes_summary.csv`.

### 5.1. M1 — базовая модель

| Спецификация | N | R² | Заметки |
|---|---:|---:|---|
| M1a (pooled, basic) | 3 660 | 0.648 | post_cba +0.219***, post_covid +0.191*** |
| M1b (basic + year FE) | 3 660 | 0.647 | post_cba/covid поглощены year FE |
| M1c (combined + year FE) | 3 660 | 0.646 | VIF проблема: per=67, ws=39 (см. 8.1) |
| M1d (player + year FE) | 3 660 | R²_within = −0.367 | within-вариация stats плохо объясняет within-вариацию salary (см. 6.3) |

**Ключевые сдвиги V0 → V1:**

| Регрессор | V0 β (SE, p) | V1 β (SE, p) | Источник изменения |
|---|---:|---:|---|
| `experience` | 0.006 (0.011, 0.59) | **0.057*** (0.012, 0.000)** | A2: разделены undrafted и rookies |
| `undrafted` | −0.352*** (0.073) | **−0.203*** (0.057)** | A2: half effect был артефактом exp=0 |
| `age` | 0.429*** (0.038) | 0.413*** (0.038) | A2: незначительный сдвиг |
| `ppg` | 0.032*** (0.006) | 0.031*** (0.006) | стабильно |
| `post_cba_2017` | 0.233*** (0.035) | 0.219*** (0.035) | стабильно (но см. §5.4 ниже) |

**Возрастной пик** (M1a baseline с age + experience): `−β_age / (2·β_age²) = 30.59` лет. Правдоподобно для NBA. Без A2 fix (V0): 34.7 — артефакт коллинеарности.

### 5.2. M2 — налог штата

Toronto теперь в выборке (N: 3 045 → 3 152, +107 obs).

| Коэффициент | V0 (SE, p) | V1 (SE, p) | Что изменилось |
|---|---:|---:|---|
| `state_tax_rate` (M2c) | −0.36 (0.33, 0.27) | **+0.15 (0.14, 0.29)** | SE упала вдвое, знак развернулся, но всё ещё null |
| `no_income_tax` (M2b) | −0.011 (0.039, 0.78) | −0.019 (0.039, 0.63) | стабильно null |

Содержательно: **null результат теперь информативен** — MDE (power 0.80) = 0.40 на коэффициенте, что в econ единицах = 21% pre-tax wage shift между Texas (0%) и Toronto (53.5%). Мы могли бы детектировать 21% gross-up — не детектируем. См. §8.3 power analysis.

### 5.3. M3 — contract_year (полностью переписано)

Сравнение спецификаций (`output/tables_v1/M3_all_models.csv`):

| Спецификация | β (`contract_year`/`cy_*`) | SE | p | N | Интерпретация |
|---|---:|---:|---:|---:|---|
| M3a (level, composite cy) | −0.5332 | 0.0246 | <0.001 | 2 177 | H7 selection: cy=1 → roles на коротких контрактах → ниже salary |
| M3b (level + interactions) | см. файл | | | 2 177 | interactions с PPG/PER/allstar |
| M3c (Δsalary, composite cy) | +0.4545 | 0.0219 | <0.001 | 2 124 | **частично циркулярный** (cy_A_up входит в composite) |
| **M3c_canonical (Δsalary, cy_exogenous)** | **−0.0051** | 0.0261 | **0.844** | 2 054 | **Канонический: нулевой эффект** |
| M3c_circular (Δsalary, cy_A_up) | +0.9155 | 0.0208 | <0.001 | 2 124 | арифметическая тавтология (для иллюстрации) |
| M3d (within, composite cy) | −0.4462 | 0.0325 | <0.001 | 2 177 | within: short contracts ассоциированы с низкой salary |

**Главный результат V1.** При устранении циркулярности (M3c_canonical) эффект «контрактного года» **исчезает** (β = −0.005, p = 0.84). MDE при 80% power: |β| ≥ 0.073 (7% Δsalary) — этот порог исключён. То есть **H6 (canonical contract-year effect) не подтверждается** на чистом сигнале.

Циркулярный M3c_circular (β = +0.916) демонстрирует, что V0 результат +0.296 был артефактом конструкции `cy_A`. Композитный M3c V1 (β = +0.455) — промежуточный результат: больше, чем V0, потому что новый `cy_A_up` чище (без pay-cut контаминации), но всё ещё содержит циркулярность.

### 5.4. Робастность к pre-trends: event-study CBA 2017

Регрессия `ln_salary ~ Σ_{τ ≠ −1} β_τ · 1{season − 2018 = τ} + Stats + Controls`:

| τ | β | 95% CI | Интерпретация |
|---:|---:|---|---|
| −2 (2015/16) | **−0.194*** | (−0.272, −0.117) | **Pre-trend есть!** |
| −1 (2016/17) | 0 | ref | |
| 0 (2017/18, CBA effective) | 0.071 | (−0.006, 0.148) | small jump |
| 1 (2018/19) | 0.154** | (0.069, 0.238) | |
| 2 (2019/20) | 0.143** | (0.036, 0.250) | |
| 3 (2020/21, COVID) | 0.209*** | (0.111, 0.307) | |
| 4 (2021/22) | 0.188*** | (0.090, 0.285) | |
| 5 (2022/23) | 0.407*** | (0.314, 0.501) | TV deal renewal |
| 6 (2023/24) | 0.463*** | (0.368, 0.559) | |

**Pre-trend test** (β_{−2} = 0): p < 0.001 — отвергается.

**Содержательная импликация.** V0 интерпретация `post_cba_2017` как чистого DiD-shock некорректна — есть значимый pre-trend (поскольку salary cap уже рос в 2015–17). Это согласуется с тем, что в M1a_cap_share (DV = ln(salary/cap_t)) коэффициент `post_cba_2017` становится **null** (β = −0.020, p = 0.57). То есть **структурный сдвиг V0 был в основном следствием роста cap**, а не самостоятельным CBA-эффектом.

### 5.5. Гетерогенность: quantile regression

M1a на τ ∈ {0.10, 0.25, 0.50, 0.75, 0.90}, cluster bootstrap SE (199 реплик):

| Регрессор | τ=0.10 | τ=0.25 | τ=0.50 | τ=0.75 | τ=0.90 |
|---|---:|---:|---:|---:|---:|
| `ppg` | 0.032 | 0.033 | 0.035 | 0.025 | **0.022** |
| `age` | 0.291 | 0.400 | 0.429 | 0.430 | 0.421 |
| `experience` | 0.082 | 0.098 | 0.091 | 0.068 | 0.051 |
| `undrafted` | −0.197 | −0.133 | −0.157 | −0.124 | **−0.050** |
| `post_covid` | 0.233 | 0.197 | 0.183 | 0.138 | 0.114 |
| `allstar` | 0.037 | −0.054 | −0.060 | 0.010 | −0.023 |

**Содержательно.** `ppg` returns: **concave** (0.032 на τ=0.10 → 0.022 на τ=0.90). Marginal PPG на top decile (max-contract игроки) ценится меньше — упор в cap-ограничение. Это эмпирическое подтверждение cap-induced concavity и обоснование, почему линейная регрессия на conditional mean (M1a) **недопредставляет** картину.

`undrafted` penalty: −0.20 на нижнем дециле → −0.05 на верхнем. Star-level undrafted ветераны (VanVleet и т.п.) пробивают селекционный барьер; на medium-low пуле штраф ощутимый.

`post_covid`: эффект монотонно ослабевает с τ — top decile уже capped, COVID/new TV deal сильнее влияли на middle класс.

### 5.6. Робастность: R1–R5

| Спецификация | β (cy) | SE | N | Комментарий |
|---|---:|---:|---:|---|
| R1 (full, tax + cy) | −0.534*** | 0.025 | 2 177 | cy эффект как в M3a, no_income_tax null |
| R2 (excl <$1M) | стабильно | | 2 008 | не reaches max-contract anchor |
| R3 (excl first-year) | −0.466*** | 0.027 | 1 798 | **A2 fix:** V0 R3 удалял 612 undrafted; V1 R3 — только 379 «настоящих» новичков |
| R4 (`cy_B_offseason` only) | см. файл | | | trade-free сигнал |
| R5 (`cy_A_up` only) | см. файл | | | **циркулярный — для контраста** |

---

## 6. Интерпретация (обновлено)

### 6.1. Что подтвердилось

- **H1 (структурные сдвиги).** Частично. post_cba_2017 значим, но **event-study выявляет pre-trends** (§5.4) → большая часть эффекта — рост salary cap, а не CBA-shock per se. post_covid тоже значим, более устойчив.
- **H2 (производительность).** Per-game PPG значим (0.031***, M1a). Combined stats (M1c) — VIF проблема (см. 8.1); чистая VORP-only спецификация (M1c_minimal) даёт VORP = +0.003 (ns) — Marginal value of advanced stats после control basic stats не идентифицируется.
- **H3 (жизненный цикл).** Подтверждено. age_peak = 30.6 года (V1, после A2 fix). V0 показывал 34.7 — артефакт `experience = 0` для undrafted.
- **H4 (драфт).** Частично. `log_draft_pick` значим в M1a (см. полный summary). `undrafted` ослаблен (−0.20 vs V0 −0.35), потому что V0 mix включал артефакт.
- **H7 (selection by contract type).** Подтверждено. `contract_year = 1` в level (M3a, V1) → β = −0.53*** — игроки в cy в среднем на коротких контрактах, заметно ниже salary.

### 6.2. Что **не** подтвердилось (новые null-результаты)

- **H5 (state tax).** Null. β_state_tax_rate = +0.15 (SE=0.14, p=0.29). MDE 21% pre-tax shift не превышен. Гипотеза gross-up и selection в no-tax штаты эмпирически не подтверждается на наших данных. Это **информативный null** (см. 8.3).
- **H6 (canonical contract-year effect).** **Отвергнут** при устранении циркулярности. β_cy_exogenous = −0.005 (p=0.84), MDE = 7%. На честном сигнале (free agency + rookie-scale endpoint) контрактный год **не даёт** Δsalary boost.

### 6.3. Содержательная интерпретация R²_within = −0.367 (M1d)

Отрицательный within-R² в M1d не является «численным артефактом linearmodels». Это означает: **demeaned stats объясняют within-вариацию ln_salary хуже, чем нулевая модель**.

Содержательная причина — структура NBA salary: контрактные ступеньки (rookie scale, mid-level, max). Within-игроцкая вариация salary определяется в основном **переходами между контрактными ступенями**, а не плавными изменениями stats. Один и тот же игрок может улучшить PPG на 3 пункта без изменения salary (если на середине контракта) или увеличить salary втрое без изменения PPG (если перешёл с rookie на mid-level).

Это согласуется с null-результатом M3c_canonical: контрактный год — формальный момент, но переход от ступеньки к ступеньке к моменту истечения контракта не виден через смену stats.

---

## 7. Ограничения (переписано, честно)

### 7.1. Что было багом, что — content

В V0 раздел 7 смешивал реальные методологические ограничения с тем, что оказалось багом данных. В V1:

- **«Возрастной пик 34.7»** — был не interpretive issue, а артефакт `experience` бага (A2). После фикса: 30.6.
- **«Toronto: low identification»** — был bag в `state_tax.csv` (A3). После фикса: Toronto в выборке.
- **«Эндогенность M3c»** — был не «теоретическая концерн», а реальная циркулярность (A1). После фикса: M3c_canonical β = 0.

### 7.2. Остающиеся методологические ограничения

1. **`cy_exogenous` recall.** Без Spotrac-данных по contract length мы фиксируем contract year по эвристике (team change OR rookie scale endpoint). Истинный contract year по контракту может не совпадать с team move (например, два года mid-level extension без смены команды). False negatives искажают null в сторону нуля. Плановая калибровка на Spotrac 2022–2024 (§3.1) не выполнена из-за технических ограничений на скрейпинг; обсуждено в Limitations.

2. **Heckman selection не сделан.** NBA — heavily preselected sample (попадают игроки, заслужившие контракт). β_stats содержат selection bias. Метод Heckman two-step требует exclusion restriction (фактор, влияющий на selection, но не на salary) — у нас такого нет. Это известное ограничение для уровня курсовой бакалавра.

3. **Эндогенность minutes (B4).** PPG, RPG и т.д. зависят от MPG, которые распределяются тренером. Игроки с высокой salary получают больше минут (sunk-cost логика) → выше per-game stats. Per-36 стандартизация (M1a_per36) частично купирует эту проблему: коэффициент `ppg_per36` остаётся значимым (0.021***), что говорит об устойчивости главного эффекта к minutes-эндогенности.

4. **CBA 2017 — не clean shock.** Event-study выявил pre-trends (β_{−2} = −0.19***). DiD-интерпретация V0 переоценивает CBA-shock. M1a_cap_share спецификация (DV = log(salary/cap)) показывает, что после deflation cap-ростом эффект CBA становится null.

5. **Jock tax (C9) не сделан.** Effective tax rate для каждого игрока — функция home + road games, которые не учтены. Это упрощение state_tax_rate в сторону overstate variation. Если road games смягчают tax differential, наш null может быть консервативным.

6. **Power для null-результатов** (§8.3). State_tax_rate MDE = 21% pre-tax shift — мы могли бы детектировать large effects, но не subtle ones (< 5% gross-up). Поэтому строго говорим **«не находим эффекта 21%+»**, а не «эффекта нет вообще».

### 7.3. Endogeneity (расширено)

Кроме отмеченных выше:

- **Reverse causality salary → stats** (B4). Coach allocates minutes по salary → PPG/RPG inflated for highly-paid. Per-36 (M1a_per36) частично решает: ppg_per36 = 0.021*** (vs ppg = 0.031*** в baseline). Это значит, что часть «эффекта PPG» в baseline — это эффект minutes-allocation.
- **Selection on contract type** (B5). Игроки с разными типами контрактов (rookie scale, mid-level, max, supermax) попадают в выборку по-разному. Это не моделируется явно. Quantile regression (§5.5) частично решает — показывает, что effect структуры salary различается по distribution.
- **Jock tax** уже обсуждено выше.

---

## 8. Диагностики V1 (новый раздел)

### 8.1. Мультиколлинеарность (VIF)

`output/tables_v1/vif_M1c.csv`. Главные нарушения:

| Регрессор | VIF |
|---|---:|
| `age` | 614 |
| `age_sq` | 289 |
| `mpg` | 143 |
| `ppg` | 104 |
| `usg_pct` | 104 |
| `per` | 67 |
| `ws` | 39 |

`age` × `age_sq` — ожидаемо (можно центрировать для устранения). PER, WS — действительно multicollinear с PPG / VORP. **Альтернатива M1c_minimal** (без PER, WS) даёт VORP = +0.003 (p=0.88) — после очистки от collinear coefs, marginal value of advanced stats не идентифицируется.

### 8.2. Гетероскедастичность (Breusch-Pagan, White)

`output/tables_v1/heteroskedasticity_tests.csv`. Все 4 модели (M1a, M1c, M2c, M3c_canonical) отвергают homoskedasticity (BP p < 10⁻¹²). Это методически означает, что cluster-robust SE — необходимый минимум.

### 8.3. Power analysis для null-результатов

`output/tables_v1/power_analysis.csv`. MDE = 2.8 × SE (power 80%, α = 0.05, two-sided):

| Регрессор | β | SE | MDE_β | Econ-interpretation |
|---|---:|---:|---:|---|
| `allstar` (M1a) | −0.011 | 0.061 | 0.171 | MDE = 17% wage premium от All-Star — marginal, V1 не детектирует |
| `state_tax_rate` (M2c) | +0.151 | 0.142 | 0.397 | MDE × 0.535 (Texas → Toronto) = 21% pre-tax shift |
| `no_income_tax` (M2b) | −0.019 | 0.039 | 0.109 | MDE = 11% wage premium for tax-free state |
| `cy_exogenous` (M3c_can) | −0.005 | 0.026 | 0.073 | MDE = 7% Δsalary за contract year — tight bound |

`cy_exogenous` MDE — наиболее жёсткий: мы исключаем эффект > 7%. Это **informative null** — даже small effects были бы обнаружены.

### 8.4. Multiple testing (FDR-Benjamini-Hochberg)

`output/tables_v1/multiple_testing.csv`. 13 ключевых p-values:

- Сильные эффекты M1a (`post_cba`, `post_covid`, `age`, `experience`, `undrafted`, `ppg`) — все проходят FDR.
- `usg_pct` в M1c: raw p = 0.041, BH p = 0.067 — **теряет 5%-significance** после коррекции на multiple testing.
- `state_tax_rate`, `cy_exogenous`, `allstar` — null до и после FDR (ожидаемо).

### 8.5. Influence diagnostics (Cook's distance)

`output/tables_v1/top_influential.csv`. Top-10 most influential: Kevin Garnett 2015/16 (Cook's d = 0.021), Hassan Whiteside, Michael Beasley. Большинство — старые ветераны на нетипичных salary в последних сезонах.

Re-fit M1a без top-10 (`output/tables_v1/M1a_no_outliers_comparison.csv`):
- `undrafted`: −0.203 → −0.167 (Δ = +17.8%)
- `experience`: 0.057 → 0.068 (Δ = +19.3%)
- `post_cba_2017`, `post_covid`, `ppg`, `age`: |Δ| < 5%

Главные эффекты устойчивы; вторичные (undrafted, experience) — слегка чувствительны к outliers.

### 8.6. Sample attrition

`output/tables_v1/sample_attrition.csv`. От 3 660 до 2 054 (M3c_canonical):

| Шаг | N | Drop |
|---|---:|---:|
| 0. data_merged | 3 660 | 0 |
| 1. − multi-team | 3 152 | 508 |
| 2. + dropna regressors | 3 152 | 0 |
| 3. + tax matched | 3 152 | 0 (TOR теперь в выборке) |
| 4. + contract_year obs | 2 177 | 975 |
| 5. + salary_next obs | 2 124 | 53 |
| 6. + cy_exogenous obs | 2 054 | 70 |

Главная потеря — multi-team (508) и контрактный год (975, в основном последний сезон выборки + multi_team_next).

### 8.7. Two-way clustering + wild cluster bootstrap

`output/tables_v1/two_way_clustering.csv`, `output/tables_v1/wild_bootstrap_pvalues.csv`.

Two-way (player × season) clustering vs только player:

| Регрессор | SE ratio | p_player → p_two_way |
|---|---:|---|
| `post_cba_2017` (M1a) | ×2.08 | 0.000 → 0.002 |
| `post_covid` (M1a) | ×2.04 | 0.000 → 0.003 |
| `state_tax_rate` (M2c) | ×0.71 | 0.288 → 0.134 |
| `cy_exogenous` (M3c_can) | ×1.17 | 0.844 → 0.867 |

С 9 годами two-way marginal, но методологически правильнее. Wild cluster bootstrap (999 reps по player_id, Rademacher) подтверждает: post_cba p_boot = 0.000, state_tax p_boot = 0.308, cy_exogenous p_boot = 0.824.

---

## 9. Заключение (V1)

Курсовая работа основана на собранной с нуля панели 3 660 наблюдений × 953 игрока × 9 сезонов (2015/16 — 2023/24). Тестировались 7 гипотез о детерминантах ln(salary) в NBA: производительность (H2), возрастной цикл (H3), драфт-статус (H4), налоговый штат (H5), contract year (H6), selection by contract type (H7), CBA-сдвиги (H1).

**V1 vs V0.** V0 содержал три критических ошибки: циркулярность M3c (A1), баг experience для undrafted (A2), пропавшие Toronto (A3). V1 исправляет все три, перезапускает 17+ моделей, добавляет диагностики (VIF, BP, power, FDR, influence, attrition, two-way clustering, wild bootstrap), альтернативные спецификации (per-36, ts_pct, cap-share, PG-ref, multi-position, CBA interactions), quantile regression, event-study CBA 2017.

**Главные результаты V1.**

- **H1 (структурные сдвиги).** Условно подтверждена. post_cba и post_covid значимы, но event-study выявляет pre-trends → cap growth, а не CBA-shock per se. M1a_cap_share показывает, что после deflation cap-ростом эффект становится null.
- **H2 (производительность).** Подтверждена для per-game stats. Advanced stats (PER, WS, VORP) — VIF проблема; их marginal value неидентифицируется после очистки от collinearity.
- **H3 (жизненный цикл).** Подтверждена. **age_peak = 30.6** — реалистичный пик NBA-зарплаты (V0 показывал 34.7 — артефакт experience-бага).
- **H4 (драфт).** Условно подтверждена. `undrafted` penalty −0.20 (V0 переоценивал до −0.35). Quantile regression: penalty −0.05 на топ-дециле — star-undrafted пробивают селекционный барьер.
- **H5 (налог).** **Отвергнута / null с power analysis.** MDE 21% pre-tax shift не превышен. Toronto в выборке (107 obs) уменьшил SE вдвое, но эффекта всё равно нет. Информативный null.
- **H6 (canonical contract-year effect).** **Отвергнута.** При устранении циркулярности (cy_exogenous) β = −0.005 (p = 0.84), MDE = 7% — даже small effects были бы обнаружены. Главный научный результат V1.
- **H7 (selection by contract type).** Подтверждена. cy=1 в level → β = −0.53 → игроки в cy в среднем на коротких контрактах с низкой salary.

**Содержательный вывод.** Salary cap в NBA жёстко структурирует распределение: max contract anchor сверху, minimum salary anchor снизу. Marginal returns to stats (concave per quantile regression), отсутствие contract-year boost (cap structure уже отыгрывает контрактные циклы) и null tax effect (no gross-up — игроки берут уровень cap) — все эти результаты согласуются друг с другом и описывают NBA salary как **cap-disciplined market** в смысле Rosen (1986) для concave returns.

V0 vs V1 — иллюстрация важности предварительной диагностики. Один баг в `fillna(0)` сдвинул возрастной пик на 4 года; один пропуск в lookup-таблице удалил Toronto и весь верхний хвост tax distribution; одна циркулярная определённость породила «эффект» +30% Δsalary, которого на самом деле нет.

---

## Приложение: Список output-таблиц и фигур V1

**Таблицы** (`output/tables_v1/`):

- M1*4 (M1a-d), M1_all_models.csv
- M2*4, M2_all_models.csv
- M3*6 (включая M3c_canonical, M3c_circular), M3_all_models.csv
- R*5, R_robustness.csv
- alt_M1_comparison.csv (10 альтернативных спецификаций)
- changes_summary.csv (V0 ↔ V1)
- vif_M1a.csv, vif_M1c.csv
- heteroskedasticity_tests.csv
- power_analysis.csv
- multiple_testing.csv
- top_influential.csv, M1a_no_outliers_comparison.csv
- sample_attrition.csv
- two_way_clustering.csv
- wild_bootstrap_pvalues.csv
- quantile_M1a.csv, quantile_M1a_long.csv
- event_study_CBA2017.csv
- specification_tests.csv
- age_peak_comparison.csv

**Фигуры** (`output/figures_v1/`):

- fig_1: salary distribution (log scale)
- fig_2: ln_salary boxplot by season
- fig_3: scatter ln_salary vs PPG
- fig_4: age profile (raw, unconditional)
- fig_5: age profile (partial regression)
- fig_6: M1a–d coefficient plot
- fig_7: M3 coefficient plot (composite vs canonical vs circular)
- fig_8: residuals M1a
- fig_9: predicted vs actual
- fig_10: correlation heatmap (stats × stats)
- fig_11: quantile coefficients β vs τ
- fig_12: event-study CBA 2017 (`event_study_cba2017.png`)
- fig_13: tax distribution by team (Toronto highlighted)
- fig_14: contract_year diagnostic (V0 cy_A vs V1 cy_exogenous)

---

*Последнее обновление: 2026-05-12.*
