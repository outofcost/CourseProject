# TODO v3 — самостоятельный рабочий лист к plan3.md

Чек-лист для автономной работы: каждая задача описана с командами, ожидаемыми артефактами, self-check'ами, регресс-тестами и fallback'ом. Все галочки `[ ]` ставлю по мере выполнения. Логи валидаций пишу в `analysis_v2/logs/`, репорты — в `analysis_v2/reports/`.

Принципы:
- **Регресс**: после каждого расширения данных прогоняю replication-test на M1a–M3d из v1. Любое расхождение коэффициента > 1e-6 после round-trip merge — это баг, до фиксации не двигаюсь дальше.
- **Sanity-first**: для каждой новой переменной — distribution, coverage, известные «якорные» значения (LAL должен быть top-3 market, Curry должен быть supermax-tier в 2017+, и т. д.).
- **Источники**: если основной источник недоступен или неполный — самостоятельно ищу 2 альтернативы и сверяю между собой. Список альтернатив фиксирую в `version 3/sources_log.md`.
- **No silent failures**: каждый scraper логирует HTTP-status, retry, anti-join. NA не «глотаю» — каждый NA либо обоснован, либо чиню парсинг.

---

## Фаза 0 · Подготовка инфраструктуры (0,5 дня)

- [ ] **0.1** Создать дерево каталогов `analysis_v2/` (точно по структуре plan3.md строки 65–80). Зеркалировать `analysis_v1/` как стартовую точку для prep/utils.
  - команда: `cp -r analysis_v1 analysis_v2 && rm analysis_v2/{m1_v1,m2_v1,m3_v1,robustness_v1,prep_v1}.py` (переименую далее)
  - self-check: `ls analysis_v2/` показывает структуру с подпапками `data_collection/`, `output/`, `logs/`, `reports/`.
- [ ] **0.2** Создать `analysis_v2/sources_log.md` — журнал ссылок, дат скрейпа, fallback-источников, причин выбора. Один блок на каждую новую переменную.
- [ ] **0.3** Создать `analysis_v2/coverage_log.csv` — таблица с колонками `variable, source, n_total, n_covered, coverage_pct, run_date, notes`. Пишется автоматически из prep_v2.py.
- [ ] **0.4** Smoke-test существующего scraper'а bbref: `python3 -m nba_scraper selftest --season 2024` должен пройти. Если bbref снова за Cloudflare — поднимаю pin'нутую версию `curl_cffi`, проверяю что `impersonate='chrome'` работает на тестовом GET `/players/c/curryst01.html`.
- [ ] **0.5** Зафиксировать снимок `data/clean/data_analysis_v1.csv` через `sha256sum` в `analysis_v2/reports/v1_snapshot.sha256` — это якорь для регресс-тестов.

---

## Фаза 1 · Сбор недостающих данных (приоритет 1)

### Блок 1.1 — Birth country / international (≈3 ч)

- [ ] **1.1.1** Открыть `nba_scraper/bbref.py` → найти `parse_player_page` (если нет — найти ближайшую функцию, парсящую meta-блок). Если функция отсутствует — написать новую в `analysis_v2/data_collection/scrape_birth_country.py`.
- [ ] **1.1.2** Реализовать парсинг блока `#meta` со страницы `/players/{letter}/{player_id}.html`. Извлечь:
  - `Born:` — дата (для верификации возраста), город, страна.
  - Country хранится как `<span itemprop="birthPlace">` → последний `<a>` обычно ведёт на `/friv/birthplaces.fcgi?country=XX`.
- [ ] **1.1.3** Source-search fallback: если bbref-страница недоступна или поле пустое — попробовать:
  1. NBA.com player profile (`stats.nba.com/player/{id}` через `curl_cffi`), смотреть `playerBio`.
  2. Wikipedia infobox через `https://en.wikipedia.org/wiki/Special:Search?search={firstname}+{lastname}+NBA`.
  3. RealGM player page (`basketball.realgm.com/player/{id}`).
  - Логировать выбранный fallback в `sources_log.md`.
