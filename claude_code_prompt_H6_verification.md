# Промпт для Claude Code: строгая проверка отвержения гипотезы H6 и составление полноценного отчёта

## КОНТЕКСТ ПРОЕКТА

Ты работаешь с курсовой работой по эконометрике (бакалавриат, 3–4 курс), тема — детерминанты заработной платы игроков NBA. Корень проекта: `/Users/karolina303/Downloads/курсач/`. Изучи **полностью** перед началом работы:

- `analysis_v1/METHODOLOGY_v1.md` — методология V1 (главный файл, к которому будут отсылки)
- `analysis_v1/contract_year_v1.py` — построение сигналов contract year (cy_A_up, cy_B_offseason, cy_C, contract_year, cy_exogenous)
- `analysis_v1/m3_v1.py` — модели M3 (level, interactions, Δsalary composite, **M3c_canonical**, M3c_circular, within)
- `analysis_v1/prep_v1.py`, `analysis_v1/utils_v1.py`, `analysis_v1/run_all_v1.py` — pipeline
- `analysis_v1/diagnostics.py`, `analysis_v1/spec_tests.py`, `analysis_v1/quantile.py`, `analysis_v1/event_study.py`, `analysis_v1/bootstrap.py`, `analysis_v1/m1_alternatives.py`
- `revisions_v1/PROBLEMS.md` — каталог из 30+ замечаний; в первую очередь блок **A1, A4, C5** (всё, что про contract_year)
- `revisions_v1/IMPLEMENTATION_PLAN.md` — план правок V1
- `output/tables_v1/` — все таблицы V1 (в первую очередь `M3*`, `M3_all_models.csv`, `changes_summary.csv`, `power_analysis.csv`, `sample_attrition.csv`)
- `data/clean/data_analysis_v1.csv`, `data/clean/contract_year_v1_diagnostics.csv` — итоговый датасет и его cy-диагностика
- `data/clean/data_analysis.csv` (V0) — для сравнения

Партнёрские брифы и общий план (для понимания исходных гипотез H1–H5):
- `docs/partner_A_brief.md`, `docs/partner_B_brief.md`, `docs/project_plan.md` (находятся в knowledge-папке проекта Claude; если нет в рабочей директории — см. METHODOLOGY_v1.md, раздел 9, где H1–H7 переименованы).

---

## ЦЕНТРАЛЬНАЯ ПРЕТЕНЗИЯ И ЦЕЛЬ ПРОВЕРКИ

В V1 «гипотеза H6 (canonical contract-year effect)» отвергается на основании M3c_canonical: регрессия `Δlog(salary_{t→t+1}) ~ cy_exogenous + controls`, где `cy_exogenous = max(cy_B_offseason, cy_C)`. Получено β = −0.0051, p = 0.844, MDE при 80% мощности ≈ 7% Δsalary. На этом основании M3c_canonical V1 заявляет, что эффект контрактного года **отсутствует**.

**Сильное подозрение:** это отвержение методологически некорректно или, как минимум, не проверяет содержательную гипотезу. Конкретно — следующие восемь линий критики, каждую из которых ты обязан протестировать численно:

### Линия 1. Смысловое несоответствие гипотезы и теста

Гипотеза H1 в исходном плане (партнёрский бриф А, раздел 2; партнёрский бриф B, гипотеза H1) формулируется как: «игроки демонстрируют значимо более высокую производительность (PER, PPG, WS) в последний год контракта при контроле возраста и опыта». Это **гипотеза о производительности**, не о Δsalary. Тест по Stiroh (2007) — это `Performance ~ ContractYear + Controls` (с player + year FE). В V1 этот тест **не проводился** в каноническом виде на cy_exogenous; вместо этого M3c_canonical регрессирует Δsalary на cy_exogenous, что соответствует другой гипотезе («премия за контрактный год в виде salary jump», ближе к H2 «teams overpay»). Проверь — действительно ли M3c_canonical V1 тестирует Stiroh-эффект, или это другая гипотеза, ошибочно записанная под одним лейблом «H6».

