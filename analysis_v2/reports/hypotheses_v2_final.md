# Финальная нумерация гипотез (H1-H10)

**Зафиксировано:** 2026-05-22. Все главы курсовой переписываются под эту нумерацию.

---

## Структура: 10 гипотез по 5 research streams

| # | Гипотеза | Stream | Источник в v1/v2 | Статус (BH-FDR @ 5%) | Ключевой коэффициент |
|---|---|---|---|---|---|
| **H1** | Performance metrics (PPG, WS, BPM) положительно влияют на ln_salary | Mincer / productivity | v1 (был H1) | ✅ подтверждена | β_ppg = +0.04 (v1) / +0.07 (внутри mid_level v2) |
| **H2** | Возрастной профиль salary имеет форму inverted-U с пиком ~28-29 лет | Mincer / career arc | v1 (был H2) | ✅ подтверждена | peak age ≈ 29 |
| **H3** | Salary cap создаёт discrete tier structure; tier dummies одни объясняют доминирующую долю дисперсии | Institutional / CBA | v2 (был H9 старая) | ✅ подтверждена | R² = 0.85 на одних tier dummies |
| **H4** | CBA 2017 (designated extension) создаёт структурный break: post-2017 рост wage в верхнем хвосте | Institutional / CBA | v1 (был H3) | ✅ подтверждена | post_cba_2017 = +26% |
| **H5** | All-NBA selection повышает будущую salary через career signaling | Awards / signaling | v2 (был H10 старая) | ✅ подтверждена | β_{all_nba_lag1} = +0.185, p = 0.008 |
| **H6** | Awards-эффект работает с 2-3-летним лагом через contract renewal cycle | Awards / dynamics | v2 (event study) | ✅ подтверждена | τ=+2 β=+0.21, τ=+3 β=+0.22 |
| **H7** | Top-5 market teams платят premium игрокам | Market context | v2 (был H8 старая) | ❌ rejected anti-direction | β_top5 = −0.098, p = 0.022 |
| **H8** | Team success (W%, playoffs, luxury tax) → individual salary premium | Team context | v2 | ❌ informative null | все p > 0.15 |
| **H9** | State income tax влияет на salary | Tax / externalities | v1 (был H4) | ❌ informative null | p > 0.27 |
| **H10** | Durability (games missed) снижает salary | Health / risk | v2 (был H11 старая) | ✅ подтверждена | β = −0.005/game, 30 пропусков = −15% |

**Итого:** 7 из 10 гипотез подтверждены при BH-FDR 5%. 5 выживают консервативный Bonferroni.

---

## Sub-findings (не отдельные гипотезы, но фигурируют в Results / Discussion)

- **Aging-veteran discount:** multi_all_nba (≥3 selections) carries β = −0.22 — survival-bias эффект, относится к Stream 3 (Awards).
- **Tier-specific Mincer:** β_ppg внутри max_30-tier падает в 2.3× vs mid_level — cap-induced concavity, относится к H3.
- **Aging × elite penalty:** взаимодействие multi_all_nba × age² — penalty концентрируется в декаданс-фазе, относится к H5/H6.

---

## Что выпало из старой нумерации

| Старая нумерация | Содержание | Куда переходит |
|---|---|---|
| v1 H5 | Race / draft pick effect | Limitations (один параграф) |
| v1 H6 | Contract year deep dive | Limitations + 1 строка результата |
| v1 H7 | Current-season allstar | Поглощается H5 (career-history доминирует) |

---

## Mapping на research streams для Lit Review

| Stream | Hypotheses | Ключевые источники |
|---|---|---|
| **1. Productivity / Mincer** | H1, H2 | Rosen (1981), Mincer (1974), Hill & Groothuis (2001), Krautmann (1999) |
| **2. Institutional / CBA** | H3, H4 | Coon CBA FAQ, Hill & Groothuis (2001), Rosen (1986) |
| **3. Awards / signaling** | H5, H6 | Lazear & Rosen (1981), Hausman & Leonard (1997), Stiroh (2007) |
| **4. Market / team context** | H7, H8 | Hembre (2021), Berri et al. (2007), Kahn (2000) |
| **5. Externalities / health** | H9, H10 | Yang & Lin (2012), Krautmann (1999), Kleven et al. (2013), Alm et al. (2012), Johnson & Hall (2017) |

Этот mapping = структура Глав 2 (Literature Review) и 5 (Discussion).