- [ ] **1.1.4** Кэширование: HTML-файлы класть в `data/raw/bbref_players/` (rate-limit 3 sec), повторный запуск не должен ходить в сеть.
- [ ] **1.1.5** Output: `data/clean/birth_country.csv` с колонками `player_id, birth_country, birth_city, birth_date, is_international`.
- [ ] **1.1.6 [SELF-CHECK]** Покрытие = 100% (3660/3660). Если < 100% — anti-join в `logs/unmatched_birth_country.csv`, ручной разбор каждой строки.
- [ ] **1.1.7 [SANITY]** Распределение по странам:
  - USA должно быть ≈70–75% (тренд: 75% в 2016 → 70% в 2024).
  - Топ non-USA: Canada, France, Australia, Serbia, Spain, Nigeria, Germany.
  - Якорные точки: Curry → USA, Doncic → Slovenia, Embiid → Cameroon, Jokic → Serbia, Antetokounmpo → Greece, Wembanyama → France.
  - Если ≥5 якорей неверны — баг парсинга, перепроверяю.
- [ ] **1.1.8 [SANITY]** Все 30 NBA-команд должны иметь хотя бы 1 international игрока за весь период (нет «команды-исключения»).

### Блок 1.2 — All-NBA, All-Defensive, MVP, DPOY (≈4 ч)

- [ ] **1.2.1** Скрипт `analysis_v2/data_collection/scrape_awards.py`. Источник: `https://www.basketball-reference.com/awards/all_league.html` (All-NBA), `/awards/all_defense.html`, `/awards/mvp.html`, `/awards/dpoy.html`.
- [ ] **1.2.2** Источник fallback: если bbref упал — `https://en.wikipedia.org/wiki/All-NBA_Team` имеет таблицу по сезонам; парсинг через `pandas.read_html`. NBA.com `/history/awards` — третий запасной.
- [ ] **1.2.3** Привязка к игрокам: bbref даёт ссылки на player-id прямо в таблице (`<a href="/players/c/curryst01.html">`). Использовать href, не имя.
- [ ] **1.2.4** Output: `data/clean/awards_panel.csv` с колонками `player_id, season, all_nba_team (0/1/2/3), all_defense_team (0/1/2), mvp (0/1), dpoy (0/1)`.
- [ ] **1.2.5 [SELF-CHECK]** В каждом сезоне:
  - ровно 15 игроков с `all_nba_team != 0` (5+5+5),
  - ровно 10 с `all_defense_team != 0` (5+5),
  - ровно 1 MVP, 1 DPOY.
  - Если число другое — ошибка scrape (например, склеились две таблицы). Не двигаюсь дальше, пока не сойдётся.
- [ ] **1.2.6 [SANITY]** Якорные значения:
  - 2015/16 MVP = Curry (unanimous), DPOY = Kawhi Leonard.
  - 2022/23 MVP = Embiid, DPOY = Jaren Jackson Jr.
  - Westbrook должен иметь MVP 2016/17 и быть в All-NBA First Team тот же сезон.

### Блок 1.3 — Derive: lag, cumulative, supermax_eligible (≈2 ч)

- [ ] **1.3.1** Скрипт `analysis_v2/derive_awards_features.py`. Принимает `awards_panel.csv` + базовую панель.
- [ ] **1.3.2** Производные:
  - `all_nba_lag1` — статус прошлого сезона.
  - `career_all_nba_count` — кумулятив **до t-1** (важно: до, не включая, иначе утечка таргета).
  - `career_allstar_count` — то же из существующего `allstar`.
  - `supermax_eligible_t`: согласно CBA 2017 — игрок eligible если (a) all-NBA в t-1, или (b) all-NBA в ≥2 из последних 3 сезонов, или (c) MVP в t-1, или (d) DPOY в t-1, **И** опыт 7–9 лет, **И** в той же команде, что задрафтовала (или получен по трейду до 4-летия). Последние два условия — отдельно: `supermax_eligible_strict` (все условия) и `supermax_eligible_loose` (только awards).
- [ ] **1.3.3 [REGRESS]** Cumulative count'ы для Curry: после сезона 2014/15 (всего 1 all-star, 0 all-NBA), после 2015/16 (2 all-star, 1 all-NBA First), после 2016/17 (3 all-star, 2 all-NBA First). Сверить руками.
- [ ] **1.3.4 [SANITY]** `supermax_eligible_loose == 1`: ~15–20 игроков в сезон (после 2017/18, до этого = 0 т.к. CBA 2017 ввела designated veteran extension). Якорные supermax-контракты: Curry (2017), Wall (2017), Westbrook (2017), Harden (2017), James (2018), Lillard (2019), KAT (2018), Antetokounmpo (2020), Jokic (2022), Booker (2022), Embiid (2022).

### Блок 1.4 — Market size (≈2 ч ручной работы)