### Линия 2. Радикально неполное определение `cy_exogenous`

`cy_exogenous = max(cy_B_offseason, cy_C)`. По коду `contract_year_v1.py`:

- `cy_B_offseason` = 1, если `team_abbr_t ≠ team_abbr_{t+1}` и ни у t, ни у t+1 нет multi-team (mid-season trade). Это **только межсезонный переход в другую команду**.
- `cy_C` = 1, если `(draft_round=1, experience=3)` или `(draft_round=2, experience=1)` — окончание rookie-scale контракта.

Из этого определения **выпадают**:

- **Re-signings с той же командой**. Игрок, у которого в сезоне t истёк 4-летний контракт и который продлевает контракт со своей командой на максимальном уровне, — это **классический контрактный год**, но `cy_B_offseason = 0` (team не изменилась) и `cy_C = 0` (если не rookie scale). В NBA это огромная доля contract years (Curry / GSW, Lillard / POR до перехода, Тейтум / BOS и т.д.).
- **Player option / team option years**. Если игрок отказался от player option и переподписал с той же командой — то же самое: `cy_exogenous = 0`.
- **Extension в середине последнего гарантированного года**. Многие игроки подписывают extension до истечения, оставаясь в той же команде — тоже выпадает.
- **Rookie scale extensions (4-летние)**, которые подписываются до фактического окончания rookie-scale. Это формально не «cy_C-сезон», но это та же контрактная логика.
- **Two-way → standard и rookie-min → veteran-min transitions** также теряются.

Если предполагать, что **значительная доля «истинных» контрактных лет — это re-signings с той же командой**, то `cy_exogenous` имеет **системно низкий recall**. Это значит, что:
- Большая часть наблюдений, помеченных `cy_exogenous = 0`, на самом деле имеет contract_year = 1 (false negatives).
- Эффект на Δsalary размывается — coefficient смещён к нулю.
- Null-результат становится **артефактом плохой проксии**, а не отсутствием эффекта.

### Линия 3. Селекционное смещение в `cy_B_offseason`

`cy_B_offseason = 1` означает «игрок сменил команду в межсезонье». Это сильно **селективная** подгруппа:
- Часть таких переходов — UFA с реальным повышением (выход на рынок, max-money offer).
- Часть — UFA, которых предыдущая команда **не захотела** удерживать на текущей зарплате → переход на **меньшую** зарплату (downward free agency).
- Часть — sign-and-trade с финансовой механикой, которая не отражает контрактного эффекта в чистом виде.

Если в выборке `cy_B_offseason = 1` доминируют **downward-FA** переходы, то Δsalary в среднем **отрицательная или нулевая** даже при сильной content-of-contract «премии за контрактный год». Это **обратный отбор**, который тянет коэффициент к нулю или в отрицательную сторону.

Проверь распределение Δlog_salary внутри `cy_B_offseason = 1` (median, mean, гистограмма, доля положительных Δlog) — если оно бимодально или сильно смещено вниз, это прямое доказательство селекционного смещения.

### Линия 4. Зависимая переменная Δlog_salary смешивает несколько эффектов

`dln_salary = log(salary_{t+1} / salary_t)` подвержена:
- **Структурным ступеням контракта**: rookie scale → mid-level → max — это механические скачки, не «премия за CY».
- **Cap inflation**: рост salary cap год к году инфлирует Δsalary, не относясь к индивидуальному эффекту. (В коде Δlog_salary не корректируется на Δlog_cap явно в M3c_canonical — проверь.)
- **Max-contract anchor**: для уже max-игроков Δsalary при подписании нового контракта ограничена правилами CBA (25%/30%/35% от cap) — это **сжимает** распределение сверху.

Альтернативные DV, которые стоит протестировать:
- `Δsalary_cap_share = (salary_{t+1}/cap_{t+1}) − (salary_t/cap_t)` — устраняет cap inflation.
- `salary_{t+1} / salary_t` без логарифма (multiplicative).
- `salary_next` в level с player FE — это уже спецификация Mincer next-period earnings.

