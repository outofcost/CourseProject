# Data dictionary

Описание всех CSV в `data/` для курсовой по эконометрике NBA. Структура папки:

```
data/
├── raw/        — сырые per-season CSV сразу после скрейпа (не использовать в анализе)
├── clean/      — финальные таблицы, готовые к JOIN'ам и регрессии  ← начни отсюда
├── lookups/    — статичные справочники (команды, штаты, налоговые ставки)
└── manual/     — данные, заполняемые вручную (cap, contract templates)
```

Для эконометрической модели **единственный файл, который тебе на самом деле нужен**, — это `clean/data_merged.csv`. Все остальные — либо его «детали» (которые в нём уже склеены), либо справочники, которые можно прилепить дополнительно.

---

## Канонические идентификаторы

Перед тем как читать таблицы по колонкам — три ключа, которые встречаются во всех файлах:

| Колонка | Что это | Пример | Откуда |
|---|---|---|---|
| `player_id` | Slug игрока на basketball-reference, **уникальный и стабильный** | `curryst01`, `jamesle01` | `<td data-append-csv="...">` на bbref |
| `player_clean` | Канонизированное имя для имён-несовместимых join'ов (lowercase, без диакритики, без `Jr./III`, без точек) | `stephen curry` | `unidecode(lower(name))` + регулярки |
| `player_name` | Имя как написано на оригинальном сайте (диакритика сохранена) | `Stephen Curry`, `Luka Dončić` | bbref / hoopshype |

**Правило join'ов:**
- Между bbref-таблицами (stats ↔ draft ↔ allstar) джойнить по `player_id` — это самый надёжный ключ.
- Между bbref и hoopshype (salaries) у hoopshype нет bbref-slug, поэтому джойним по `(player_clean, season)`.
- `player_clean` собран так, чтобы Luka Dončić с bbref и `Luka Doncic` с hoopshype оба превратились в `luka doncic`.

---

## `clean/data_merged.csv` — главный файл, готов к регрессии

**3660 строк × 66 колонок.** Один наблюдение = (игрок, сезон). Получен JOIN'ом всех остальных таблиц + добавлением производных переменных. Если ты строишь регрессию `ln_salary ~ stats + age + dummies`, читай этот файл.

**Primary key:** `(player_id, season)` — уникален.

**Покрытие:** сезоны 2015/16 — 2023/24 (`season ∈ {2016, …, 2024}`), 383–427 игроков в сезоне.

### Identity & period

| Колонка | Тип | Описание |
|---|---|---|
| `player_id` | str | bbref slug, см. выше. PK. |
| `player_clean` | str | Канон. имя. |
| `player_name` | str | Оригинальное имя. |
| `season` | int | Год **окончания** сезона. `2024` = сезон 2023/24. PK. |

### Roster

| Колонка | Тип | Описание |
|---|---|---|
| `team_abbr` | str | Команда, 3-буквенный код bbref. Композиты для traded mid-season: `2TM` (2 teams), `3TM`, `4TM`. См. ниже. |
| `position` | str | Позиция: `PG`, `SG`, `SF`, `PF`, `C` (иногда дефис: `SF-PF`). |
| `age` | int | Возраст на 1 февраля сезона. Диапазон 19–43. |

### Per-game stats (basketball-reference / leagues/NBA_{year}_per_game.html)

Все «PG» (per game) — это средние **за игру**, не суммы.

| Колонка | Тип | Описание |
|---|---|---|
| `gp` | int | Games played. Фильтр **≥ 20**. |
| `gs` | int | Games started. |
| `mpg` | float | Minutes per game. Фильтр **≥ 5**. |
| `fg`, `fga`, `fg_pct` | float | Field goals: made / attempted / pct (0–1). |
| `fg3`, `fg3a`, `fg3_pct` | float | Three-pointers. **`fg3_pct` NaN, если 0 попыток** (128 строк). |
| `fg2`, `fg2a`, `fg2_pct` | float | Two-pointers. `fg2_pct` NaN при 0 попыток (1 строка). |
| `efg_pct` | float | Effective FG% (учитывает что 3pt дороже). |
| `ft`, `fta`, `ft_pct` | float | Free throws. `ft_pct` NaN при 0 попыток (5 строк). |
| `orb`, `drb`, `rpg` | float | Offensive / defensive / total rebounds. |
| `apg`, `spg`, `bpg` | float | Assists / steals / blocks. |
| `tov`, `pf` | float | Turnovers / personal fouls. |
| `ppg` | float | Points. |

