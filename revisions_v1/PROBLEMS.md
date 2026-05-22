# Правки В1 — реестр проблем работы

> Это список всех замечаний по работе после критического review методологии, кода и output-таблиц на ревизии V0 (May 2026).
> Каждая запись содержит: **что обнаружено**, **где конкретно в коде/данных**, **последствия для результатов**, **обязательно ли чинить для защиты курсовой**.
>
> Кодировка статусов:
> - 🔴 **CRITICAL** — без исправления результат недействителен.
> - 🟠 **HIGH** — серьёзно влияет на интерпретацию, исправлять надо.
> - 🟡 **MEDIUM** — методологическая дыра, желательно закрыть, но не блокирует.
> - 🟢 **LOW / cosmetic** — улучшения качества работы.
>
> Приоритеты согласованы с пользователем: курсовая бакалавра, защита через 1–2 недели, методы уровня 3–4 курса.

---

## БЛОК A. Критические ошибки результатов

### A1 🔴 Циркулярность M3c — «canonical contract-year effect» построен на тавтологии

**Где.** `analysis/contract_year.py:38-41` (определение `cy_A`); `analysis/m3.py:50-61` (регрессия M3c).

**Что.** Сигнал `cy_A` = `|s_{t+1}/cap_{t+1} − s_t/cap_t| / |s_t/cap_t| > 0.25` — функция от `s_{t+1}/s_t`. В M3c зависимая `Δln_salary_{t→t+1} = ln(s_{t+1}/s_t)` регрессируется на `contract_year`, в которой `cy_A` доминирует (1005 из ~1430 cy=1).

**Проверка фактов** (на `data_analysis.csv`):

| Группа | N | Mean Δln_salary |
|---|---:|---:|
| `contract_year = 0` | 1014 | 0.064 |
| `contract_year = 1` | 1378 | **0.320** |
| `cy_A = 0` | 1702 | 0.070 |
| `cy_A = 1` | 1005 | **0.344** |
| `cy_B = 0` (без trade) | 1511 | **0.267** |
| `cy_B = 1` (был trade) | 881 | **0.117** ← противоположный знак! |

**Последствия.** Коэффициент M3c +0.296 — арифметическое следствие правила «помечать обсервации с большим |Δsalary|». Гипотеза H6 в текущей форме **не проверена**. Контр-тест по чистому экзогенному сигналу cy_B даёт **противоположный знак** (игроки после trade теряют темп роста зарплаты).

**Действия.** См. план §1.1, §3.

---

### A2 🔴 Бага в `experience` — все 612 undrafted имеют `experience = 0`

**Где.** `analysis/prep.py:51-53`.

**Что.** `df["experience"] = df["experience"].fillna(0)`. Изначально `experience = season − draft_year`, а у undrafted `draft_year = NaN`. После `fillna(0)` — все undrafted, независимо от длительности карьеры, получают `experience = 0`.

**Проверка.** Fred VanVleet наблюдается 8 сезонов (2017–2024), все с `experience = 0`. То же — Calderon и другие undrafted-ветераны.

**Последствия.**
1. Дамми `undrafted` и индикатор `experience = 0` на твоей выборке **тождественны** — drafted имеют `experience ≥ 1`.
2. Коэффициент `experience` идентифицируется только на drafted; интерпретация в METHODOLOGY неточна.
3. R3 («исключены rookies, `experience = 0`») фактически **удаляет все 612 undrafted**, а не «новичков-rookies». Комментарий в коде `robustness.py:53-55` объясняет проблему неверно.
4. Все коэффициенты M1d, M2d, M3d, R3 поплывут после фикса.

**Действия.** План §1.2.

---

### A3 🔴 Toronto Raptors полностью выпадают из M2/M3/R

**Где.** `data/lookups/state_tax.csv` (TOR отсутствует / NaN) → `analysis/m2.py:25` (`dropna(subset=["state_tax_rate"])`).

**Что.** Toronto в Канаде, нет US state tax. 107 наблюдений TOR удаляются при формировании выборки M2/M3/R. При этом combined federal + Ontario provincial top marginal ≈ **53.5%** — **самая высокая** налоговая нагрузка в лиге.