### Линия 5. Выбор контролей включает эндогенные переменные

В X3c_can включены `ppg, rpg, apg, mpg, gp, per, ws, vorp, usg_pct` — это **современная** производительность игрока, которая по гипотезе Stiroh **сама зависит** от contract year. Если CY → ↑performance → ↑salary, то контролируя на performance, ты **поглощаешь** механизм, через который CY действует на salary. Это **bad control problem** (Angrist & Pischke, 2009, ch.3).

Стоит проверить спецификацию **без** stats-контролей: `dln_salary ~ cy_exogenous + age + age_sq + experience + position + year FE`.

### Линия 6. Power analysis не учитывает heterogeneity

MDE = 7% Δsalary — это для **среднего** эффекта по всей выборке. Но:
- Эффект CY может быть концентрирован в подгруппах (молодые на UFA, ветераны на mid-level, не-max игроки).
- Heterogeneous treatment effects при усреднении на нулевую популяцию (которая включает много false negatives — см. Линию 2) дадут нулевой ATE при ненулевых CATE.
- В power analysis нужно отдельно посчитать MDE для **подгрупп**, в которых сигнал чище.

### Линия 7. Сравнение с M3c (composite, β = +0.45, p < 0.001) и M3c_circular (β = +0.92)

V1 интерпретирует M3c_circular = +0.92 как «тавтологию», M3c (composite) = +0.45 как «промежуточное» из-за остаточной циркулярности через `cy_A_up`, и M3c_canonical = 0 как «правду». Но это не единственная интерпретация:
- Альтернативно: cy_A_up захватывает **дополнительные** истинные contract years, которые `cy_exogenous` упускает (см. Линию 2 про re-signings — большая часть из них как раз попадает в cy_A_up).
- В таком случае M3c_composite ≈ 0.45 — это **более правильная оценка**, а M3c_canonical = 0 — артефакт неполного определения.
- Циркулярность через cy_A_up действительно присутствует, но её сила не означает, что cy_exogenous «канонически чище» — она означает, что у нас **две прокси с разными свойствами**: одна с высокой циркулярностью, но высоким recall; другая с нулевой циркулярностью, но низким recall.

### Линия 8. Не была построена внешняя валидация cy_exogenous

В V1 нет ни одной проверки cy_exogenous против внешнего источника contract data (Spotrac, Basketball-Reference contracts). Без неё мы не знаем:
- True positive rate cy_exogenous: какая доля cy_exogenous=1 действительно соответствует contract year по реальным данным?
- False negative rate: какая доля **истинных** contract years имеет cy_exogenous = 0?

---

## КОНКРЕТНЫЙ ПЛАН ПРОВЕРКИ — ВЫПОЛНИТЬ В ЭТОМ ПОРЯДКЕ

### Этап 0. Подготовка

1. Запусти существующий pipeline и проверь воспроизводимость:
   ```bash
   cd /Users/karolina303/Downloads/курсач
   source .venv/bin/activate  # если есть; иначе установи зависимости
   python -m analysis_v1.run_all_v1
   ```
2. Удостоверься, что `data/clean/data_analysis_v1.csv` и все таблицы V1 — те же, что в репозитории.
3. Прочитай `analysis_v1/contract_year_v1.py` целиком и зафиксируй для себя все условия NA, multi-team фильтрации и состав композитов.

### Этап 1. Диагностика самой переменной `cy_exogenous`

Запиши результаты в `output/h6_verification/01_cy_exogenous_diagnostics.csv` и краткий .md-summary.