### Advanced stats (basketball-reference / leagues/NBA_{year}_advanced.html)

| Колонка | Тип | Описание |
|---|---|---|
| `mp_total` | int | Сумма минут за сезон (не PG — total). |
| `per` | float | Player Efficiency Rating (Hollinger). 15 = league average. |
| `ts_pct` | float | True Shooting % (учитывает 2pt/3pt/FT в одной метрике). |
| `fg3a_rate` | float | Доля попыток с 3pt из всех FGA. |
| `ft_rate` | float | Доля FTA от FGA. |
| `orb_pct`, `drb_pct`, `trb_pct` | float | % реб. подобранных из всех доступных в игре. |
| `ast_pct`, `stl_pct`, `blk_pct`, `tov_pct` | float | % использования соотв. действия. |
| `usg_pct` | float | Usage rate (% владений, которые заканчиваются на игроке). |
| `ows`, `dws`, `ws`, `ws_48` | float | Offensive / Defensive / total Win Shares и per-48-min. |
| `obpm`, `dbpm`, `bpm` | float | Off./Def./Net Box Plus-Minus (relative to league avg). |
| `vorp` | float | Value Over Replacement Player. |

### Salary (hoopshype через Wayback Machine)

| Колонка | Тип | Описание |
|---|---|---|
| `salary_usd` | float | Номинальная зарплата за сезон. Фильтр **> $100,000**. |

### Draft (basketball-reference / draft/NBA_{year}.html)

LEFT JOIN. 612 строк (~16.7%) имеют **все четыре поля NULL** — это **undrafted free agents** (Fred VanVleet, Wesley Matthews и т.п.). Для них стоит `undrafted = 1`.

| Колонка | Тип | Описание |
|---|---|---|
| `draft_year` | float | Год драфта (1996–2024 в нашем диапазоне). NULL для undrafted. |
| `draft_round` | float | 1 или 2. NULL для undrafted. |
| `draft_pick` | float | Общий пик (1–60). NULL для undrafted. |
| `draft_team` | str | Команда, выбравшая игрока (НЕ обязательно текущая — игроки часто меняют команды). NULL для undrafted. |
| `college` | str | NCAA-программа. NULL ещё чаще (1115 строк) — иностранные игроки, G-League / overseas вместо колледжа. |
| `undrafted` | int | 1 если игрок не был задрафтован. **Используй в регрессии вместо/вместе с `draft_pick`.** |

### Awards

| Колонка | Тип | Описание |
|---|---|---|
| `allstar` | int | 1 если игрок участвовал в All-Star Game этого сезона. 214 единиц / 3660 строк. |

### Derived features (посчитаны в `merge.py`)

| Колонка | Тип | Описание |
|---|---|---|
| `ln_salary` | float | `log(salary_usd)`. Стандартная зависимая переменная для wage-equations. |
| `age_sq` | int | `age² `. Для квадратичной возрастной кривой Минсера. |
| `post_cba_2017` | int | 1 для сезонов ≥ 2018 (новый CBA вступил в силу с 2017/18). |
| `post_covid` | int | 1 для сезонов ≥ 2021 (COVID-bubble сезон 2020/21 и далее). |
| `experience` | float | `season - draft_year`. Лет в лиге. NULL для undrafted (612 строк). |

---

## `clean/stats_all.csv` — per_game + advanced без зарплат

**3796 строк × 53 колонки.** То же что `data_merged.csv`, но **без** salary/draft/allstar/derived. Это «слой» данных до итогового join'а — используй, если хочешь сам контролировать как присоединяются зарплаты и фичи.

**Primary key:** `(player_id, season)`.

Колонки: всё из «Identity & period», «Roster», «Per-game stats», «Advanced stats» (см. выше).

---

## `clean/salaries_all.csv` — зарплаты по сезонам

**4785 строк × 5 колонок.** Зарплаты всех игроков с зарплатой ≥ $100k, по всем 9 сезонам.

**Primary key:** `(player_clean, season)`.

