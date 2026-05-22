# =============================================================================
# 01_scrape_bbref.R
# Проект: Курсовая по эконометрике NBA
# Автор:  Партнёр B
# Дата:   2025
# Задача: Скрейпинг per-game и advanced статистики с basketball-reference.com
#         за сезоны 2015/16 – 2023/24
# Входы:  —
# Выходы: data/raw/per_game_all.csv
#         data/raw/advanced_all.csv
# =============================================================================

library(tidyverse)
library(rvest)
library(polite)
library(stringi)
library(janitor)

# Загружаем глобальные параметры (SEASONS, MIN_GP и т.д.)
source("scripts/00_setup.R")

# ---- Вспомогательная функция: канонизация имён игроков ----------------------
# Проблема: на разных сайтах имена пишутся по-разному.
# "Luka Dončić" vs "Luka Doncic", "P.J. Tucker" vs "PJ Tucker" и т.д.
# Решение: lowercase + убрать диакритику + убрать спецсимволы.

canonicalize_name <- function(name) {
  name %>%
    stringi::stri_trans_general("Latin-ASCII") %>%  # Dončić → Doncic
    tolower() %>%
    stringr::str_remove_all("[\\.,\\-'']") %>%       # убрать точки, запятые, дефисы
    stringr::str_remove_all("\\s+(jr|sr|ii|iii|iv)$") %>%  # убрать суффиксы
    stringr::str_squish()                             # убрать лишние пробелы
}

# ---- Функция: скрейп одной таблицы с bbref ----------------------------------

scrape_bbref_table <- function(url, table_id, season_year, pause_sec = 4) {
  # 1. Создаем сессию
  session <- polite::bow(url, user_agent = "NBA Thesis Research / student project")
  
  # 2. Просто скрейпим страницу без лишних параметров
  page <- polite::scrape(session)
  
  # 3. ПРОВЕРКА: если страница не загрузилась, не идем дальше
  if (is.null(page)) {
    message(" --- Ошибка: Не удалось загрузить страницу (возможно, бан по IP)")
    return(NULL)
  }
  
  Sys.sleep(pause_sec) 
  
  # 4. Поиск таблицы
  table_node <- page %>% rvest::html_element(paste0("#", table_id))
  
  if (is.na(table_node)) {
    warning("Таблица с id ", table_id, " не найдена на странице")
    return(NULL)
  }
  
  table_raw <- rvest::html_table(table_node, fill = TRUE)
  
  table_raw %>%
    janitor::clean_names() %>%
    dplyr::mutate(season = season_year)
}


# ---- 1. PER-GAME СТАТИСТИКА -------------------------------------------------

message("\n=== Скрейпим per-game статистику ===")

per_game_list <- list()

for (yr in SEASONS) {
  url <- glue::glue("https://www.basketball-reference.com/leagues/NBA_{yr}_per_game.html")
  message("  Сезон ", yr - 1, "/", yr %% 100, " ... ", appendLF = FALSE)

  tryCatch({
    df <- scrape_bbref_table(url, table_id = "per_game_stats", season_year = yr)

    if (!is.null(df)) {
      per_game_list[[as.character(yr)]] <- df
      message("OK (", nrow(df), " строк)")
    }
  }, error = function(e) {
    message("ОШИБКА: ", e$message)
    # Записываем в лог
    cat(format(Sys.time()), "| per_game | season:", yr, "| ERROR:", e$message, "\n",
        file = "logs/scrape_log.txt", append = TRUE)
  })
}

# Склеиваем все сезоны
per_game_raw <- dplyr::bind_rows(per_game_list)
message("Итого per_game строк (до фильтрации): ", nrow(per_game_raw))


# ---- 2. ADVANCED СТАТИСТИКА -------------------------------------------------

message("\n=== Скрейпим advanced статистику ===")

advanced_list <- list()

for (yr in SEASONS) {
  url <- glue::glue("https://www.basketball-reference.com/leagues/NBA_{yr}_advanced.html")
  message("  Сезон ", yr - 1, "/", yr %% 100, " ... ", appendLF = FALSE)

  tryCatch({
    df <- scrape_bbref_table(url, table_id = "advanced_stats", season_year = yr)

    if (!is.null(df)) {
      advanced_list[[as.character(yr)]] <- df
      message("OK (", nrow(df), " строк)")
    }
  }, error = function(e) {
    message("ОШИБКА: ", e$message)
    cat(format(Sys.time()), "| advanced | season:", yr, "| ERROR:", e$message, "\n",
        file = "logs/scrape_log.txt", append = TRUE)
  })
}

advanced_raw <- dplyr::bind_rows(advanced_list)
message("Итого advanced строк (до фильтрации): ", nrow(advanced_raw))


# ---- 3. ОЧИСТКА PER-GAME ----------------------------------------------------