1. **Распределение по сезонам**: сколько `cy_exogenous = 1` в каждом сезоне; сравни с `contract_year = 1` (composite) и `cy_A_up = 1`.
2. **Распределение по возрасту**: cy_exogenous=1 у молодых (rookie endpoint доминирует) vs ветеранов (offseason move).
3. **Доля компонентов**: сколько cy_exogenous=1 — это `cy_C` (rookie scale endpoint), сколько — `cy_B_offseason` (team change), сколько — оба.
4. **Дельта salary по группам**: median, mean, sd, доля положительных Δlog_salary внутри:
   - `cy_exogenous = 1, cy_C = 1, cy_B_offseason = 0` (только rookie endpoint)
   - `cy_exogenous = 1, cy_C = 0, cy_B_offseason = 1` (только team change)
   - `cy_exogenous = 1, cy_C = 1, cy_B_offseason = 1` (оба)
   - `cy_A_up = 1, cy_exogenous = 0` (захвачен только cy_A_up)
   - `contract_year = 1, cy_exogenous = 0` (composite минус canonical = доля «потерянных» в каноне)
5. **Доля downward-FA**: внутри `cy_B_offseason = 1`, какая доля имеет Δlog_salary < 0 vs > 0 vs близко к нулю?

### Этап 2. Внешняя валидация cy_exogenous (ручная подвыборка)

1. Возьми топ-50 игроков по средней salary за период 2018–2023. Для каждого вручную (через Basketball-Reference contract data, статью на Wikipedia или открытые данные Spotrac, если доступны через WebFetch) собери реальные годы окончания контракта.
2. Сопоставь с `cy_exogenous` и `contract_year` (composite). Посчитай:
   - True Positive Rate (recall): из истинных contract years какая доля имеет `cy_exogenous = 1`?
   - False Positive Rate: из истинных НЕ-contract years какая доля имеет `cy_exogenous = 1`?
   - То же для `contract_year` (composite).
3. Если recall `cy_exogenous` < 60% — это прямое доказательство несостоятельности проксии. Если recall > 85% — претензия из Линии 2 опровергнута.
4. Результаты сохрани в `output/h6_verification/02_external_validation_top50.csv` и `02_validation_summary.md`.

### Этап 3. Альтернативные определения contract year

Построй и протестируй ещё **минимум 5** определений contract year, каждое с явным указанием на: (а) what is captured, (б) what is missed, (в) экзогенность по отношению к Δsalary.

1. **cy_same_team_endpoint**: эвристика, ловящая re-signings с той же командой. Например: `cy_same_team_endpoint = 1`, если `salary_{t+1}/salary_t > 1.2` И `team_t == team_{t+1}` И игрок наблюдался ≥3 сезона с этой командой (чтобы исключить mid-contract bumps). Допускается частичная циркулярность — это и нужно тестировать (см. ниже).
2. **cy_option_year**: дамми года, в котором у игрока был player option / team option. Этим придётся приближать по правилам (например, наличие резкого Δsalary, не объяснимого rookie scale переходами; либо вручную для топ-50).
3. **cy_age_based**: для каждого игрока с непрерывным контрактом >3 лет считаем «контрактный год» — последний год перед известной точкой возобновления контракта по структуре salary (`real_salary_change` лежит в коридоре −0.05…+0.05 несколько лет подряд, затем резко скачет вверх или вниз). Это даёт alternative cy с возможностью включения same-team renewals.
4. **cy_spotrac_top_300**: если есть возможность скрейпинга или ручного ввода контрактных данных с Spotrac для топ-300 — построй чистый cy на этой подвыборке. Если нет — используй имеющиеся данные `data/manual/*` (если есть `contracts_top300.csv` или подобное).
5. **cy_walk_back**: ещё один экзогенный сигнал — для каждого игрока, перешедшего командой между t и t+1 (как в cy_B_offseason), пометить **также** игроков, у которых в t было `salary_{t+1}/cap_{t+1} − salary_t/cap_t > 0.05` И они остались в той же команде (это новые extensions того же игрока, не rookie scale).

Для каждого альтернативного определения — повтори M3c-регрессию в идентичной спецификации, но с заменой DV/control set (Этап 4) и сохрани таблицу.

### Этап 4. Каноническая регрессия Stiroh-эффекта на производительности