| Колонка | Тип | Описание |
|---|---|---|
| `player_clean` | str | Канон. имя. JOIN-ключ к stats. |
| `player_name` | str | Имя как на hoopshype. |
| `player_slug_hh` | str | **Slug hoopshype** (вид `stephen-curry`, не путать с bbref `curryst01`). Сохранён для отладки, в join'ах не используется. |
| `season` | int | Год окончания сезона. |
| `salary_usd` | float | Номинальная зарплата. |

**Почему больше строк, чем в stats_all (4785 vs 3796):** в зарплатах есть игроки на 10-day и two-way контрактах, которые не дотягивают до фильтра `GP ≥ 20`. После JOIN'а в `data_merged` они отфильтровываются.

---

## `clean/draft_picks.csv` — драфты 1996–2024

**1714 строк × 8 колонок.** Один игрок = одна строка (даже если он играл много лет). Покрытие с 1996 года — достаточно для всех активных в 2016–2024.

**Primary key:** `player_id`.

| Колонка | Тип | Описание |
|---|---|---|
| `player_id` | str | bbref slug. PK. |
| `player_clean`, `player_name` | str | Имя в двух форматах. |
| `draft_year` | int | Год драфта. |
| `draft_round` | int | 1 или 2. |
| `draft_pick` | int | Общий пик. |
| `draft_team` | str | Команда, выбравшая игрока. |
| `college` | str | NCAA. NULL для иностранных / G-League / high school игроков (363 NULL). |

**Что НЕ включено:** undrafted игроки. Они материализуются только при LEFT JOIN с `stats_all` — те, у кого нет совпадения по `player_id` в drafts, и есть undrafted (612 в финальном merge).

---

## `clean/allstar_all.csv` — All-Star rosters

**214 строк × 6 колонок.** Один игрок-сезон = одна строка.

**Primary key:** `(player_id, season)`.

