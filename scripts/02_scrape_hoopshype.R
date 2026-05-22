# =============================================================================
# 02_scrape_hoopshype.R
# Проект: Курсовая по эконометрике NBA
# Автор:  Партнёр B
# Дата:   2025
# Задача: Скрейпинг зарплат игроков с hoopshype.com за сезоны 2015/16–2023/24
# Входы:  —
# Выходы: data/raw/salaries_all.csv
# =============================================================================

library(tidyverse)
library(rvest)
library(polite)
library(stringi)
library(janitor)
library(readr)

source("scripts/00_setup.R")

# Функция канонизации имён (та же, что в 01_scrape_bbref.R)
canonicalize_name <- function(name) {
  name %>%
    stringi::stri_trans_general("Latin-ASCII") %>%
    tolower() %>%
    stringr::str_remove_all("[\\.,\\-'']") %>%
    stringr::str_remove_all("\\s+(jr|sr|ii|iii|iv)$") %>%
    stringr::str_squish()
}


# ---- Функция: скрейп зарплат одного сезона с hoopshype ----------------------

scrape_hoopshype_salaries <- function(season_start, season_end, pause_sec = 4) {
  # season_start = 2015, season_end = 2016 → сезон 2015/16
  url <- glue::glue("https://hoopshype.com/salaries/players/{season_start}-{season_end}/")

  message("  ", season_start, "/", season_end %% 100, " → ", url, " ... ",
          appendLF = FALSE)

  tryCatch({
    session <- polite::bow(url,
                           user_agent = "NBA Thesis Research / student project")
    page    <- polite::scrape(session)
    Sys.sleep(pause_sec)

    # hoopshype использует кастомную таблицу с классом .hh-salaries-ranking-table
    # Попробуем сначала html_table(), потом — ручной парсинг через css-классы
    tables <- page %>% rvest::html_elements("table") %>% rvest::html_table()

    if (length(tables) == 0) {
      # Запасной путь: парсим вручную через CSS
      names_raw   <- page %>%
        rvest::html_elements(".name") %>%
        rvest::html_text2()

      salaries_raw <- page %>%
        rvest::html_elements(".salary") %>%
        rvest::html_text2()

      # Первый элемент .salary обычно — заголовок сезона, убираем
      if (length(salaries_raw) > length(names_raw)) {
        salaries_raw <- salaries_raw[-1]
      }

      df <- tibble::tibble(
        player_name  = names_raw,
        salary_raw   = salaries_raw
      )

    } else {
      # Обычный html_table() сработал
      df <- tables[[1]] %>%
        janitor::clean_names()

      # На hoopshype обычно колонки: rank, player, team, salary_текущийсезон, ...
      # Нам нужны player и первая колонка зарплаты
      # Ищем колонку с именем вида "x2015_2016" или просто первую числовую
      salary_cols <- names(df)[stringr::str_detect(names(df), "\\d{4}")]

      if (length(salary_cols) == 0) {
        # Последний fallback: берём вторую числовую колонку
        salary_cols <- names(df)[sapply(df, function(x) any(stringr::str_detect(x, "\\$")))]
      }

      if (length(salary_cols) == 0) {
        warning("Не нашли колонку зарплаты на ", url)
        return(NULL)
      }

      current_season_col <- salary_cols[1]

      df <- df %>%
        dplyr::rename(
          player_name = dplyr::contains("player"),
          salary_raw  = dplyr::all_of(current_season_col)
        ) %>%
        dplyr::select(player_name, salary_raw)
    }

    # Парсим зарплату: "$5,123,456" → 5123456
    df <- df %>%
      dplyr::filter(!is.na(player_name), player_name != "", player_name != "Player") %>%
      dplyr::mutate(
        salary_usd  = readr::parse_number(salary_raw),  # убирает $, запятые
        season      = season_end,                         # год сезона (2016 для 2015/16)
        player_clean = canonicalize_name(player_name)
      ) %>%
      dplyr::filter(
        !is.na(salary_usd),
        salary_usd >= MIN_SALARY          # убираем мусор (two-way, 10-day)
      ) %>%
      dplyr::select(player_clean, player_name, season, salary_usd)

    message("OK (", nrow(df), " игроков)")
    return(df)

  }, error = function(e) {
    message("ОШИБКА: ", e$message)
    cat(format(Sys.time()), "| hoopshype | season:", season_end,
        "| ERROR:", e$message, "\n",
        file = "logs/scrape_log.txt", append = TRUE)
    return(NULL)
  })
}


# ---- Скрейпим все сезоны ----------------------------------------------------

message("\n=== Скрейпим зарплаты с hoopshype ===")

# Формируем пары сезонов: (2015,2016), (2016,2017), ..., (2023,2024)
season_pairs <- tibble::tibble(
  start = SEASONS - 1,
  end   = SEASONS
)

salaries_list <- list()

for (i in seq_len(nrow(season_pairs))) {
  yr_start <- season_pairs$start[i]
  yr_end   <- season_pairs$end[i]

  result <- scrape_hoopshype_salaries(yr_start, yr_end)

  if (!is.null(result)) {
    salaries_list[[as.character(yr_end)]] <- result
  }
}

salaries_raw <- dplyr::bind_rows(salaries_list)
message("\nИтого зарплат собрано: ", nrow(salaries_raw), " строк")


# ---- Дополнительная очистка -------------------------------------------------

salaries_clean <- salaries_raw %>%
  # Убираем явно невалидные значения
  dplyr::filter(salary_usd > MIN_SALARY, salary_usd < 1e8) %>%  # до $100M — защита от мусора

  # Убираем дубли (если игрок упомянут дважды за сезон — берём максимальную зарплату)
  dplyr::group_by(player_clean, season) %>%
  dplyr::slice_max(salary_usd, n = 1, with_ties = FALSE) %>%
  dplyr::ungroup()

message("После дедупликации: ", nrow(salaries_clean), " строк")


# ---- Санити-чек: распределение зарплат --------------------------------------

message("\nРаспределение зарплат ($):")
print(summary(salaries_clean$salary_usd))

# Топ-5 самых высоких зарплат (проверка на адекватность)
message("\nТоп-5 зарплат в датасете:")
salaries_clean %>%
  dplyr::slice_max(salary_usd, n = 5) %>%
  dplyr::select(player_name, season, salary_usd) %>%
  dplyr::mutate(salary_fmt = scales::dollar(salary_usd)) %>%
  print()

# Распределение по сезонам
message("\nИгроков по сезонам:")
salaries_clean %>%
  dplyr::count(season) %>%
  print()


# ---- Сохранение -------------------------------------------------------------

readr::write_csv(salaries_clean, "data/raw/salaries_all.csv")
message("\nСохранено: data/raw/salaries_all.csv (", nrow(salaries_clean), " строк)")

cat("\n")
cat("============================================================\n")
cat("  02_scrape_hoopshype.R выполнен\n")
cat("  Следующий шаг: 03_load_manual.R (ручные CSV)\n")
cat("============================================================\n")