**Это главный тест, которого нет в V1.** Гипотеза H1 (исходная) — это `Performance ~ ContractYear`, не Δsalary. Для каждой меры производительности (PER, PPG, WS, VORP, USG%, TS%) запусти:

```
Y_perf_it = α_i + λ_t + β·ContractYear_it + γ·Age + δ·Age² + ε
```

— с two-way FE (player + season), cluster SE по player. Используй **обе** прокси: `contract_year` (composite) и `cy_exogenous`. Дополнительно протестируй спецификации с **взаимодействием** `ContractYear × Age30+` (это исходная H3).

Сохрани полную таблицу со всеми β, SE, p, MDE — `output/h6_verification/04_stiroh_performance_test.csv`.

### Этап 5. Re-test M3c_canonical с устранёнными «bad controls»

Запусти M3c_canonical V1 **без** stats-контролей (только age, age_sq, experience, position, year FE):

```
Δlog_salary ~ cy_exogenous + age + age_sq + experience + pos_dummies + year FE
```

И сравни с оригинальным M3c_canonical (V1, со stats-контролями) и с альтернативной DV `Δsalary_cap_share`.

Сохрани сравнительную таблицу `output/h6_verification/05_m3c_canonical_no_bad_controls.csv`.

### Этап 6. Heterogeneous treatment effects

Протестируй M3c_canonical (и Stiroh-аналог на performance) в **разрезе** подгрупп:

- По возрасту: <25 / 25–28 / 29+
- По salary tier: minimum (<$2M в реальном выражении), mid (2–10M), high (10–25M), max-eligible (>25M)
- По стажу: 1–2 года, 3–6, 7+
- По позиции: G / F / C
- По previous season All-Star статусу

Для каждой подгруппы — β, SE, p, n. Сохрани `output/h6_verification/06_heterogeneous_effects.csv`. Особое внимание: если в любой осмысленной подгруппе β существенно отлично от нуля, **это опровергает** утверждение об отсутствии CY-эффекта в целом.

### Этап 7. Mover analysis на уровне игрока

Внутри игроков, у которых наблюдался ровно один cy_exogenous=1, посмотри:
- Средняя Δlog_salary до и после cy_exogenous=1.
- Event-study coefficients (–3, –2, –1, **0**, +1, +2, +3) с year FE, как в `event_study.py`, но привязка к cy_exogenous, а не к CBA-2017.
- Это — критическая проверка: если эффект в году ContractYear=1 значим и положительный относительно ContractYear=–1, то null-результат M3c_canonical — артефакт усреднения.

Сохрани таблицу и фигуру: `output/h6_verification/07_event_study_around_cy.csv`, `07_event_study_around_cy.png`.

### Этап 8. Power analysis с поправкой на heterogeneity

Для каждой осмысленной подгруппы (Этап 6) посчитай MDE при 80% мощности. Сравни с агрегатной MDE из V1 power_analysis.csv. Сделай вывод: была ли мощность теста M3c_canonical V1 достаточной для **подгрупповых** эффектов.

Сохрани `output/h6_verification/08_power_by_subgroup.csv`.

### Этап 9. Sensitivity: что должно произойти с β_cy_exogenous, чтобы H6 не отвергалась

Используя подход Oster (2019), посчитай:
- Δ — bound, насколько β сдвинется при инклюзии исключённых контролей (если бы они были равны по силе наблюдаемым).
- δ — needed strength of unobserved confounding, чтобы β_observed = 0 был согласован с β_true ≠ 0.

Этот тест даст ответ на главный вопрос: «насколько устойчив null-результат M3c_canonical к мерам отбора, которые мы не наблюдаем?»

Сохрани `output/h6_verification/09_oster_sensitivity.csv`.

### Этап 10. Сводный вердикт

Свести все результаты Этапов 1–9 в один master-файл:

`output/h6_verification/VERIFICATION_RESULTS.md` (~5–7 страниц).