- [ ] **1.4.1** Создать `analysis_v2/data_collection/manual_market_size.csv` — ровно 30 строк (по одной на команду), без сезонной разбивки (предполагаем стабильность; релокация Seattle→OKC за пределами выборки).
- [ ] **1.4.2** Колонки: `team_abbr, team_full, dma_rank, dma_households_millions, msa_population_millions, top5_market (0/1), top10_market (0/1), media_market_revenue_proxy`.
- [ ] **1.4.3** Источники (заполнять параллельно, сверять):
  1. Nielsen DMA Rankings 2023/24 (есть в Википедии «List of US television markets»).
  2. US Census MSA population 2020.
  3. Для Toronto — Greater Toronto Area population (Statistics Canada).
- [ ] **1.4.4 [SANITY]** Якорные ранги: NYC = 1, LA = 2, Chicago = 3, Philadelphia = 4, SF Bay = 5, Memphis ≈ 50+ (наименьший в NBA), New Orleans, OKC, Utah, Milwaukee — bottom-tier. LAL/LAC/NYK/BKN/CHI/GSW = top5_market.
- [ ] **1.4.5** Опционально: добавить `state_income_tax_rate` от team_state — это пересечётся с уже имеющимися данными о налогах, использовать как валидацию (FL/TX/NV/TN/WA — 0%).

### Блок 1.5 — Contract tier classifier (≈6 ч)

- [ ] **1.5.1** Собрать lookup-таблицу CBA-thresholds: `analysis_v2/data_collection/cba_thresholds.csv`. Колонки: `season_end_year, cap, luxury_tax, mle_taxpayer, mle_nontaxpayer, biannual, max_25_pct, max_30_pct, max_35_pct, min_salary_0yrs, min_salary_10yrs`.
- [ ] **1.5.2** Источники:
  - Coon's CBA FAQ (`cbafaq.com`) — главный, для каждого сезона.
  - bbref `/contracts/salary-cap-history.html` — для cap & tax line.
  - HoopsRumors archive — для MLE и max-tier чисел.
  - Sportac (если доступен без VPN) — для проверки.
- [ ] **1.5.3 [SANITY]** Cap должен расти монотонно (за исключением 2020/21 — flat из-за COVID). 2015/16 = $70M, 2016/17 = $94M (скачок из-за TV deal — это «cap spike»), 2023/24 ≈ $136M.
- [ ] **1.5.4** Реализовать `analysis_v2/classify_tier.py` по логике из plan3.md строки 16–29. Дополнения:
  - tier'ы строго упорядочены: `minimum < rookie_scale < mid_level < high_mid < max_25 < max_30 < max_35 < supermax`.
  - Учитывать `multi_year_contract` если есть данные (для rookie scale важна года 1–4, не только опыт).
- [ ] **1.5.5 [VALIDATION]** Ручная разметка топ-30 игроков по cumulative earnings — кросс-проверить с автомат-классификацией. Допустимо расхождение ≤ 10% (3 из 30); больше — править пороги.
- [ ] **1.5.6 [SANITY]** Распределение по tier на сезон:
  - rookie_scale: ~120–150,
  - minimum: ~80–120,
  - mid_level: ~80–120,
  - max_25/30/35: ~10–25 суммарно,
  - supermax: 0 в 2015/16 (не существовал), 1–3 в 2017/18, 5–10 к 2023/24.
- [ ] **1.5.7 [FALLBACK]** Если rule-based выдаёт >10% «overpay» — это означает, что cap-share превышает max-pct, что физически невозможно. Проверить cap_t в panel'и; вероятно используется некорректный год.

### Блок 1.6 — Team-level: win %, playoffs, cap commitment (≈6 ч, приоритет 2)

- [ ] **1.6.1** Скрипт `analysis_v2/data_collection/scrape_team_records.py`. Источник: bbref `/teams/{TEAM}/{YEAR}.html`, поля Record (W-L), Pace, ORtg, DRtg, Playoff result.
- [ ] **1.6.2** Output: `data/clean/team_season.csv` с колонками `team_abbr, season, wins, losses, win_pct, made_playoffs, playoff_round_reached (0=missed, 1=R1, 2=Conf semis, 3=Conf finals, 4=Finals, 5=Champion), conf_seed`.
- [ ] **1.6.3** Лаги: добавить `team_win_pct_lag1`, `team_made_playoffs_lag1`.
- [ ] **1.6.4** Cap space proxy:
  - агрегировать существующую панель: для каждой `(team_abbr, season)` сумма `salary_usd` всех ростер-игроков.
  - `team_cap_space_t = cap_t − team_salary_committed_t` (может быть отрицательным = over the cap, что норма).
  - `team_over_luxury_tax_t = (team_salary_committed_t > luxury_tax_t)` из CBA-thresholds.