**Последствия.** Идентификация β_state_tax_rate теряет именно те наблюдения, которые имеют наибольшую идентификационную силу (variation наверху распределения). Null-результат H5 может быть артефактом отсутствия high-tax обсерваций.

**Действия.** План §1.3.

---

### A4 🟠 cy_A засчитывает падения зарплаты как «contract year»

**Где.** `analysis/contract_year.py:39`.

**Что.** `df["cy_A"] = (df["real_salary_change"].abs() > A_thresh)`. По модулю → 324 наблюдения из 1005 cy_A=1 имеют **падение** зарплаты > 25%.

**Последствия.**
1. Пул `cy_A = 1` бимодален: молодые на pay raise + ветераны на pay cut. Эти процессы — разные.
2. Огромная гетероскедастичность: `std(Δln_salary | cy=1) = 0.78` vs `std(Δln_salary | cy=0) = 0.07`. Clustered SE не лечат внутрикластерную heteroskedasticity.
3. Содержательно: «контрактный год» канонически — это игроки, претендующие на новый/повышенный контракт. Сюда не должны попадать игроки, чей контракт истёк и которые согласились на меньший.

**Действия.** План §1.1 (вместе с A1 — разделить cy_A на up/down).

---

## БЛОК B. Эконометрические проблемы спецификации

### B1 🟠 Стандартные ошибки только player-clustered

**Где.** Все модели в `m1.py`, `m2.py`, `m3.py`, `robustness.py`: `cov_type="clustered", cluster_entity=True`.

**Что.** Кластеризация только по игроку. Для двумерной панели нужны минимум two-way clustered SE (player × season) или wild cluster bootstrap, особенно с малым числом year-кластеров (9 → стандартный two-way может занижать SE).

**Последствия.** SE по `post_cba_2017`, `post_covid`, `state_tax_rate`, `contract_year` могут быть существенно занижены → завышенная значимость.

**Действия.** План §4.1.

---

### B2 🟠 Мультиколлинеарность combined stats без диагностики

**Где.** `analysis/config.py:26-27`: `COMBINED_STATS = ["ppg", "rpg", "apg", "mpg", "gp", "per", "ws", "vorp", "usg_pct"]`.

**Что.** PER ≈ f(PPG, RPG, APG, TS%, USG); WS ≈ PPG-weighted; VORP = BPM × min%. В одной регрессии — корелляции 0.7+. Никаких VIF / condition number / corr-matrix не показано.

**Последствия.**
1. «Парадоксальный» `PER = −0.025` в M1c интерпретирован как «содержательная мультиколлинеарность», но это просто **переспецификация модели**.
2. Стандартные ошибки на одинокий стат завышены, оценки нестабильны.

**Действия.** План §2.1.

---

### B3 🟠 R²_within < 0 в M1d/M2d/M3d не объяснён содержательно

**Где.** Сравнение в METHODOLOGY §7.8.

**Что.** `R²_within = −0.20` в M1d было списано на «численный артефакт linearmodels». На самом деле это означает: demeaned stats хуже объясняют demeaned ln_salary, чем нулевая модель. Содержательно — within-вариация зарплаты определяется контрактными ступеньками, а не плавной траекторией stats.

**Последствия.** Player FE спецификации не дают «более чистую» оценку — они говорят, что внутри-игроцкая корреляция stat↔salary в твоих данных низка.

**Действия.** План §2.2 + дописать секцию обсуждения.

---

### B4 🟠 Эндогенность stats ↔ minutes ↔ salary

**Что.** Coach allocates minutes по игроку с высоким salary (sunk-cost / investment justification) → больше PPG/RPG → выглядит «продуктивнее». Reverse causality.

**Последствия.** β_stats завышены направлением.

**Действия.** План §2.3 — заменить per-game на per-36, добавить lagged stats.

---

### B5 🟠 Возрастной пик 34.7 года — артефакт коллинеарности (age, age², experience, undrafted)

**Что.** Реальный пик зарплаты в NBA ~29–30. Получено 34.7. Причина — `experience = age − draft_age ≈ age − 21` для drafted; для undrafted `experience = 0` (см. A2). `age` и `experience` смешиваются.

**Последствия.** Интерпретация «inverted-U с пиком 34.7» — неправдоподобна. После фикса A2 пик сдвинется.

