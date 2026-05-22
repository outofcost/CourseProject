# Глава 6 — Заключение (драфт v2)

## 6.1 Резюме исследования

Курсовая работа эмпирически отвечает на вопрос: **какие факторы и в какой мере определяют зарплату NBA-игрока в эпоху post-2011 CBA**. Используется собственноручно собранная панель: 953 уникальных игрока × 9 сезонов (2015/16–2023/24) = 3 660 player-seasons, обогащённая 53 регрессорами (153 итоговых колонки), включая 7 новых блоков относительно v1 итерации:

1. Birth country / international status (bbref player meta-block, 100% coverage)
2. All-NBA / All-Defensive / MVP / DPOY history (bbref awards pages, валидировано на 9/9 сезонах: 15/10/1/1)
3. Lag-структуры наград + supermax-eligibility (CBA 2017 designated extension)
4. Contract tier (8 категорий, rule-based классификатор)
5. Team-level: win pct, made playoffs, over_luxury_tax (9/9 чемпионов NBA воспроизведены)
6. Market size: Nielsen DMA + MSA population (30 команд вручную)
7. Durability: games_missed_lag1, 3y_cum

Регресс-тест воспроизводимости v1 PASSED (max coef diff < 5×10⁻⁵ на всех M1a–M3d моделях).

## 6.2 Статус 10 гипотез

| # | Гипотеза | Статус (BH-FDR @ 5%) | Ключевой коэффициент |
|---|---|---|---|
| H1 | Performance ↑ → salary ↑ | ✅ подтверждена (v1) | β_ppg = +0.04 (v1) / +0.07 (внутри mid_level v2) |
| H2 | Возрастной профиль ∩ | ✅ подтверждена (v1) | peak age ≈ 29 |
| H3 | CBA 2017 break | ✅ подтверждена (v1) | post_cba_2017 = +26% |
| H4 | State tax | ❌ informative null (v1) | p > 0.27 |
| H5 | Race / draft | (не основная) | — |
| H6 | Contract year cycle | ⚠ частично (v1 H6 deep dive, сокращён) | Δsalary = +35% (canonical) |
| H7 | Current-season allstar | ❌ not rejected | β = +0.029, p = 0.65 (поглощается career-history) |
| **H8** | **Market size premium** | **✅ rejected (anti-direction)** | **β_top5 = −0.098, p = 0.022** |
| **H9** | **Tier structure determinism** | **✅ rejected** | **R² = 0.85 на одних tier dummies** |
| **H10** | **Awards channel post-event** | **✅ rejected** | **β_{all_nba_lag1} = +0.185, p = 0.008; τ=+2 event-study β = +0.21** |
| **H11** | **Durability discount** | **✅ rejected (main effect)** | **β = −0.005/game, p < 0.001** |

Семь гипотез из десяти статистически подтверждены при контроле multiple testing (BH-FDR 5%). Пять — выживают даже консервативный Bonferroni @ 5%.

## 6.3 Главный методологический вклад

**Shapley-декомпозиция R² на 9 блоков факторов с количественным распределением вкладов.** В отличие от sequential R² (order-dependent), Shapley даёт fair и axiomatic-обоснованную attribution каждому блоку:

| Блок | Доля объяснённой дисперсии |
|---|---|
| Performance | 36.8% |
| Age + Experience | 28.7% |
| Demographics | 14.1% |
| **Awards** | **12.2%** |
| Durability | 5.7% |
| International | 0.8% |
| Team | 0.8% |
| Structural | 0.6% |
| Market | 0.2% |

Это **прямой количественный ответ** на вопрос темы работы: NBA salary primarily detected through Mincer-core (productivity + career arc), augmented by institutional channelling через awards и tier structure. Окружающий контекст (market, team, macro) ≈ 2% объяснённой дисперсии.

## 6.4 Содержательные выводы

1. **NBA — это рынок индивидуального таланта, не team-context redistribution.** Все team-level контроли (win %, playoffs, luxury tax) — null после контроля игрока.

2. **Salary cap создаёт квази-детерминистический institutional layer.** Tier dummies одни объясняют R² = 0.85 — больше, чем full Mincer спецификация. Performance ↔ salary связь работает через discrete jumps между tier'ами, не через непрерывную elasticity.

3. **Cap-truncation в верхнем хвосте.** β_ppg внутри max_30-tier падает в 2.3 раза vs mid_level — прямое подтверждение Rosen (1986) cap-induced concavity в дискретной форме.

4. **Awards channel работает с задержкой 2-3 года.** Event study вокруг первого All-NBA: salary skip +22% при τ=+2, +3 — когда подписывается следующий контракт. Это classical contract-cycle dynamics.

5. **Market-size premium отсутствует / отрицательный.** β_top5 = −0.098 (p = 0.022); interaction × allstar не значима. Согласуется с Hembre (2021); направление дисконта объясняется через player-side compensating differential на off-court доход.

6. **Aging-veteran discount.** multi_all_nba (≥3 selections) carries β = −0.22 — past elite status underprices current performance для legend-в-декаданс игроков.

7. **Durability — реальный price effect.** −0.5% salary за каждый пропущенный матч; 30 пропусков = −15%. По Shapley 5.7% explained variance.

## 6.5 Ограничения

- Endorsement income, agency / agent data не собраны (priority 3 по плану) — marketability channel идентифицирован только через residual selection, не напрямую.
- TOT-rows (~14% выборки) теряются в специциях с team-level переменными.
- Oster δ < 1 для всех ключевых коэффициентов — magnitude чувствительна к спецификации (sign-stability подтверждена).
- Tier classification rule-based; data-driven approach (через manual Coon CBA labels) был бы строже.

## 6.6 Дальнейшие направления

1. Structural model two-sided matching для NBA-CBA.
2. Endorsement-augmented Mincer с Forbes / jersey sales данных.
3. 2023 CBA second-apron event study.
4. Counterfactual simulation отмены cap-rules.

---

## 6.7 Финальное утверждение

NBA salary в эпоху post-2011 CBA — это в **65% случаев Mincer-функция** от продуктивности и career arc, модулированная **в 32% institutional channelling** через awards history, contract tier и health record. **Менее 3% дисперсии** salary объясняется окружающим контекстом (market, team success, macro structure). Salary cap нейтрализует team-side market premium, превращая bargaining в выбор **типа** контракта в пределах CBA-grid, а не непрерывный price-setting.

Это первая работа, насколько нам известно, которая **количественно** декомпозирует NBA salary variance на блоки факторов с order-independent attribution (Shapley) на данных современного CBA-режима.