- [ ] **1.6.5 [SANITY]** GSW в 2016/17 = 67 wins (рекорд), made finals (lost). Cleveland 2015/16 = champion. Sumcheck: для каждого сезона sum of wins по всем командам = sum of losses (с поправкой на 30 команд × 82 game / 2; для 2019/20: 71–72 games, 2020/21: 72).
- [ ] **1.6.6 [SANITY]** Cap space: топ-команды по committed salary — Warriors 2018–2020, Nets 2021–2023 (KD/Harden/Kyrie). Должны быть deeply over the tax.

### Блок 1.7 — Durability / games missed (≈1 ч, derived)

- [ ] **1.7.1** Скрипт `analysis_v2/derive_durability.py`. Логика: `games_missed_t = season_length_t − games_played_t`, где `season_length`: 82 (норма), 72 (2019/20 регулярка прервана, у разных команд 64–67), 72 (2020/21 укороченный), 82 (с 2021/22). Уточнить 2019/20: использовать реальное число сыгранных команд (max games per team).
- [ ] **1.7.2** Производные:
  - `games_missed_lag1`,
  - `games_missed_3y_cumulative` (сумма за t-1, t-2, t-3),
  - `gp_pct_t = games_played_t / season_length_t` (как непрерывная альтернатива).
- [ ] **1.7.3 [SANITY]** Игрок с games_played = 82 → games_missed = 0. Игрок с games_played = 5 в обычный сезон → games_missed = 77 (тяжёлая травма, маркер). Распределение: median ≈ 15–20 missed games.
- [ ] **1.7.4 [SANITY]** Сезон 2019/20: max games_played по panel = 75 (или близко), не 82. Если в данных встречается 82 — значит season_length применён неправильно.

### Блок 1.8 — Agency (приоритет 3, опционально, ≈10 ч)

- [ ] **1.8.1** Решение go/no-go: если на конец фазы 1 priority 1 закончен и есть запас 1+ день — делать; иначе пропустить и записать в риски.
- [ ] **1.8.2** Источник 1: Hoopshype `/agents/` (current snapshot + Wayback за каждый сезон).
- [ ] **1.8.3** Источник 2 (fallback): RealGM agent page, Forbes top-100 agents, manual поиск top-100 игроков.
- [ ] **1.8.4** Output: `data/clean/agency_panel.csv` (player_id, season, agency, agency_tier, klutch_dummy).
- [ ] **1.8.5 [SANITY]** LeBron James → Klutch с 2012; AD → Klutch; Westbrook → Excel/then Wasserman. Известные Klutch-clients (PG, Trae, Zion, JJJ) должны быть отмечены.
- [ ] **1.8.6 [COVERAGE BUDGET]** Если coverage < 60% даже на top-300 — отбрасываем переменную, пишем в риски (правило: переменная с coverage <60% не идёт в regression — слишком много NA).

### Блок 1.9 — Jersey sales rank (приоритет 3, ≈3 ч)

- [ ] **1.9.1** NBA.com press releases по сезону: `https://pr.nba.com/{season}-top-jerseys/`. Также можно через web.archive.org для прошлых сезонов.
- [ ] **1.9.2** Source-search: если NBA.com скрывает архив — Forbes, ESPN, SI публиковали top-15 jersey lists в end-of-season обзорах.
- [ ] **1.9.3** Output: `data/clean/jersey_sales_top15.csv` (player_id, season, jersey_rank). 9 сезонов × 15 = ~135 строк.
- [ ] **1.9.4 [SANITY]** Curry, LeBron, KD — должны быть в top-5 почти каждый сезон. Doncic появляется с 2018/19 и быстро растёт.

---

## Фаза 2 · Интеграция и валидация (3 дня)

### Блок 2.1 — Merging pipeline

- [ ] **2.1.1** Написать `analysis_v2/prep_v2.py`. Логика:
  1. Загружает `data/clean/data_analysis_v1.csv` как базу.
  2. Последовательно left-join'ит каждый новый источник.
  3. После каждого join'а — logging coverage и anti-join'ов.
  4. Сохраняет `data/clean/data_analysis_v2.csv`.
