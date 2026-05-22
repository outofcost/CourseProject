# =============================================================================
# 03_load_manual.R
# Проект: Курсовая по эконометрике NBA
# Автор:  Партнёр B
# Дата:   2025
# Задача: Загрузить и проверить ручные CSV (налоги, salary cap, контракты).
#         Сгенерировать маркировку contract_year — Сценарий Б (эвристика).
#         Сценарий А (ручная разметка топ-300) — отдельный файл, если есть.
# Входы:  data/manual/state_tax.csv          (заполнить вручную!)
#         data/manual/salary_cap.csv          (9 строк, заполнить вручную)
#         data/raw/per_game_all.csv
#         data/raw/salaries_all.csv
# Выходы: data/manual/state_tax_validated.csv
#         data/manual/salary_cap_validated.csv
#         data/manual/contract_year_heuristic.csv
# =============================================================================

library(tidyverse)
library(readr)
library(janitor)

source("scripts/00_setup.R")


# ============================================================
# ЧАСТЬ 1: НАЛОГОВЫЕ СТАВКИ
# ============================================================
# Если ты ещё не заполнил state_tax.csv — запусти этот блок,
# он создаст файл с уже известными нулями (штаты без налога)
# и NA для остальных. Заполни NA по taxfoundation.org.

message("=== Загружаем налоговые ставки ===")

# Жёстко заданные ставки для штатов без подоходного налога
# (они стабильны — 0% во всём нашем периоде)
no_tax_states <- c("Texas", "Florida", "Tennessee", "Nevada")
# Примечание: Tennessee отменил налог на инвестдоходы в 2021,
# для зарплат = 0% весь период.

# Ставки по ключевым штатам (top marginal, %)
# Источник: taxfoundation.org — проверь и уточни по годам!
tax_rates_reference <- tribble(
  ~state,           ~approx_rate, ~notes,
  "California",     13.3,         "13.3% с 2012 по наст.время (Prop 30)",
  "New York",       10.9,         "10.9% с 2021; до 2021 — 8.82%",
  "Oregon",         9.9,          "9.9% стабильно",
  "Minnesota",      9.85,         "9.85% стабильно",
  "Massachusetts",  5.0,          "5% плоская шкала (5.05% до 2020)",
  "Wisconsin",      7.65,         "7.65% стабильно",
  "Illinois",       4.95,         "4.95% с 2017; до 2017 — 3.75%",
  "Michigan",       4.25,         "4.25% стабильно",
  "Indiana",        3.23,         "3.23% плоская шкала",
  "Ohio",           3.99,         "снижалась с 5.39% до 3.99%",
  "Pennsylvania",   3.07,         "3.07% стабильно",
  "Georgia",        5.75,         "снижается с 2024; в 2015-2023 = 5.75%",
  "North Carolina", 5.25,         "снижалась, 5.25% в осн. периоде",
  "Louisiana",      6.0,          "6% топ-ставка",
  "Oklahoma",       5.0,          "5% стабильно",
  "Colorado",       4.55,         "4.55% плоская шкала",
  "Utah",           4.95,         "4.95% плоская шкала",
  "Arizona",        4.5,          "2.5% с 2023; до 2023 — 4.5%",
  "DC/Virginia",    8.95,         "8.95% для DC (Wizards играют в DC)",
  "Ontario (Canada)", 53.53,      "Провинциальная + федеральная. Особый случай — см. ниже"
)

message("Справочник ставок:")
print(tax_rates_reference)
message("\n⚠️  ВАЖНО: Это приближённые значения!")
message("  Заполни data/manual/state_tax_TEMPLATE.csv точными ставками по годам.")
message("  Источник: https://taxfoundation.org/data/all/state/state-income-tax-rates/\n")

# Если файл state_tax.csv уже заполнен — загружаем и валидируем
state_tax_path <- "data/manual/state_tax.csv"

if (file.exists(state_tax_path)) {
  state_tax <- read_csv(state_tax_path, show_col_types = FALSE) %>%
    janitor::clean_names()

  # Проверки
  missing_rates <- state_tax %>% filter(is.na(top_marginal_rate))
  if (nrow(missing_rates) > 0) {
    warning("В state_tax.csv есть незаполненные ставки: ", nrow(missing_rates), " строк")
    print(missing_rates)
  }

  # Проверка: штаты без налога должны иметь ставку = 0
  wrong_zero <- state_tax %>%
    filter(no_income_tax == 1, top_marginal_rate != 0)
  if (nrow(wrong_zero) > 0) {
    warning("Штаты с no_income_tax=1 имеют ненулевую ставку:")
    print(wrong_zero)
  }

  write_csv(state_tax, "data/manual/state_tax_validated.csv")
  message("state_tax.csv загружен и проверен: ", nrow(state_tax), " строк")

} else {
  message("⚠️  Файл data/manual/state_tax.csv не найден.")
  message("   Заполни data/manual/state_tax_TEMPLATE.csv и переименуй в state_tax.csv")
  message("   Продолжаем с заглушкой (только no_income_tax флаг).")

  # Заглушка: используем только флаг no_income_tax из справочника
  team_state <- read_csv("data/lookups/team_state_lookup.csv", show_col_types = FALSE)
  state_tax <- expand_grid(
    team_abbr = team_state$team_abbr,
    season    = SEASONS
  ) %>%
    left_join(select(team_state, team_abbr, state, no_income_tax), by = "team_abbr") %>%
    mutate(top_marginal_rate = ifelse(no_income_tax == 1, 0, NA_real_))
}


