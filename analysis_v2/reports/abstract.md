# Аннотация (драфт, ~300 слов)

## Русская версия

Работа эмпирически декомпозирует вариацию зарплаты игроков NBA на блоки факторов: производительность, человеческий капитал, демография, награды, durability, рыночные характеристики, команда, структурные изменения. Используется собственноручно собранная панель 3 660 player-seasons (953 уникальных игрока × 9 сезонов 2015/16–2023/24), сформированная скрейпингом Basketball-Reference и Hoopshype с применением curl_cffi для обхода Cloudflare и Wayback Machine для исторических salary-снапшотов. Панель расширена 7 блоками новых переменных: страна рождения (100% покрытие), All-NBA/MVP/DPOY history (lags + cumulative counts), supermax-eligibility согласно CBA 2017, rule-based contract tier classifier (8 категорий с CBA-thresholds), team season records (W-L, playoff round), market size (Nielsen DMA + MSA population), durability (games missed lag).

Эконометрический анализ включает Mincer-расширения с year fixed effects и cluster-robust SE на player_id, two-way fixed effects panel models, tier-specific регрессии, event study вокруг первого All-NBA, **Shapley-декомпозиция R² на 9 блоков** (order-independent attribution), wild-cluster bootstrap для interaction-коэффициентов, Oster (2019) δ-sensitivity, multiple-testing corrections (Bonferroni и BH-FDR).

Главный новый результат — **количественная иерархия факторов**: Performance + Age = 65.5% объяснённой дисперсии; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International суммарно ≈ 2.4%. Из 10 ключевых гипотез (H1–H10) 7 подтверждены при контроле multiple testing (BH-FDR 5%). Salary cap создаёт quasi-deterministic institutional layer (tier dummies одни дают R² = 0.85), модулирующий performance-pricing через discrete category jumps. Market-size премии нет — обнаружен дисконт ~10% для крупных рынков (anti-marketability, согласуется с Hembre, 2022). Awards channel работает с 2-3-летней задержкой через contract renewal cycle. Multi-time All-NBA игроки в фазе decline получают penalty −22% — survival bias эффект aging-vet selection.

**Объём данных**: 3 660 × 153 переменных, 23 спецификации регрессий, 7 рисунков, 9 раундов sanity-валидации, регресс-тест воспроизводимости v1 (max coef diff < 5×10⁻⁵). Воспроизводимый код: `analysis_v2/` package, Python 3.13 + statsmodels + linearmodels.

**Ключевые слова**: NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.

---

## English version (~300 words)

This work empirically decomposes the variance of NBA player salaries into factor blocks: performance, human capital, demographics, awards, durability, market characteristics, team, structural changes. We use a self-scraped panel of 3,660 player-seasons (953 unique players × 9 seasons 2015/16–2023/24), assembled via Basketball-Reference and Hoopshype scraping with curl_cffi for Cloudflare bypass and Wayback Machine for historical salary snapshots. The panel extends v1 with 7 new blocks: birth country (100% coverage), All-NBA/MVP/DPOY history (lags + cumulative counts), supermax eligibility per 2017 CBA, rule-based contract tier classifier (8 categories with CBA thresholds), team season records (W-L, playoff round), market size (Nielsen DMA + MSA population), durability (games missed lag).

Econometric analysis includes Mincer extensions with year fixed effects and cluster-robust SE on player_id, two-way fixed effects panel models, tier-specific regressions, event study around first All-NBA selection, **Shapley R² decomposition over 9 blocks** (order-independent attribution), wild-cluster bootstrap for interaction coefficients, Oster (2019) δ-sensitivity, multiple testing corrections (Bonferroni and BH-FDR).

The headline new finding is a **quantitative hierarchy of factors**: Performance + Age = 65.5% of explained variance; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International jointly ≈ 2.4%. Of 10 key hypotheses (H1–H10), 7 survive multiple testing (BH-FDR 5%). Salary cap creates a quasi-deterministic institutional layer (tier dummies alone yield R² = 0.85), modulating performance-pricing via discrete category jumps. No market-size premium found — a ~10% discount detected for large-market teams (anti-marketability, consistent with Hembre, 2022). Awards channel operates with 2-3 year lag through contract renewal cycle. Multi-time All-NBA players in decline phase receive −22% penalty — survival-bias effect of aging-vet selection.

**Data extent**: 3,660 × 153 variables, 23 regression specifications, 7 figures, 9 rounds of sanity validation, v1 reproducibility test (max coef diff < 5×10⁻⁵). Reproducible code: `analysis_v2/` package, Python 3.13 + statsmodels + linearmodels.

**Keywords**: NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.