- [ ] **2.1.2** Хэш-проверка: SHA256 базового файла v1 должен совпасть с фиксированным в `v1_snapshot.sha256` (см. **0.5**). Если не совпадает — кто-то правил v1, останавливаюсь и разбираюсь.
- [ ] **2.1.3** Каждый left-join обёрнут в функцию `safe_join(left, right, on, name)`, которая:
  - проверяет, что у `right` нет дубликатов по ключу (`right.duplicated(on).sum() == 0`),
  - после join проверяет, что `len(result) == len(left)` (нет fan-out),
  - пишет в `coverage_log.csv` метрику покрытия,
  - если покрытие < ожидаемого (см. таблицу ниже) — raise или warning + сохранение anti-join.

| Переменная | Ожидаемое покрытие |
|---|---|
| birth_country | 100% |
| all_nba_lag1 | ≥85% (NA только для season=2016 если нет lag-данных за 2015) |
| supermax_eligible_loose | 100% (после 2017, до — 0) |
| market_size | 100% |
| contract_tier | 100% |
| team_win_pct_lag1 | ≥95% |
| games_missed_lag1 | ≥95% |

### Блок 2.2 — Descriptive валидация (День 2)

- [ ] **2.2.1** Скрипт `analysis_v2/validation_v2.py`. Для каждой новой переменной выводит:
  - `describe()` (mean, std, min, max, quartiles),
  - cross-tab по сезонам,
  - cross-tab по позициям,
  - топ-10 / bottom-10 игроков по value.
- [ ] **2.2.2 [SANITY-CHECKS, чек-лист]**
  - [ ] `is_international.mean()` ∈ [0.22, 0.32] и **растёт** от 2016 к 2024.
  - [ ] `all_nba_t.value_counts()`: ровно 15 ненулевых на сезон.
  - [ ] `mvp.sum()` per season == 1 для каждого сезона.
  - [ ] `supermax_eligible_loose.sum()` по сезонам: 0 в 2016/17, монотонный рост до ~20 к 2023/24.
  - [ ] `contract_tier`: распределение монотонно убывает от minimum/rookie_scale к supermax.
  - [ ] `team_win_pct` median ≈ 0.5, std ≈ 0.15, min ≥ 0.1, max ≤ 0.85.
  - [ ] `market_size_rank` корреляция с `top5_market`: |ρ| ≈ 0.6+ (top5 ↔ low rank).
  - [ ] `games_missed_lag1` median ≈ 15–25, тяжёлый правый хвост.
- [ ] **2.2.3** Корреляционная матрица всех новых + старых главных регрессоров. Сохранить в `reports/correlation_matrix_v2.png`. Флажки на |r| > 0.85 — это коллинеарность, требует решения (drop / PCA / interaction).
- [ ] **2.2.4** VIF для финального M1c-full спецификейшена. VIF > 10 для PER+WS — ожидаемо, держим только одно. Для всего остального > 10 — drop.

### Блок 2.3 — Регресс-тест (День 3) ⚠ КРИТИЧНО

- [ ] **2.3.1** Скрипт `analysis_v2/regress_test_v1.py`. Прогоняет на `data_analysis_v2.csv` **существующие** M1a, M1b, M2a, M2b, M2c, M3a, M3b, M3c, M3d **без новых регрессоров** (только переменные, уже бывшие в v1).
- [ ] **2.3.2** Сравнить каждый коэффициент с `analysis_v1/output/*.txt`. Допуск: abs(diff) < 1e-6 для коэффициента, abs(diff) < 1e-4 для SE.
- [ ] **2.3.3** Если хоть один коэффициент расходится:
  1. STOP, не идти в фазу 3.
  2. Проверить, не изменилось ли N в фильтре (например, левый join случайно завёл новые строки).
  3. Проверить, что переменные prep_v1 не были переопределены в prep_v2.
  4. Запустить `compare_v0_v1.py`-стиль diff между `data_analysis_v1.csv` и `data_analysis_v2.csv` колонкам, что были до v2 расширения — они должны быть identical.
- [ ] **2.3.4 [SUCCESS]** Все 9 моделей реплицируются — пишу `validation_report_v2.md` с таблицей «old vs new coeff, SE, N» и зелёным статусом.

### Блок 2.4 — Финал фазы 2

- [ ] **2.4.1** Снапшот: `data/clean/data_analysis_v2.csv` фиксирую через `sha256sum > analysis_v2/reports/v2_snapshot.sha256`.
- [ ] **2.4.2** Заполнить `version 3/sources_log.md` для всех 9 источников: ссылка, дата скрейпа, fallback, sanity-якоря.

---

## Фаза 3 · Эконометрический анализ (7 дней)

### Блок 3.1 — M1c-full и M1d-full (Дни 1–2)