| Колонка | Тип | Описание |
|---|---|---|
| `player_id` | str | bbref slug. |
| `player_clean`, `player_name` | str | Имя. |
| `season` | int | Год окончания сезона. |
| `allstar` | int | Всегда 1 (для отсутствующих игроков значение будет 0 после LEFT JOIN'а в merge). |
| `allstar_team` | str | Команда AS-матча: `East`/`West` (2016, 2017, 2024) или `Team LeBron`/`Team Stephen`/`Team Giannis` (2018-2020). |

---

# Lookup-таблицы — справочники, не данные

## `lookups/team_state_lookup.csv`

**30 строк × 5 колонок.** Маппинг команда → штат (с учётом особых случаев — Toronto в Канаде, Washington в DC/VA).

| Колонка | Тип | Описание |
|---|---|---|
| `team_abbr` | str | Код bbref (3 буквы). |
| `team_name`, `city`, `state` | str | Локация. |
| `no_income_tax` | int | 1 для штатов без подоходного налога (TX, FL, NV, TN, WA). |

## `lookups/state_tax.csv`

**30 строк × 24 колонки.** Wide-формат: одна строка = команда, колонки `2008..2026` хранят top marginal personal income tax rate (как строка с `%`) для штата команды в каждом году. Источник — taxfoundation.org, заполнено вручную (см. `manual/state_tax_TEMPLATE.csv` — этот шаблон уже не нужен).

**Почему wide-формат:** удобен для просмотра в Excel и для копирования из таблиц Tax Foundation, где данные ровно в такой ориентации. Для JOIN'а с `data_merged` его нужно сначала развернуть в long через `pd.melt()`.

## `manual/state_tax_TEMPLATE.csv`

**270 строк (= 30 команд × 9 сезонов), 6 колонок.** Long-format шаблон с пустой колонкой `top_marginal_rate`. **Не заполнен** — пользователь заполнил `lookups/state_tax.csv` вместо него. Можно удалить либо игнорировать.

## `taxes.csv` (в корне проекта)

**50 строк × 1 колонка** (CSV-разделитель `;`, не `,`). Сырые налоговые ставки 50 штатов × 2008-2026. Источник для `lookups/state_tax.csv`. Не используется в коде, оставлен для воспроизводимости.

---

# То что state_tax отдельно — нормально?

**Да, и это правильный паттерн** — `state_tax` это **dimension table** (справочник) в star-schema:

- Налоговая ставка зависит от **(штат, год)**, а не от (игрок, сезон). Размер штатов/команд (30) на порядок меньше fact-таблицы (3660 player-seasons). Хранить ставку в каждой строке player-season — это дублирование информации.
- Налоги — единственная переменная, **полностью внешняя** к скрейпу. Она пришла из Tax Foundation вручную и обновляется независимо. Изоляция её в `lookups/` означает, что обновить ставки можно не перетрагивая пайплайн скрейпа.
- Wide-формат `state_tax.csv` сохраняет ту же ориентацию, в которой Tax Foundation публикует таблицы — это удобно для ручных правок.

**Но в `data_merged.csv` налогов нет** — это не из-за «забыли», а из-за того, что в первичных требованиях было «налоги штатов уже есть вручную, их не трогаем». Если хочешь прилепить их к финальному датасету для регрессии — это 5 строк:

```python
import pandas as pd

df  = pd.read_csv('data/clean/data_merged.csv')
tax = pd.read_csv('data/lookups/state_tax.csv')

# 1) wide → long
year_cols = [c for c in tax.columns if c.isdigit()]
tax_long = tax.melt(
    id_vars=['team_abbr', 'state', 'no_income_tax'],
    value_vars=year_cols,
    var_name='season',
    value_name='top_marginal_rate',
)

# 2) типы: season → int, ставка "6.00%" → 6.0
tax_long['season'] = tax_long['season'].astype(int)
tax_long['top_marginal_rate'] = (
    tax_long['top_marginal_rate'].str.rstrip('%').astype(float)
)

# 3) LEFT JOIN: команда + сезон → ставка
df = df.merge(
    tax_long[['team_abbr', 'season', 'state', 'no_income_tax', 'top_marginal_rate']],
    on=['team_abbr', 'season'],
    how='left',
)
```

После этого в `df` появятся колонки `state`, `no_income_tax`, `top_marginal_rate` для каждой строки player-season.

**Один нюанс:** строки с `team_abbr ∈ {2TM, 3TM, 4TM}` — это игроки, поменявшие команду в течение сезона. Для них налог не определён (играли в разных штатах с разной нагрузкой). В таблице налогов их нет, и после JOIN'а они получат `NaN`. В регрессии их надо либо отбросить (`df.dropna(subset=['top_marginal_rate'])`), либо специально импьютировать средневзвешенным по дням (отдельная задача).

---

# Pipeline: как файлы связаны

```
basketball-reference                                hoopshype (Wayback)
 ├── /leagues/{year}_per_game.html                   └── /salaries/players/{start}-{end}/
 ├── /leagues/{year}_advanced.html                                │
 ├── /draft/NBA_{year}.html                                       │
 └── /allstar/NBA_{year}.html                                     │
       │       │       │       │                                  │
       ▼       ▼       ▼       ▼                                  ▼
   data/raw/per_game_{year}.csv          (per-season,          data/raw/salaries_{year}.csv
   data/raw/advanced_{year}.csv          ~400-600 rows each)
   data/raw/draft_{year}.csv
   data/raw/allstar_{year}.csv
       │       │       │       │                                  │
       │       │       │       │                                  │
       │       └───────┼───────┘                                  │
       │       JOIN on player_id+season                           │
       ▼               ▼               ▼                          ▼
  clean/stats_all   clean/draft_picks  clean/allstar_all     clean/salaries_all
   (3796 rows)       (1714 rows)        (214 rows)            (4785 rows)
       │                  │                 │                     │
       └────────┬─────────┴─────────────────┴─────────────────────┘
                ▼
       clean/data_merged.csv  (3660 × 66, готов к регрессии)
                │
                │  + state_tax если хочешь экстерналии
                ▼
       lookups/state_tax.csv  (внешний источник, не из скрейпа)
```

---

# Краткий рецепт для регрессии

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data/clean/data_merged.csv')

# базовая Минсеровская спецификация:
#   ln_salary = β0 + β1*age + β2*age² + β3*experience + β4-stats + β5*allstar + γ*post_cba_2017 + δ*post_covid + ε
features = [
    'age', 'age_sq', 'experience',
    'ppg', 'rpg', 'apg', 'ts_pct',
    'per', 'ws', 'vorp', 'usg_pct',
    'allstar', 'undrafted',
    'post_cba_2017', 'post_covid',
]

# для undrafted: experience NaN → используй фильтр или замени
sample = df.dropna(subset=['experience'])    # или заменить на 0 + dummy
```

Для FE-модели в `plm` / `linearmodels` группировать по `player_id` (individual FE) и/или `season` (year FE). Кластеризовать SE по `player_id`.