**Действия.** План §2.4.

---

### B6 🟡 `fg_pct = −1.13` интерпретирован шатко

**Что.** «Эффект центрового, который мало бросает» — даже после контроля на `pos_C` (как референс) такое объяснение неполно. Скорее всего — selection on backups + multicollinearity с другими shooting %.

**Действия.** План §2.5 — заменить три % на `ts_pct` (true shooting).

---

### B7 🟠 Null-results без power analysis

**Что.** `allstar` SE = 0.06 → MDE ≈ +12%; `state_tax_rate` SE = 0.33 → MDE ≈ +66% дифференциала между Calif. (14.6%) и Texas (0%). Null-результат при таких SE не информативен — мы просто не можем детектировать эффект.

**Действия.** План §4.3.

---

### B8 🟡 Heckman selection не сделан

**Что.** NBA — heavily preselected sample. Оценки β_stats содержат selection bias (Heckman 1979).

**Действия.** Для бакалавра уровня — упомянуть в limitations, не делать. См. план §6 (deferred).

---

### B9 🟡 Heteroskedasticity tests отсутствуют

**Действия.** План §4.2 — Breusch-Pagan / White tests, как complementary diagnostic к cluster-SE.

---

### B10 🟡 Multiple testing correction отсутствует

**Что.** 17+ моделей × ~17 регрессоров = 250+ p-values. Несколько «значимостей» (rpg `*`, gp `**`) на грани — могут быть false positives.

**Действия.** План §4.4 — Bonferroni/BH для основных гипотез H1–H8.

---

## БЛОК C. Спецификационные мелочи

### C1 🟡 Зависимая переменная — `ln(salary)` без cap-deflation

**Что.** Структурный рост cap «вьедается» в year FE, но не отделяется. Лучше — `log(salary / cap_t)` как DV.

**Действия.** План §2.6 — параллельный run на cap-deflated DV для robustness.

---

### C2 🟢 Position C как референс — нетипично

**Действия.** Поменять на PG (план §2.7).

---

### C3 🟡 Multi-position игроки обрезаются до первой роли

**Где.** `prep.py:67`: `df["position"].str.split("-").str[0]`.

**Действия.** План §2.8 — multi-hot dummies.

---

### C4 🟢 Salary cap значения не валидированы из источника

**Действия.** Зафиксировать ссылку (NBA.com / Spotrac) в комментариях `config.py`.

---

### C5 🟡 Trade vs free agency не разделены в `cy_B`

**Действия.** План §1.4 — отделить trade (mid-season) от team change in offseason.

---

### C6 🟡 `gp` как регрессор endogenous

**Действия.** Минимум — обсудить; альтернативно — заменить на `mp_total / 48` (нормализация per 48 minutes).

---

### C7 🟡 `usg_pct` endogenous (определяется тренером)

**Действия.** То же — обсудить как ограничение.

---

### C8 🟡 Returns to stats могут меняться после CBA 2017

**Действия.** План §2.9 — interactions `PPG × post_cba`.

---

### C9 🟠 Jock tax — упомянут в methodology, не сделан

**Действия.** План §3.2.

---

### C10 🟡 Outliers (Curry $51.9M, KD, LeBron) — influence diagnostics нет

**Действия.** План §4.5 — Cook's distance, leverage.

---

### C11 🟠 Quantile regression обязательна

**Что.** Cap structure делает effect concave: top decile упирается в max-contract, bottom — в minimum. Линейная регрессия на conditional mean неверно представляет распределение.

**Действия.** План §5.1 — q-reg на τ = 0.10, 0.25, 0.50, 0.75, 0.90.

---

### C12 🟡 Dynamic panel (lagged ln_salary) — игнорируется

**Действия.** Базовый Arellano-Bond — на уровне 3–4 курса бакалавра уже сложно. Деферим в §6.

---

### C13 🟡 Shooting % NaN → 0 без дамми-флага

**Действия.** План §1.5 — добавить `no_attempts` дамми.

---

### C14 🟡 Selection by hoopshype snapshot availability

**Действия.** План §4.6 — диагностика missingness.

---

### C15 🟢 Hoopshype salary precision (round to $100K)

**Действия.** Упомянуть в limitations.

---

