# =============================================================================
# 00_setup.R
# Проект: Курсовая по эконометрике NBA (Contract Year Effect + Tax Burden)
# Автор:  Партнёр B
# Дата:   2025
# Задача: Установить пакеты, создать структуру папок, задать глобальные параметры
# Входы:  —
# Выходы: Готовая структура папок nba_thesis/
# =============================================================================

# ---- 0. Проверка версии R ---------------------------------------------------
stopifnot("Нужен R >= 4.3" = getRversion() >= "4.3")

# ---- 1. Установка пакетов ---------------------------------------------------

# Список всех нужных пакетов
required_packages <- c(
  # Сбор данных
  "rvest",       # парсинг HTML
  "httr",        # HTTP-запросы
  "polite",      # вежливый скрейпинг (robots.txt + задержки)

  # Обработка данных
  "tidyverse",   # dplyr, ggplot2, stringr, readr, tidyr, purrr, forcats
  "janitor",     # clean_names(), tabyl()
  "lubridate",   # работа с датами
  "stringi",     # stri_trans_general() — убираем диакритику

  # Эконометрика
  "plm",         # Panel data models (FE, RE, Hausman)
  "lmtest",      # bptest(), resettest(), coeftest()
  "sandwich",    # vcovCL() — кластеризованные SE
  "car",         # vif()
  "fixest",      # feols() — быстрый FE + staggered DiD (Sun-Abraham)

  # Вывод результатов
  "stargazer",   # таблицы регрессий в LaTeX/HTML
  "broom",       # tidy() — превратить модели в data.frame
  "modelsummary",# альтернатива stargazer, гибче

  # Графика
  "ggplot2",     # основа (входит в tidyverse, но явно для ясности)
  "patchwork",   # склейка нескольких ggplot
  "scales",      # форматирование осей (dollar, comma)
  "corrplot",    # корреляционный heatmap
  "ggcorrplot"   # ggplot-версия corrplot
)

# Установить только то, чего ещё нет
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages) > 0) {
  message("Устанавливаем пакеты: ", paste(new_packages, collapse = ", "))
  install.packages(new_packages, dependencies = TRUE)
} else {
  message("Все пакеты уже установлены.")
}

# Проверка успешности установки
missing_after <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(missing_after) > 0) {
  warning("Не удалось установить: ", paste(missing_after, collapse = ", "))
} else {
  message("OK: все пакеты установлены и доступны.")
}


# ---- 2. Создание структуры папок --------------------------------------------

# Корневая папка проекта — по умолчанию текущая рабочая директория
# Поменяй ROOT на свой путь, если нужно:
# ROOT <- "C:/Users/ВашеИмя/Desktop/nba_thesis"
ROOT <- getwd()

dirs <- c(
  "data/raw",          # сырые CSV после скрейпинга
  "data/manual",       # ручные CSV: контракты, cap
  "data/lookups",      # справочники: team→state, позиции
  "data/clean",        # финальный датасет
  "scripts",           # R-скрипты
  "output/tables",     # stargazer / etable
  "output/figures",    # ggplot2 графики
  "logs"               # логи скрейпинга
)

for (d in dirs) {
  path <- file.path(ROOT, d)
  if (!dir.exists(path)) {
    dir.create(path, recursive = TRUE)
    message("Создана папка: ", path)
  }
}
message("Структура папок готова.")


# ---- 3. Глобальные параметры проекта ----------------------------------------

# Сезоны в проекте (формат: последний год сезона, т.е. 2016 = сезон 2015/16)
SEASONS <- 2016:2024

# Минимальный порог для включения игрока в выборку
MIN_GP <- 20      # игры проведены
MIN_MPG <- 5      # средние минуты за игру

# Порог для фильтрации мусорных зарплат (меньше нет ни одного реального контракта)
MIN_SALARY <- 100000

# Порог высокого налога штата для DiD (в %)
HIGH_TAX_THRESHOLD <- 8
LOW_TAX_THRESHOLD  <- 3

# Seed для воспроизводимости (используй везде, где есть рандомизация)
set.seed(42)

# Тема ggplot2 для единообразия графиков
theme_nba <- theme_minimal(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "grey40"),
    axis.title    = element_text(face = "bold"),
    legend.position = "bottom"
  )


# ---- 4. Справочник команда → штат → налоговая ставка ------------------------
# Полный список 30 команд NBA с кодами и штатами.
# Налоговые ставки (top marginal personal income tax rate) заполнишь
# вручную в data/manual/state_tax.csv по данным taxfoundation.org.
# Здесь — только справочник команда → штат для быстрого присвоения.