В нём — раздел по каждой линии критики (1–8 из «Центральной претензии») с конкретными числами и выводом:
- ✅ Линия N подтверждена (доказательства такие-то).
- ❌ Линия N опровергнута (доказательства такие-то).
- ⚖️ Линия N неопределённа (доказательства такие-то; требуется дополнительная работа).

В конце — итоговый вердикт по H6: справедливо ли отвергнута; если нет — какая альтернативная спецификация даёт «честный» тест, и каков её результат.

---

## ВТОРОЙ ВЫХОД: ПОЛНОЦЕННЫЙ ОТЧЁТ В АКАДЕМИЧЕСКОМ СТИЛЕ (10 СТРАНИЦ, РУССКИЙ ЯЗЫК)

Параллельно с результатами проверки составь **самостоятельный** отчёт, который будет интегрирован в курсовую работу (главы 2–3). Объём — **~10 страниц** (без титула и приложений; ~3500–4500 слов; учитывая 2400 знаков на страницу для 14pt times new roman 1.5 spacing — целевой объём ~ 30 000 знаков).

Файл: `output/h6_verification/H6_full_report.md` (markdown с математикой через LaTeX inline `$...$` и блочный `$$...$$`).

Дополнительно собери Word-версию (.docx) через python-docx или pandoc: `output/h6_verification/H6_full_report.docx`. Используй академическое форматирование (заголовки 1–3 уровней, нумерация формул, единое цитирование Stiroh 2007 / Berri 2007 / Kahn-Sherer 1988 / Kleven 2013 / Oster 2019 / Angrist-Pischke 2009).

### Структура отчёта

#### 1. Введение и постановка вопроса (1–1.5 стр)

- Краткий обзор контрактной структуры NBA: rookie scale, max contract, mid-level exception, salary cap (с упоминанием CBA 1995 → 2011 → 2017 → 2023).
- Что такое contract year effect: исходно — поведенческая гипотеза Stiroh (2007). Чёткое разделение **двух разных** утверждений:
  - (а) Эффект на производительность: игроки **играют лучше** в последний год контракта.
  - (б) Эффект на заработную плату: команды **переплачивают** за всплеск производительности.
- Что было сделано в V1 проекта и почему отвержение H6 в её текущей формулировке требует ревизии.

#### 2. Данные и сэмпл (1.5 стр)

- Источники: Basketball-Reference (stats, draft), Hoopshype (salary), Tax Foundation (state tax), ручные lookup-таблицы. Период 2015/16 – 2023/24, 9 сезонов.
- Шаги построения панели: scraping (rvest в R), очистка имён через `stringi::stri_trans_general("Latin-ASCII")`, маркировка multi-team строк, фильтрация GP ≥ 20, MP ≥ 5/match, salary > $100 000.
- Финальная панель: 3 660 player-seasons, 953 unique игроков.
- Sample attrition при тесте M3c_canonical: 3 660 → 2 054 (см. `sample_attrition.csv`).
- Описание ключевых переменных: `ln_salary`, `salary_cap_share`, `real_salary_change`, performance metrics (PPG/PER/WS/VORP), demographics, draft variables, contract year proxies.
- Описание построения **всех** cy-сигналов с формальными определениями:
  - $cy^{A_{up}}_{it} = \mathbb{1}\{\frac{s_{i,t+1}/cap_{t+1}}{s_{it}/cap_t} - 1 > 0.25\}$
  - $cy^{B_{off}}_{it}$ — переход между сезонами без mid-season trade
  - $cy^{C}_{it}$ — окончание rookie scale
  - $\text{contract\_year}_{it} = \max(cy^{A_{up}}_{it}, cy^{B_{off}}_{it}, cy^{C}_{it})$
  - $cy^{exo}_{it} = \max(cy^{B_{off}}_{it}, cy^{C}_{it})$
- **Дополнительные** определения из Этапа 3 (cy_same_team_endpoint, cy_option_year, cy_age_based, cy_walk_back) — формальные определения и интуиция.

#### 3. Методология (2 стр)

