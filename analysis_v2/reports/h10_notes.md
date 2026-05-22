# H10 — Awards channel: discussion notes

Sample: 2268 player-seasons.

## Three spec headline results

M10a (cumulative cumsums) — see m1_full_notes for coefficients.

**M10a_robust (binary indicators)** — cleaner interpretation:
- all_nba_lag1: β = +0.1591, SE = 0.0788, p = 0.0437
- has_career_all_nba: β = +0.0252, SE = 0.0944, p = 0.7898
- multi_all_nba: β = -0.2198, SE = 0.1058, p = 0.0380
- has_career_allstar: β = +0.3311, SE = 0.0830, p = 0.0001

**M10b (supermax_eligible_loose substitution):**
- supermax_eligible_loose: β = +0.1304, SE = 0.0789, p = 0.0987
- career_allstar_count: β = +0.0804, SE = 0.0273, p = 0.0033

## Event study around first All-NBA (τ in years)

Pre-event years (τ < 0) should be close to 0 — no anticipation.
Lag-1 (τ = +1) is the headline: salary jump *after* first All-NBA,
conditional on contemporaneous performance.

- τ =   -2: β = -0.2086, CI95 = [-0.5376, +0.1203]
- τ =   -1: β = -0.1529, CI95 = [-0.4674, +0.1616]
- τ =    0: β = -0.2405, CI95 = [-0.5110, +0.0300]*
- τ =   +1: β = +0.1652, CI95 = [-0.0382, +0.3686]
- τ =   +2: β = +0.2121, CI95 = [+0.0217, +0.4024]**
- τ =   +3: β = +0.2234, CI95 = [+0.0133, +0.4334]**
- τ = 4plus: β = -0.1116, CI95 = [-0.3342, +0.1111]