message("\n=== Чистим per-game ===")

per_game_clean <- per_game_raw %>%
  # Убираем строки-разделители (basketball-reference вставляет повторяющиеся заголовки)
  dplyr::filter(player != "Player", !is.na(player), player != "") %>%

  # КЛЮЧЕВОЙ МОМЕНТ: если игрок играл за несколько команд —
  # оставляем только строку TOT (итоговая статистика за сезон)
  dplyr::group_by(player, season) %>%
  dplyr::mutate(has_tot = any(tm == "TOT")) %>%
  dplyr::filter(!(has_tot & tm != "TOT")) %>%
  dplyr::ungroup() %>%

  # Преобразуем числовые колонки (bbref отдаёт всё как character)
  dplyr::mutate(
    across(c(g, gs, mp, fg, fga, x3p, x3pa, x2p, x2pa,
             ft, fta, orb, drb, trb, ast, stl, blk, tov, pf, pts),
           ~ suppressWarnings(as.numeric(.)))
  ) %>%

  # Переименовываем для удобства
  dplyr::rename(
    player_name = player,
    team_abbr   = tm,
    position    = pos,
    gp          = g,
    ppg         = pts,
    rpg         = trb,
    apg         = ast,
    mpg         = mp
  ) %>%

  # Добавляем канонизированное имя для join'ов
  dplyr::mutate(player_clean = canonicalize_name(player_name)) %>%

  # Базовый фильтр: только «реальные» игроки
  dplyr::filter(
    gp  >= MIN_GP,
    mpg >= MIN_MPG
  ) %>%

  # Оставляем нужные колонки
  dplyr::select(player_clean, player_name, season, team_abbr, position,
                age, gp, gs, mpg, ppg, rpg, apg,
                fg, fga, x3p, x3pa, ft, fta,
                stl, blk, tov, pf)

message("Per-game после фильтрации: ", nrow(per_game_clean), " строк")


# ---- 4. ОЧИСТКА ADVANCED ----------------------------------------------------

message("\n=== Чистим advanced ===")

advanced_clean <- advanced_raw %>%
  dplyr::filter(player != "Player", !is.na(player), player != "") %>%

  # Та же логика TOT
  dplyr::group_by(player, season) %>%
  dplyr::mutate(has_tot = any(tm == "TOT")) %>%
  dplyr::filter(!(has_tot & tm != "TOT")) %>%
  dplyr::ungroup() %>%

  # Числовые колонки advanced
  dplyr::mutate(
    across(c(per, ts_percent, x3p_ar, f_tr, orb_percent, drb_percent, trb_percent,
             ast_percent, stl_percent, blk_percent, tov_percent, usg_percent,
             ows, dws, ws, ws_48, obpm, dbpm, bpm, vorp),
           ~ suppressWarnings(as.numeric(.)))
  ) %>%

  dplyr::rename(
    player_name = player,
    team_abbr   = tm
  ) %>%

  dplyr::mutate(player_clean = canonicalize_name(player_name)) %>%

  # Оставляем только нужные advanced метрики
  dplyr::select(player_clean, player_name, season, team_abbr,
                per, ts_percent, usg_percent,
                ws, ws_48, ows, dws,
                bpm, obpm, dbpm, vorp)

message("Advanced после фильтрации: ", nrow(advanced_clean), " строк")


# ---- 5. САНИТИ-ЧЕК: несматченные имена -------------------------------------

# Проверяем, насколько хорошо совпадают имена между двумя таблицами
# (пока без зарплат — это сделаем в 04_merge_clean.R)

unmatched_check <- dplyr::anti_join(
  per_game_clean,
  advanced_clean,
  by = c("player_clean", "season")
)

if (nrow(unmatched_check) > 0) {
  message("⚠️  Не сматчились ", nrow(unmatched_check),
          " строк per_game ↔ advanced. Смотри: logs/unmatched_pg_vs_adv.csv")
  readr::write_csv(unmatched_check,
                   "logs/unmatched_pg_vs_adv.csv")
} else {
  message("OK: все per_game строки нашли пару в advanced.")
}


# ---- 6. СОХРАНЕНИЕ ----------------------------------------------------------

readr::write_csv(per_game_clean, "data/raw/per_game_all.csv")
readr::write_csv(advanced_clean, "data/raw/advanced_all.csv")

message("\nСохранено:")
message("  data/raw/per_game_all.csv  — ", nrow(per_game_clean), " строк")
message("  data/raw/advanced_all.csv  — ", nrow(advanced_clean), " строк")

cat("\n")
cat("============================================================\n")
cat("  01_scrape_bbref.R выполнен\n")
cat("  Следующий шаг: 02_scrape_hoopshype.R\n")
cat("============================================================\n")