- Базовая Mincer-модель и её адаптация для NBA: $\ln s_{it} = \alpha + \beta_1 \text{Stats}_{it} + \beta_2 \text{Age}_{it} + \beta_3 \text{Age}_{it}^2 + \beta_4 \text{Exp}_{it} + \gamma' \text{Demographics}_i + \delta_t + \varepsilon_{it}$.
- Спецификации M1–M3 (с явной записью каждой и указанием player FE / year FE / two-way FE).
- Тесты идентификации:
  - F-тест fixed vs pooled
  - LM-тест RE vs pooled (Breusch-Pagan)
  - Hausman-тест FE vs RE
  - Тест Чоу на структурный сдвиг 2017/2020
- Диагностика: VIF, Breusch-Pagan на гетероскедастичность, Cook's distance, RESET Рамсея, Shapiro-Wilk.
- Кластеризация SE: player-level, two-way (player × season), wild cluster bootstrap (999 реплик).
- Квантильная регрессия (Koenker-Bassett, 1978) — для проверки гетерогенности по дециле.
- Event-study спецификация: $\ln s_{it} = \sum_{\tau \neq -1} \beta_\tau \mathbb{1}\{T_{it} = \tau\} + \text{Controls} + \nu_{it}$.

#### 4. Контрактный год: построение проксии и её диагностика (2 стр)

- Подробный академический разбор всех проксий с обсуждением их свойств:
  - Recall vs precision.
  - Циркулярность (cy_A_up).
  - Селекционное смещение (cy_B_offseason → downward FA).
  - Incomplete coverage (cy_exogenous пропускает same-team renewals).
- Корреляции с Δlog_salary (Этап 1) — формальная таблица.
- External validation (Этап 2): TPR / FPR против ручной выборки.
- Финальные рекомендации по выбору **главной** проксии для исходной H1/H6.

#### 5. Результаты тестирования H6 (2.5 стр)

- Таблица 1: M3c V1 (composite, β = +0.45), M3c_canonical (cy_exogenous, β = −0.005), M3c_circular (cy_A_up, β = +0.92), плюс наши новые: M3c_alt1 (cy_same_team_endpoint), M3c_alt2 (cy_age_based), M3c_alt3 (cy_walk_back), плюс спецификация без bad controls. Каждая колонка — β, SE, p, MDE_β.
- Таблица 2: Stiroh-style тест на производительности (Этап 4). PER / PPG / WS / VORP / USG%. Two-way FE. Композитный и канонический контрактный год.
- Таблица 3: Heterogeneous effects (Этап 6) — по возрасту, salary tier, стажу, позиции. Особо выделить те strata, где эффект значим.
- Event-study фигура (Этап 7).
- Oster bound (Этап 9).
- Интерпретация — что значит каждый результат экономически.

#### 6. Сопоставление с литературой (0.5 стр)

- Stiroh (2007) — обнаружил CY effect на производительности, ~3% улучшение, на данных 1980–2002.
- Berri et al. (2007) — overpayment for scoring.
- White & Sheldon (2014), Gaffney et al. (2020) — replication CY-эффекта.
- Kleven et al. (2013) — налоговая нагрузка как baseline для H5.
- Объясни, **где** наш результат сходится / расходится с литературой и почему.

#### 7. Ограничения и направления дальнейших исследований (0.5 стр)

- Recall cy_exogenous (важнейшее).
- Selection by contract type.
- Bad controls problem в Mincer-уравнении.
- Heckman selection для NBA-выборки.
- Перспективы: Spotrac contract data, machine learning approach к разметке CY.

#### 8. Заключение (0.5 стр)

- Главный методологический вывод: **результат «H6 не подтверждается» в V1 является артефактом неполного и эндогенно-нагруженного определения cy_exogenous**, а не свидетельством отсутствия Stiroh-эффекта.
- Конкретный bottom line с числами: при канонической спецификации Stiroh-теста на производительности (или при cy_walk_back / cy_age_based-определении) эффект contract year оказывается ___ [подставить полученное].