# ============================================================
# ЧАСТЬ 2: SALARY CAP
# ============================================================
# Заполни data/manual/salary_cap.csv вручную.
# Источник: https://basketball.realgm.com/nba/info/salary_cap

message("\n=== Загружаем salary cap ===")

salary_cap_path <- "data/manual/salary_cap.csv"

if (file.exists(salary_cap_path)) {
  salary_cap <- read_csv(salary_cap_path, show_col_types = FALSE)
  message("Salary cap загружен:")
  print(salary_cap)
} else {
  message("⚠️  Файл salary_cap.csv не найден. Создаём с известными значениями...")

  # Исторические значения salary cap NBA ($ млн)
  # Источник: Basketball Reference / RealGM
  salary_cap <- tribble(
    ~season, ~salary_cap_usd,
    2016,    70750000,
    2017,    99093000,   # резкий скачок — новый TV-контракт
    2018,    99093000,
    2019,    101869000,
    2020,    109140000,
    2021,    109140000,  # заморожен из-за COVID
    2022,    112414000,
    2023,    123655000,
    2024,    136021000
  )

  write_csv(salary_cap, salary_cap_path)
  message("Создан data/manual/salary_cap.csv с известными значениями.")
  message("⚠️  Проверь цифры по: basketball.realgm.com/nba/info/salary_cap")
  print(salary_cap)
}


# ============================================================
# ЧАСТЬ 3: МАРКИРОВКА CONTRACT_YEAR — СЦЕНАРИЙ Б (ЭВРИСТИКА)
# ============================================================
# Правило: contract_year_it = 1, если в сезоне t+1:
#   (а) игрок сменил команду (team_abbr изменился), ИЛИ
#   (б) зарплата выросла ≥ 20% при той же команде (новый контракт), ИЛИ
#   (в) игрок исчез из датасета (последний наблюдаемый сезон)
#
# Ограничения метода: ~30-40% ложно-положительных (продления в середине сезона)
# Документируем это в Главе 2.2 как "heuristic labeling".

message("\n=== Маркируем contract_year (Сценарий Б — эвристика) ===")

# Загружаем per_game для получения team и salary
per_game <- read_csv("data/raw/per_game_all.csv", show_col_types = FALSE)
salaries  <- read_csv("data/raw/salaries_all.csv",  show_col_types = FALSE)

# Объединяем: нам нужна пара (player, season, team, salary) для анализа переходов
transitions <- per_game %>%
  select(player_clean, season, team_abbr) %>%
  left_join(
    select(salaries, player_clean, season, salary_usd),
    by = c("player_clean", "season")
  ) %>%
  arrange(player_clean, season)

# Добавляем данные следующего сезона для каждого игрока
transitions <- transitions %>%
  group_by(player_clean) %>%
  mutate(
    team_next    = lead(team_abbr),
    salary_next  = lead(salary_usd),
    season_next  = lead(season)
  ) %>%
  ungroup()

# Правило маркировки
cy_heuristic <- transitions %>%
  mutate(
    # (а) смена команды
    changed_team = !is.na(team_next) & team_next != team_abbr,

    # (б) зарплата выросла ≥ 20% при той же команде
    big_raise_same_team = !is.na(salary_next) &
      !changed_team &
      (salary_next / salary_usd >= 1.20),

    # (в) последний наблюдаемый сезон игрока
    last_season = is.na(team_next),

    # Итоговая маркировка
    contract_year = as.integer(changed_team | big_raise_same_team | last_season),

    # Метод маркировки (для документирования в курсовой)
    cy_method = dplyr::case_when(
      changed_team         ~ "team_change",
      big_raise_same_team  ~ "salary_jump",
      last_season          ~ "last_observed",
      TRUE                 ~ "not_cy"
    )
  ) %>%
  select(player_clean, season, contract_year, cy_method)

# Сводка
cy_summary <- cy_heuristic %>%
  count(contract_year, cy_method) %>%
  arrange(desc(contract_year), desc(n))

message("\nРаспределение contract_year по методу маркировки:")
print(cy_summary)

share_cy <- mean(cy_heuristic$contract_year, na.rm = TRUE)
message("\nДоля contract_year = 1: ", round(share_cy * 100, 1),
        "% (ожидаем 25-35%)")

if (share_cy > 0.45) {
  warning("Доля contract_year слишком высока (", round(share_cy * 100, 1),
          "%). Проверь логику эвристики — возможно, salary_jump порог слишком низкий.")
}

# Сохраняем
write_csv(cy_heuristic, "data/manual/contract_year_heuristic.csv")
message("Сохранено: data/manual/contract_year_heuristic.csv")

message("\n⚠️  Это Сценарий Б (эвристика).")
message("   Сообщи Партнёру А на чек-ине, какой сценарий используем.")
message("   Если есть время на ручную разметку топ-300 → data/manual/contracts_top300.csv")


cat("\n")
cat("============================================================\n")
cat("  03_load_manual.R выполнен\n")
cat("  Следующий шаг: 04_merge_clean.R\n")
cat("============================================================\n")
