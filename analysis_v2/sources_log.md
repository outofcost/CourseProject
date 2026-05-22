# sources_log — журнал источников фазы 1

Один блок на новую переменную / источник. Заполняется по мере сбора. Цель — чтобы каждое значение в `data_analysis_v2.csv` имело traceable происхождение.

Формат каждой записи:
- **Variable(s):** имя выходной колонки
- **Primary source:** URL + дата скрейпа / составления
- **Fallback(s):** что использовали, если primary упал
- **Sanity anchors:** проверочные значения
- **Notes:** ручные правки, исключения

---

## 1.4 — Market size (manual)

- **Variable(s):** `dma_rank_us`, `msa_population_millions`, `market_size_rank_nba`, `top5_market`, `top10_market`, `media_market_revenue_proxy`
- **Primary sources:**
  - Nielsen DMA Rankings 2023/24 (`https://en.wikipedia.org/wiki/List_of_United_States_television_markets`, snapshot 2026-05-12)
  - US Census Bureau MSA population estimates (Vintage 2023; `https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-metro-and-micro-statistical-areas.html`)
  - Statistics Canada CMA 2021 для Toronto (Greater Toronto Area = 6.4M)
- **Fallback(s):** Wikipedia "List of metropolitan statistical areas" с тем же census-источником
- **Sanity anchors:**
  - NYC DMA = 1; LA = 2; Chicago = 3; Philadelphia = 4; SF Bay = 6 (по Nielsen 2023/24)
  - Memphis DMA ≈ 50+; OKC ≈ 41; New Orleans ≈ 51 — наименьшие в NBA
  - MSA pop: NY ≈ 20.1M, LA ≈ 13.2M, Toronto ≈ 6.4M (GTA), Memphis ≈ 1.34M
- **Notes:** Toronto не входит в Nielsen US DMA (Канада). `dma_rank_us` = NaN, для NA-wide ранжирования используем `market_size_rank_nba` по MSA population. `top5_market` — фиксированный список из plan3.md (NYK, BRK, LAL, LAC, CHI, GSW).

---

## 1.1 — Birth country / international

- **Variable(s):** `birth_country`, `birth_city`, `birth_date_meta`, `is_international`
- **Primary source:** Basketball-Reference player meta block (`/players/{letter}/{player_id}.html`, тег `<span itemprop="birthPlace">`)
- **Fallback(s):**
  1. NBA.com player profile (`stats.nba.com/player/{id}`)
  2. Wikipedia infobox
  3. RealGM player page
- **Sanity anchors:**
  - Curry → USA, Doncic → Slovenia, Embiid → Cameroon, Jokic → Serbia, Antetokounmpo → Greece, Wembanyama → France
  - Ожидаемая доля USA: 70–75%
- **Notes:** TBD после первого прогона.

---

## 1.2 — Awards (All-NBA, All-Defensive, MVP, DPOY)

- **Variable(s):** `all_nba_team` (0/1/2/3), `all_defense_team` (0/1/2), `mvp` (0/1), `dpoy` (0/1)
- **Primary source:**
  - `https://www.basketball-reference.com/awards/all_league.html`
  - `https://www.basketball-reference.com/awards/all_defense.html`
  - `https://www.basketball-reference.com/awards/mvp.html`
  - `https://www.basketball-reference.com/awards/dpoy.html`
- **Fallback(s):** Wikipedia "All-NBA Team" по сезонам, NBA.com/history/awards
- **Sanity anchors:**
  - 2015/16: MVP = Curry (unanimous), DPOY = Kawhi Leonard
  - 2016/17: MVP = Westbrook, All-NBA First includes him
  - 2022/23: MVP = Embiid, DPOY = Jaren Jackson Jr.
  - Ровно 15 All-NBA / 10 All-Defense / 1 MVP / 1 DPOY в сезон
- **Notes:** TBD после прогона.

---

## 1.5.1 — CBA thresholds (manual lookup)

- **Variable(s):** `cap`, `luxury_tax`, `apron_first`, `apron_second`, `mle_taxpayer`, `mle_nontaxpayer`, `biannual`, `max_25_pct`, `max_30_pct`, `max_35_pct`, `min_salary_0yrs`, `min_salary_10yrs`
- **Primary source:** Coon's CBA FAQ (`https://cbafaq.com/`)
- **Secondary:** Basketball-Reference `/contracts/salary-cap-history.html`, HoopsRumors archive
- **Sanity anchors:**
  - Cap: 2015/16 = $70M, 2016/17 = $94M (TV cap spike), 2023/24 ≈ $136.0M
  - Cap должен расти монотонно, за исключением 2020/21 (flat $109.1M из-за COVID)
  - Max %: 25 (0–6 лет), 30 (7–9 лет), 35 (10+ лет)
- **Notes:** Значения собраны на 2026-05-12. Цифры округлены до миллионов, точные значения хранятся в `cba_thresholds.csv`.

---

## 1.6 — Team records (TBD)
## 1.7 — Durability (derived, no external source)
## 1.8 — Agency (TBD, priority 3)
## 1.9 — Jersey sales (TBD, priority 3)