#### 9. Приложения

- Полные regression outputs для всех новых спецификаций.
- Список 50 игроков для external validation с реальными контрактными датами и колонкой «совпадает с cy_exogenous (Y/N)».
- R/Python код для всех новых анализов.

---

## ТРЕБОВАНИЯ К СТИЛЮ И ПРОВЕРКЕ

1. **Академический русский язык**, уровень 3–4 курса бакалавриата. Тон — как в журнале «Прикладная эконометрика». Никаких разговорных выражений, никаких неоправданных англицизмов (только устоявшиеся термины: panel-FE, cluster-robust SE, MDE, DiD).
2. **Каждое утверждение** в отчёте подкреплено либо числом из твоих таблиц `output/h6_verification/*`, либо ссылкой на конкретный файл V1, либо литературой. Никаких голословных «возможно», «вероятно», «по всей видимости».
3. **Формулы** — через LaTeX inline и block.
4. **Таблицы** — нумерованные, с подписями, со ссылкой из текста («См. Таблицу 1»).
5. **Каждая критическая претензия должна быть либо подтверждена, либо опровергнута численно**. Не оставляй формулировки вида «может быть проблемой» — либо доказывай, что проблема есть (и приводи β/SE/p), либо доказывай, что её нет.
6. **Не упрощай результат под подтверждение пользовательской интуиции**. Если после всех проверок H6 действительно отвергается (например, и Stiroh-тест на производительности даёт null, и cy_walk_back даёт null, и heterogeneous effects нигде не значимы) — отчёт должен **честно** это сказать и привести MDE, чтобы подтвердить мощность.
7. **Обязательная финальная проверка**: после написания отчёта запусти отдельный шаг — пройдись по нему построчно как ревьюер: проверь, что каждое число воспроизводится из соответствующего CSV, что нет «висящих» ссылок (например, упоминание Таблицы 4, которой нет), что нет противоречий между разделами.

---

## ВЫХОДНЫЕ ФАЙЛЫ (фиксированный список)

В директории `output/h6_verification/`:

1. `01_cy_exogenous_diagnostics.csv` + `01_summary.md`
2. `02_external_validation_top50.csv` + `02_validation_summary.md`
3. `03_alternative_cy_definitions.csv` (mapping каждого определения и каждой обсервации)
4. `04_stiroh_performance_test.csv`
5. `05_m3c_canonical_no_bad_controls.csv`
6. `06_heterogeneous_effects.csv`
7. `07_event_study_around_cy.csv` + `07_event_study_around_cy.png`
8. `08_power_by_subgroup.csv`
9. `09_oster_sensitivity.csv`
10. `VERIFICATION_RESULTS.md` — сводный вердикт по каждой линии критики (5–7 стр)
11. `H6_full_report.md` — полноценный отчёт на русском (~10 стр)
12. `H6_full_report.docx` — конвертация в Word

Все промежуточные .py-скрипты, написанные для этих проверок, положи в `analysis_v1/h6_verification/` с понятными именами (`01_diagnostics.py`, `04_stiroh_test.py` и т.д.).

---

## ПОСЛЕДНЕЕ И САМОЕ ВАЖНОЕ

Подойди к этой задаче как независимый рецензент. Ты **не** должен ни подтвердить, ни опровергнуть интуицию заказчика — ты должен **разобраться**. Если претензии заказчика подтверждаются — приводи численные доказательства и предлагай чёткую исправленную спецификацию. Если претензии оказываются неверны — пиши это прямо и обосновывай, почему M3c_canonical V1 — всё-таки правильный тест.

Не экономь на численных проверках. На моменте, когда сомневаешься «может, пропустить эту проверку» — **не пропускай**. Это курсовая работа, которая будет защищаться, и любая дыра в методологии будет видна научному руководителю.

Начни с того, что прочитаешь все указанные в первом разделе файлы. Только потом приступай к Этапу 0. Документируй каждый шаг.