- [ ] **3.1.1** Скрипт `analysis_v2/m1_full.py`. Расширяет `analysis_v1/m1_v1.py`: добавляет Demo + Market + Awards + Durability + Team блоки.
- [ ] **3.1.2** Спецификации (фиксированный порядок переменных в output table):
  - M1c-full (pooled OLS + year FE),
  - M1d-full (two-way FE: player + season),
  - M1c-full_no_collinear (после VIF > 10),
  - M1c-full_logit_robust (Driscoll-Kraay SE как робастность, опционально).
- [ ] **3.1.3** Cluster SE по `player_id` для всех. Для M1d-full также вычислить FE-only result и проверить, что time-invariant переменные (market, is_international) выпали с предупреждением, а не молча.
- [ ] **3.1.4 [REGRESS]** В M1c-full коэффициенты старых переменных (ppg, mpg, age) не должны меняться по знаку или порядку величины относительно v1 M1c. Если меняется — это либо реальный confounding new var → old var (содержательно), либо баг. Принимаю только если контролируемо: «коэф ppg упал с 0.04 на 0.03 после добавления all_nba_lag1, потому что all-NBA коррелирует с ppg» — это нормально. Если упал на 0.001 — что-то сломалось.
- [ ] **3.1.5 [SANITY]** Знак `all_nba_lag1` положительный, существенный (по величине больше, чем коэф allstar). Знак `games_missed_lag1` отрицательный. Знак `top5_market`: ожидается 0 или слегка положительный.

### Блок 3.2 — Декомпозиция вариации (День 3)

- [ ] **3.2.1** Скрипт `analysis_v2/h_decomposition.py`.
- [ ] **3.2.2** Sequential R² по 8 блокам в порядке plan3.md строки 122. Сохранить таблицу `output_v2/tables/r2_decomposition.csv`.
- [ ] **3.2.3** Bootstrap CI: 200 реплик, resampling кластеров `player_id`. Записать lower/upper 95% для каждого ΔR².
- [ ] **3.2.4 [SANITY]** Сумма ΔR² должна равняться R² финальной полной модели (с точностью до 1e-10). Если нет — баг в incremental fit.
- [ ] **3.2.5 [SANITY]** Performance block (ppg, apg, mpg, per, ws) должен давать самый большой ΔR² (≈ 50–60% от R² финальной). Awards block ΔR² должен быть > 0 (формальная гипотеза H10).
- [ ] **3.2.6 [ROBUSTNESS]** Альтернативный порядок: добавить блоки в обратном порядке (Team → Performance), сравнить ΔR². Если результаты дико разные — это shows order-dependence (что мотивирует Shapley в 3.2.7).
- [ ] **3.2.7 [OPTIONAL]** Shapley decomposition — 2^8 = 256 регрессий. Использовать pure Python loop с itertools.combinations. На output `output_v2/tables/r2_shapley.csv`. Если время позволяет.

### Блок 3.3 — H8: Market size (День 4)

- [ ] **3.3.1** Скрипт `analysis_v2/h8_market.py` — M8a, M8b, M8c, M8d (см. plan3.md строки 131–138).
- [ ] **3.3.2** Cluster SE по `player_id`. Wild cluster bootstrap для маргинальных коэффициентов интеракций (M8c, M8d). 1000 реплик.
- [ ] **3.3.3 [SANITY]** В M8b: `market_size_rank` (1 = крупнейший) → ожидаемый знак отрицательный (меньше ранг = больше зарплата) **если** есть market premium. NULL — тоже валидный результат, согласно Hembre (2021).
- [ ] **3.3.4** Интерпретация: если intercept в M8c показывает, что для не-allstar в top5 markets зарплата выше — это marketability канал; если только для allstar — это «star tax / star bonus». Это идёт прямо в обсуждение.

### Блок 3.4 — H9: Tier структура (День 5)

- [ ] **3.4.1** Скрипт `analysis_v2/h9_tier.py` — M9a, M9b, M9c.
- [ ] **3.4.2** Tier-specific regressions: внутри каждого tier'а отдельная Mincer-модель. Сохранить таблицу с коэф ppg внутри каждого tier'а.
- [ ] **3.4.3 [SANITY]** β_ppg должен быть высоким внутри mid_level (рыночная зона) и низким внутри max_25/max_30/max_35 (truncation by cap) и rookie_scale (зарплата по slot).
- [ ] **3.4.4 [SANITY]** R² внутри tier-specific регрессий должен быть ниже общего (less variation внутри одной tier). Если R² внутри tier > общего — баг.
- [ ] **3.4.5** Иллюстрация: график β_ppg(tier) — это войдёт в Главу 5.

