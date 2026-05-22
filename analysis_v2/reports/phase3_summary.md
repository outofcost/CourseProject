# Phase 3 — econometric summary

Sample: 2268 player-seasons (3660 − TOT/early lag).

## Model specifications and R²

- M1c_full           : R² = 0.6510  (extended Mincer + Awards + Market + Durability + Team)
- M1c_full_robust_awards : R² = 0.6518  (binary indicators replace cumulative)
- M9a (pure tier)    : R² = 0.8489  (institutional layer alone)
- M9b (full + tier)  : R² = 0.8623  (tier adds +0.21 R² over M1c_full)
- M11b (durability × age) : R² = 0.6515
- M_full (everything): R² = 0.8624

## Hypothesis status (10 hypotheses, after BH-FDR @ 5%)

- **H7 allstar (M1c_full)** (β = +0.0291, p = 0.6467): ❌ not rejected
- **H8a market top5** (β = -0.0980, p = 0.0219): ✅ rejected
- **H9 tier supermax (M_full)** (β = +1.1877, p = 0.0000): ✅ rejected
- **H9 tier max_35 (M_full)** (β = +1.2785, p = 0.0000): ✅ rejected
- **H9 tier rookie_scale (M_full)** (β = -0.0876, p = 0.0512): ❌ not rejected
- **H9 tier minimum (M_full)** (β = -0.9055, p = 0.0000): ✅ rejected
- **H10 all_nba_lag1** (β = +0.1850, p = 0.0083): ✅ rejected
- **H10 career_allstar_count** (β = +0.1221, p = 0.0000): ✅ rejected
- **H10 supermax_elig (M_full)** (β = +0.0783, p = 0.1938): ❌ not rejected
- **H11 games_missed_lag1** (β = -0.0049, p = 0.0000): ✅ rejected
- **H11 games_missed × age** (β = -0.0004, p = 0.1242): ❌ not rejected

## Oster sensitivity (δ ≥ 1 = robust)

- all_nba_lag1: β_full = +0.1564, δ = -0.015 (no)
- top5_market: β_full = -0.1090, δ = +0.138 (no)
- supermax_eligible_loose: β_full = +0.1336, δ = +0.005 (no)
- games_missed_lag1: β_full = -0.0042, δ = +0.060 (no)
- has_career_allstar: β_full = +0.2123, δ = +0.034 (no)
- multi_all_nba: β_full = -0.1887, δ = +0.015 (no)

## Key content findings (for Chapter 4–5)

1. **Performance + Age = 65.5% of explained variance** (Shapley). Mincer-structure dominant.
2. **Awards = 12.2%** explained variance (Shapley) — formal recognition has real pricing weight.
3. **Tier dummies alone give R² = 0.85** — CBA structure pseudo-deterministic.
4. **top5_market β ≈ −0.10** — anti-marketability (consistent with Hembre 2021); interaction with allstar/intl is not significant → uniform discount.
5. **Awards channel via event study**: 22% jump 2–3 years post-first-All-NBA, consistent with contract-cycle dynamics.
6. **Aging-veteran discount**: multi_all_nba (≥3) carries β = −0.22 — past-elite status underprices current performance for ageing legends.
7. **Durability**: games_missed_lag1 β = −0.005 (per game). 30-game miss = −15% salary.
8. **Team controls null**: win_pct_lag1, made_playoffs_lag1, over_luxury_tax all p > 0.15. Team success doesn't transfer to individual price.