### C16 🟢 F-test poolability — есть в коде, не вынесен в README

**Действия.** План §5.3 — отдельная таблица specification tests.

---

## БЛОК D. Расширения работы (extensions)

### D1 🟢 DiD/event-study вокруг CBA 2017

**Действия.** План §5.2 — простой event-study на уровне 3–4 курса.

---

### D2 🟢 Расширение hoopshype до 2008–2014

**Действия.** Если позволит время — план §5.4. ~7 дополнительных сезонов.

---

### D3 🟢 Spotrac на подвыборку для калибровки cy

**Действия.** План §3.1 — ручная сверка 100–200 наблюдений 2022–2024 sezona.

---

### D4 🟢 Market-size proxy (city population, TV market)

**Действия.** План §5.5 — добавить controls.

---

### D5 — D15 — отложены до магистратуры/статьи (см. §6 плана).

---

## БЛОК E. Документация и воспроизводимость

### E1 🟠 `output/figures/` ПУСТО

**Что.** Нет ни одного графика. Для защиты курсовой обязательны:
- Distribution of ln_salary by season
- Scatter ln(salary) vs PPG / age / mpg with quadratic fit
- Coefficient plot (with 95% CI) для каждой модели
- Predicted vs actual ln_salary
- Residuals plot
- Quantile regression coefficient plot (если C11 сделан)
- Event-study coefficient plot (если D1 сделан)
- Heatmap correlations stats × stats

**Действия.** План §5.6.

---

### E2 🟡 Correlation matrix не выведена в descriptive

**Действия.** План §5.6.

---

### E3 🟡 Counts by season не в README

**Действия.** План §5.6.

---

### E4 🟡 Tests prep.py / contract_year.py не написаны

**Действия.** План §4.7 — минимум 5 простых assertions.

---

### E5 🟠 METHODOLOGY содержит устаревшие интерпретации

**Что.** После фиксов A1–A4, B5 интерпретация раздела 5 и 6 поменяется. Раздел 7 (limitations) тоже надо переписать — некоторые из перечисленных limitations были на самом деле баги, а не теоретические ограничения.

**Действия.** План §5.7 — переписать METHODOLOGY после всех run'ов.

---

## Сводка: что обязательно для защиты vs nice-to-have

### Обязательно (без этого работа теряет смысл)
1. **A1** — снять cy_A из M3c и пересчитать. Это **главное**.
2. **A2** — исправить experience для undrafted и пересчитать все 17 моделей.
3. **A3** — добавить Toronto state_tax_rate (~53.5%) и пересчитать M2/M3/R.
4. **E5** — переписать METHODOLOGY с новыми числами и честной интерпретацией.

### Сильно желательно (повышает оценку)
5. **A4 + C5** — разделить cy_A_up/cy_A_down, cy_B trade/free-agency.
6. **B1** — wild cluster bootstrap для key coefficients.
7. **B2** — VIF + альтернативная M1c с одним advanced stat (VORP).
8. **B5** — фикс коллинеарности age/experience.
9. **C11** — quantile regression (легко на `statsmodels.QuantReg`).
10. **E1** — фигуры (10+ штук).

### Полезно (если есть время)
11. **C9** — jock tax (требует scraping road schedule).
12. **D1** — event-study CBA 2017.
13. **D3** — Spotrac калибровка на 100 наблюдений.

### Отложено для магистратуры
14. Heckman, GMM, IV, расширение к 2008.

---

## Артефакты текущей версии (V0) — что есть на руках

- `analysis/` — 9 .py файлов, ~600 строк кода. Структура чистая.
- `output/tables/` — 22 .txt + 5 .csv (M1*4, M2*4, M3*4, R*5, descriptive, 3 сводных).
- `data/clean/data_merged.csv` — 3660 × 66.
- `data/clean/data_analysis.csv` — 3660 × 81 (после prep + contract_year).
- `analysis/METHODOLOGY.md` — 720 строк, требует переписи раздела 5–7.

После Правок В1 ожидается:
- 30+ output-таблиц (добавятся quantile + event-study + sensitivity к exp-фиксу).
- 12+ фигур.
- Полная переработка METHODOLOGY раздела результатов.
- Новый `pipeline_v1.log` с воспроизводимостью.