### Блок 3.5 — H10: Awards channel (День 6)

- [ ] **3.5.1** Скрипт `analysis_v2/h10_awards.py` — M10a, M10b.
- [ ] **3.5.2** Event-study вокруг первого All-NBA: для каждого игрока, впервые попавшего в All-NBA в сезоне t*, построить относительные годы −2…+3 и оценить fixed-effect coefficient.
- [ ] **3.5.3 [SANITY]** Pre-trend (−2, −1) должен быть ≈ 0 или плавно растущий (контракт-цикл confound), коэф +1 должен быть значимо положительный, +2 — устойчиво положительный.
- [ ] **3.5.4** Multiple-testing correction: всего гипотез теперь 10 (H1–H10). Применить Bonferroni на 10 и BH-FDR на 10. Документировать оба порога в Главе 4.

### Блок 3.6 — H11: Durability и финал (День 7)

- [ ] **3.6.1** Скрипт `analysis_v2/h11_durability.py` — M11a, M11b.
- [ ] **3.6.2** Combined model `M_full`: все блоки в одной спецификации. Это финальная картинка.
- [ ] **3.6.3 [SANITY]** В M11a знак `games_missed_lag1` отрицательный. В M11b интеракция `games_missed × age` должна быть отрицательной (стареющие игроки штрафуются за missed games сильнее, т. к. signal о травме сильнее).
- [ ] **3.6.4** Oster sensitivity для главных новых коэф (β_market, β_supermax, β_all_nba_lag1, β_tier). δ=1, Rmax=1.3·R²_obs.
- [ ] **3.6.5** Финальный отчёт `analysis_v2/reports/phase3_summary.md`: 10 гипотез × (effect size, SE, p, bonf-pass, oster-stable).

---

## Фаза 4 · Реструктуризация текста (5 дней)

- [ ] **4.1** Глава 1 (Введение). Переформулировать цели; новые задачи 5–7 (market, tier, awards). Обновить 1.5 предобзор.
- [ ] **4.2** Глава 2 (Обзор литературы). Ужать 2.1 contract-year, расширить 2.3 Mincer, добавить 2.4 (market) и 2.5 (institutional pricing). Добавить H8/H9/H10 в 2.6.
  - [ ] **4.2.1** Найти и оформить ссылки: Rottenberg 1956, Lazear & Rosen 1981, Krautmann 1999, Hausman & Leonard 1997, Berri & Schmidt 2010, Hill & Groothuis 2001, Coon CBA FAQ.
- [ ] **4.3** Глава 3 (Методология). Обновить 3.1 источники, 3.2 операционализация, ужать 3.3 эвристики (с 10 до 3), добавить M8/M9/M10/M11 в 3.4.
- [ ] **4.4** Глава 4 (Результаты). Реорганизация по факторам (см. plan3.md строки 199–211). H6 deep dive сокращается до 1.5–2 страниц.
- [ ] **4.5** Глава 5 (Дискуссия). Параллельно к Главе 4: декомпозиция, market premium, tier truncation, supermax-eligibility как формальный механизм awards.
- [ ] **4.6** Глава 6 (Заключение) + Аннотация. Переписать вокруг иерархии факторов. 10 гипотез вместо 7.
- [ ] **4.7 [REGRESS]** Перепроверить все цитирования: bib-test (см. фазу 6) каждой главы по мере написания.

---

## Фаза 5 · Визуализация (3 дня, 6–8 рисунков)

- [ ] **5.1** Рис. 1 — Waterfall декомпозиции R². Главный.
- [ ] **5.2** Рис. 2 — Возрастной профиль (parabolic fit + пик).
- [ ] **5.3** Рис. 3 — Quantile β_ppg(τ).
- [ ] **5.4** Рис. 4 — Event-study CBA 2017 coefplot.
- [ ] **5.5** Рис. 5 — Boxplot/violin ln(salary) по tier.
- [ ] **5.6** Рис. 6 — Forest plot main effects M1c-full.
- [ ] **5.7** Рис. 7 — Heatmap precision/recall contract-year proxies (5×5).
- [ ] **5.8 [OPTIONAL]** Рис. 8 — Market × allstar interaction scatter.
- [ ] **5.9** Технические требования: 6×4 inch, sans-serif, grayscale-safe, PDF + PNG@300dpi.
- [ ] **5.10 [SANITY]** Каждый рисунок — отдельно посмотреть в PDF reader, проверить:
  - подписи осей читаемы при печати,
  - нет clipping'а легенды,
  - все цвета различимы в grayscale (или используется штриховка).