team_state_lookup <- tibble::tribble(
  ~team_abbr, ~team_name,              ~city,             ~state,           ~no_income_tax,
  "ATL",      "Atlanta Hawks",          "Atlanta",         "Georgia",         0L,
  "BOS",      "Boston Celtics",         "Boston",          "Massachusetts",   0L,
  "BKN",      "Brooklyn Nets",          "Brooklyn",        "New York",        0L,
  "CHA",      "Charlotte Hornets",      "Charlotte",       "North Carolina",  0L,
  "CHI",      "Chicago Bulls",          "Chicago",         "Illinois",        0L,
  "CLE",      "Cleveland Cavaliers",    "Cleveland",       "Ohio",            0L,
  "DAL",      "Dallas Mavericks",       "Dallas",          "Texas",           1L,  # 0% налог
  "DEN",      "Denver Nuggets",         "Denver",          "Colorado",        0L,
  "DET",      "Detroit Pistons",        "Detroit",         "Michigan",        0L,
  "GSW",      "Golden State Warriors",  "San Francisco",   "California",      0L,
  "HOU",      "Houston Rockets",        "Houston",         "Texas",           1L,  # 0% налог
  "IND",      "Indiana Pacers",         "Indianapolis",    "Indiana",         0L,
  "LAC",      "Los Angeles Clippers",   "Los Angeles",     "California",      0L,
  "LAL",      "Los Angeles Lakers",     "Los Angeles",     "California",      0L,
  "MEM",      "Memphis Grizzlies",      "Memphis",         "Tennessee",       1L,  # 0% налог
  "MIA",      "Miami Heat",             "Miami",           "Florida",         1L,  # 0% налог
  "MIL",      "Milwaukee Bucks",        "Milwaukee",       "Wisconsin",       0L,
  "MIN",      "Minnesota Timberwolves", "Minneapolis",     "Minnesota",       0L,
  "NOP",      "New Orleans Pelicans",   "New Orleans",     "Louisiana",       0L,
  "NYK",      "New York Knicks",        "New York",        "New York",        0L,
  "OKC",      "Oklahoma City Thunder",  "Oklahoma City",   "Oklahoma",        0L,
  "ORL",      "Orlando Magic",          "Orlando",         "Florida",         1L,  # 0% налог
  "PHI",      "Philadelphia 76ers",     "Philadelphia",    "Pennsylvania",    0L,
  "PHX",      "Phoenix Suns",           "Phoenix",         "Arizona",         0L,
  "POR",      "Portland Trail Blazers", "Portland",        "Oregon",          0L,
  "SAC",      "Sacramento Kings",       "Sacramento",      "California",      0L,
  "SAS",      "San Antonio Spurs",      "San Antonio",     "Texas",           1L,  # 0% налог
  "TOR",      "Toronto Raptors",        "Toronto",         "Ontario (Canada)",0L,  # особый случай
  "UTA",      "Utah Jazz",              "Salt Lake City",  "Utah",            0L,
  "WAS",      "Washington Wizards",     "Washington",      "DC/Virginia",     0L
)

# Сохраняем справочник
readr::write_csv(team_state_lookup,
                 file.path(ROOT, "data/lookups/team_state_lookup.csv"))
message("Справочник команда→штат сохранён: data/lookups/team_state_lookup.csv")


# ---- 5. Шаблон ручного CSV для налоговых ставок ----------------------------
# Заполнить вручную по: taxfoundation.org/state-income-tax-rates/
# Ставки меняются каждый год — нужны значения для каждого сезона.

state_tax_template <- tidyr::expand_grid(
  team_abbr = team_state_lookup$team_abbr,
  season    = SEASONS
) %>%
  dplyr::left_join(
    dplyr::select(team_state_lookup, team_abbr, state, no_income_tax),
    by = "team_abbr"
  ) %>%
  dplyr::mutate(
    top_marginal_rate = NA_real_,  # ЗАПОЛНИТЬ ВРУЧНУЮ (например: 13.3 для CA)
    notes             = NA_character_
  )

readr::write_csv(state_tax_template,
                 file.path(ROOT, "data/manual/state_tax_TEMPLATE.csv"))
message("Шаблон налоговых ставок сохранён: data/manual/state_tax_TEMPLATE.csv")
message("Заполни top_marginal_rate вручную по taxfoundation.org и переименуй в state_tax.csv")


# ---- 6. Итог ----------------------------------------------------------------

cat("\n")
cat("============================================================\n")
cat("  00_setup.R выполнен успешно\n")
cat("============================================================\n")
cat("  Следующий шаг: 01_scrape_bbref.R\n")
cat("  — scraping basketball-reference (per_game + advanced)\n")
cat("============================================================\n")
