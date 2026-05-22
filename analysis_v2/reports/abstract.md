# Аннотация (HSE-формат: RU 250 + EN 250 слов)

## Русская версия

Работа эмпирически декомпозирует вариацию логарифма реальной зарплаты NBA-игрока на тематические блоки факторов в эпоху post-2011 CBA. Используется собранная автором панель 3 660 player-seasons (953 уникальных игрока × 9 сезонов 2015/16–2023/24) на основе Basketball-Reference и Hoopshype. Панель расширена семью новыми блоками: страна рождения (100% покрытие), история наград (All-NBA / MVP / DPOY лаги и cumulative counts), supermax-eligibility согласно CBA 2017, rule-based contract tier classifier (8 категорий), team season records, размер рынка (Nielsen DMA + MSA population), durability (games missed lag).

Эконометрика включает Mincer-расширения с year fixed effects и cluster-robust SE на player_id, tier-specific регрессии, event study вокруг первого All-NBA, **Shapley-декомпозицию R²** по 9 блокам (order-independent attribution), wild-cluster bootstrap, Oster δ-sensitivity, multiple-testing corrections (Bonferroni и BH-FDR).

Главный методологический результат — количественная иерархия факторов: Performance + Age = 65.5% объяснённой дисперсии; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International ≈ 2.4%. Из десяти гипотез (H1–H10) семь подтверждены при BH-FDR 5%. Salary cap создаёт near-deterministic institutional layer (tier dummies одни дают R² = 0.85), модулирующий performance-pricing через discrete category jumps. Премии за крупный рынок нет — обнаружен дисконт ≈10% (anti-marketability, направление согласуется с Hembre, 2022). Awards channel работает с 2-3-летней задержкой через contract renewal cycle. Multi-time All-NBA игроки в фазе decline несут residual penalty −22% — sub-finding survival bias.

**Ключевые слова:** NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.

---

## English version

This paper empirically decomposes the variance of log real NBA player salary into thematic factor blocks under the post-2011 CBA. We use a self-scraped panel of 3,660 player-seasons (953 unique players × 9 seasons 2015/16–2023/24) from Basketball-Reference and Hoopshype, extended with seven new blocks: birth country (100% coverage), award history (All-NBA / MVP / DPOY lags and cumulative counts), supermax eligibility under the 2017 CBA, a rule-based contract tier classifier (8 categories), team season records, market size (Nielsen DMA + MSA population), and durability (games missed lag).

Estimation includes Mincer extensions with year fixed effects and cluster-robust SE on player_id, tier-specific regressions, an event study around first All-NBA selection, **Shapley R² decomposition** over 9 blocks (order-independent attribution), wild-cluster bootstrap, Oster δ-sensitivity, and multiple-testing corrections (Bonferroni and BH-FDR).

The headline methodological result is a quantitative factor hierarchy: Performance + Age = 65.5% of explained variance; Awards = 12.2%; Demographics = 14.1%; Durability = 5.7%; Market + Team + Structural + International ≈ 2.4%. Of ten hypotheses (H1–H10), seven survive BH-FDR at 5%. The salary cap creates a near-deterministic institutional layer (tier dummies alone yield R² = 0.85), modulating performance-pricing via discrete category jumps. There is no large-market premium — instead a ≈10% discount (anti-marketability, direction consistent with Hembre, 2022). The awards channel operates with a 2–3 year lag via the contract renewal cycle. Multi-time All-NBA players in decline carry a residual penalty of −22% — a survival-bias sub-finding.

**Keywords:** NBA, panel data, Mincer regression, salary cap, contract tiers, Shapley decomposition, market size, awards channel, durability discount.