---

## Фаза 6 · Финальная вычитка (2 дня)

- [ ] **6.1** Сверить список литературы с in-text citations. Найти и исправить расхождения:
  - [ ] Cameron, Gelbach & Miller (2011) vs Cameron & Miller (2015) — решить и привести к одному виду.
  - [ ] Hinton & Sun (2019) — добавить в список.
  - [ ] Сверить все 19→23 источника. В аннотации/1.7 указать корректное число.
  - [ ] Единый стандарт цитирования (выбрать APA или ГОСТ).
- [ ] **6.2 [REGRESS]** Прогнать spell-check (русский + английские термины).
- [ ] **6.3 [REGRESS]** Все LaTeX-formulas рендерятся (никаких `\hat\beta_{ppg}` посреди абзаца без $).
- [ ] **6.4 [REGRESS]** Сквозная нумерация таблиц и рисунков. Cross-references «см. Таблицу N» соответствуют.
- [ ] **6.5** Объём 55–70 страниц. Если >70 — ужимать главу 2 (литература). Если <55 — расширить главу 5 (дискуссия).
- [ ] **6.6** Финальный сборочный экспорт: PDF, проверить в Adobe Reader (не только в native просмотрщике).

---

## Сводный календарь (5 недель = 25 рабочих дней)

| Неделя | Дни | Фаза | Что должно быть к концу |
|---|---|---|---|
| 1 | 1–5 | 0 + 1 (priority 1+2) | data_analysis_v2.csv построен, priority 1 + 2 covered, coverage_log.csv заполнен |
| 2 | 6–8 | 2 | validation_report_v2.md зелёный, регресс v1 моделей сошёлся |
| 2 | 9–10 | 3 (M1c-full, decomposition start) | M1c-full table, R² decomposition draft |
| 3 | 11–15 | 3 (H8, H9, H10, H11, finalize) | Все 10 гипотез на output, phase3_summary.md |
| 4 | 16–20 | 4 | Все 6 глав переписаны |
| 5 | 21–23 | 5 | Все рисунки в `output_v2/figures/` |
| 5 | 24–25 | 6 | Финальный PDF, bib-test зелёный |

---

## План B при дефиците времени (3 недели вместо 5)

Если дедлайн жёсткий — приоритизирую как в plan3.md строка 255:
- Фаза 1: только priority 1 (block 1.1–1.5).
- Фаза 3: только дни 1–3 (M1c-full + decomposition + H8).
- Фаза 4: только Главы 4 и 6.
- Фаза 5: только рис. 1, 3, 5.

Это даёт ~80% improvement при ~50% затратах. Принимаю решение на конец недели 1 (после фазы 1) — успеваю ли в 5 недель.

---

## Внешние риски и mitigation (живой раздел, дополняется по ходу)

- [ ] **R1** Hoopshype/bbref deeper Cloudflare update — fallback на Wayback (уже работает для hoopshype). Если bbref упадёт — backup на NBA.com + Wikipedia + RealGM. Расширить `nba_scraper/http.py` если придётся.
- [ ] **R2** Market size NULL effect — это содержательный результат, оформляю как «информативный null» по аналогии с H4 tax.
- [ ] **R3** Tier classifier даёт странное распределение — cross-validate на 30 топ-игроках. Hand-curated supermax list как safety net.
- [ ] **R4** Замедление работы — пересматриваю scope на конец каждой недели. Не пытаюсь успеть всё ценой качества.
- [ ] **R5** Новые переменные ломают v1 результаты — фаза 2.3 это ловит. Не двигаюсь дальше, пока не сойдётся.

---

## Definition of Done (всей работы)

1. `data/clean/data_analysis_v2.csv` существует, ≥40 колонок, 3660 строк, SHA256 зафиксирован.
2. Все 10 гипотез имеют output-таблицу в `output_v2/tables/`.
3. Регресс-тест v1: все коэффициенты M1a–M3d совпадают (diff < 1e-6).
4. Главный рисунок (waterfall R² decomposition) готов в PDF + PNG.
5. Курсовая 55–70 страниц, все 6 глав переписаны под новую структуру.
6. `validation_report_v2.md` + `phase3_summary.md` + `sources_log.md` заполнены и пушнуты.
7. Bib-test зелёный, объём проверен, spell-check пройден.
