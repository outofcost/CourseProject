# Этап 2 — Внешняя валидация cy-прокси (резюме)

**Источник истины:** Wikipedia-страницы 22 высокозарплатных игроков.
Контрактным годом считаем сезон t, после которого (между t и t+1) произошло контрактное событие: подписание нового контракта, extension, opt-in/opt-out с переходом, межсезонный trade.

**Ограничения.** Spotrac недоступен; ручная проверка ограничена 22 топ-игроками по cap-share (~5% выборки).
Это даёт оценку recall **в сегменте high-salary players** — где истинные contract years наиболее заметны.

## 2.1. Валидационный набор

- Игроков: 22
- Player-seasons: 186
- Из них cy_truth = 1: 66
- cy_truth = 0: 120

## 2.2. Метрики качества прокси

| pred           |   n_eval |   n_truth_1 |   n_pred_1 |   TP |   FP |   FN |   TN |   TPR_recall |    FPR |   precision |     F1 |   accuracy |
|:---------------|---------:|------------:|-----------:|-----:|-----:|-----:|-----:|-------------:|-------:|------------:|-------:|-----------:|
| cy_exogenous   |      149 |          54 |         27 |   20 |    7 |   34 |   88 |       0.3704 | 0.0737 |      0.7407 | 0.4938 |     0.7248 |
| contract_year  |      149 |          54 |         45 |   27 |   18 |   27 |   77 |       0.5    | 0.1895 |      0.6    | 0.5455 |     0.698  |
| cy_A_up        |      155 |          54 |         22 |   10 |   12 |   44 |   89 |       0.1852 | 0.1188 |      0.4545 | 0.2632 |     0.6387 |
| cy_B_offseason |      149 |          54 |         21 |   17 |    4 |   37 |   91 |       0.3148 | 0.0421 |      0.8095 | 0.4533 |     0.7248 |
| cy_C           |      186 |          66 |          6 |    3 |    3 |   63 |  117 |       0.0455 | 0.025  |      0.5    | 0.0833 |     0.6452 |


Ключевые числа:
- **cy_exogenous: TPR (recall) = 37.0%** (захватывает только 20 из 54 истинных contract years).
- **contract_year (composite): TPR = 50.0%**.
- Это — оценка снизу: если cy_exogenous пропускает >40% contract years даже на high-salary подвыборке,
  то на всей выборке (где доминируют средние контракты) recall может быть ещё ниже.

## 2.3. Примеры пропущенных истинных contract years (cy_exogenous=0, cy_truth=1)

| player_name           |   season | team_abbr   |   real_salary_change |   cy_A_up |   cy_B_offseason |   cy_C |   contract_year |
|:----------------------|---------:|:------------|---------------------:|----------:|-----------------:|-------:|----------------:|
| Stephen Curry         |     2016 | GSW         |               -0.208 |         0 |                0 |      0 |               0 |
| Stephen Curry         |     2017 | GSW         |                1.719 |         1 |                0 |      0 |               1 |
| Stephen Curry         |     2021 | GSW         |                0.033 |         0 |                0 |      0 |               0 |
| LeBron James          |     2016 | CLE         |                0.003 |         0 |                0 |      0 |               0 |
| LeBron James          |     2017 | CLE         |                0.021 |         0 |                0 |      0 |               0 |
| LeBron James          |     2019 | LAL         |               -0.019 |         0 |                0 |      0 |               0 |
| LeBron James          |     2022 | LAL         |               -0.019 |         0 |                0 |      0 |               0 |
| Damian Lillard        |     2016 | POR         |                3.272 |         1 |                0 |      0 |               1 |
| Damian Lillard        |     2020 | POR         |                0.061 |         0 |                0 |      0 |               0 |
| Kevin Durant          |     2017 | GSW         |               -0.106 |         0 |                0 |      0 |               0 |
| Kevin Durant          |     2018 | GSW         |                0.167 |         0 |                0 |      0 |               0 |
| Russell Westbrook     |     2016 | OKC         |                0.179 |         0 |                0 |      0 |               0 |
| Russell Westbrook     |     2017 | OKC         |                0.012 |         0 |                0 |      0 |               0 |
| James Harden          |     2017 | HOU         |                0.012 |         0 |                0 |      0 |               0 |
| Giannis Antetokounmpo |     2020 | MIL         |                0.065 |         0 |                0 |      0 |               0 |
| Giannis Antetokounmpo |     2023 | MIL         |               -0.023 |         0 |                0 |      0 |               0 |
| Joel Embiid           |     2018 | PHI         |                3.06  |         1 |                0 |      0 |               1 |
| Joel Embiid           |     2021 | PHI         |                0.038 |         0 |                0 |      0 |               0 |
| Anthony Davis         |     2020 | LAL         |                0.209 |         0 |                0 |      0 |               0 |
| Anthony Davis         |     2023 | LAL         |               -0.028 |         0 |                0 |      0 |               0 |
| Kawhi Leonard         |     2021 | LAC         |                0.2   |         0 |                0 |      0 |               0 |
| Jimmy Butler          |     2021 | MIA         |                0.017 |         0 |                0 |      0 |               0 |
| Paul George           |     2020 | LAC         |                0.074 |         0 |                0 |      0 |               0 |
| Klay Thompson         |     2018 | GSW         |                0.036 |         0 |                0 |      0 |               0 |
| Chris Paul            |     2018 | HOU         |                0.429 |         1 |                0 |      0 |               1 |


**Содержательно.** Это в основном extensions со своей командой (Curry 2017 supermax, Lillard 2020, Antetokounmpo 2020, Embiid 2021/2024, Jokić 2018/2022, Tatum 2020/2024 и т.д.). Все они истинные contract years, но `cy_B_offseason = 0` (тот же клуб) и `cy_C = 0` (не rookie endpoint), поэтому `cy_exogenous` их пропускает. 
Многие из них при этом захватываются циркулярным `cy_A_up` (с soft-circularity).
