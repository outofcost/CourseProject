# H9 — Tier-structure hypothesis: discussion notes

Sample: 2268 player-seasons. Reference tier: mid_level.

## Headline R² jumps (institutional pricing power)

- M1c_full R² (no tiers): 0.6510
- **M9a (pure tier, no performance) R²: 0.8489** — institutional layer alone
- **M9b (M1c + tier) R²: 0.8623** — full picture
- ΔR² from tier dummies on top of M1c: +0.2113

## Tier dummy coefficients (M9b, reference = mid_level)

- **tier_minimum**: β = -0.9055, SE = 0.0308, p = 0.0000***
- **tier_rookie_scale**: β = -0.0878, SE = 0.0449, p = 0.0506*
- **tier_high_mid**: β = +0.8496, SE = 0.0367, p = 0.0000***
- **tier_max_25**: β = +1.1359, SE = 0.0396, p = 0.0000***
- **tier_max_30**: β = +1.1598, SE = 0.0502, p = 0.0000***
- **tier_max_35**: β = +1.2643, SE = 0.0613, p = 0.0000***
- **tier_supermax**: β = +1.2062, SE = 0.0840, p = 0.0000***
- **tier_overpay**: β = +1.3316, SE = 0.0631, p = 0.0000***

## Tier-specific β_ppg (truncation pattern)

If institutional CBA structure suppresses performance-pricing in the top tiers (cap-truncation) and bottom tiers (rookie/min slot), then β_ppg should be highest inside `mid_level` and close to zero in `max_*` and `rookie_scale`.

- minimum       : n=307, β_ppg = +0.0931 (p=0.004)
- rookie_scale  : n=484, β_ppg = +0.0939 (p=0.000)
- mid_level     : n=717, β_ppg = +0.0781 (p=0.017)
- high_mid      : n=442, β_ppg = +0.0706 (p=0.000)
- max_25        : n=209, β_ppg = +0.0679 (p=0.001)
- max_30        : n= 50, β_ppg = +0.0340 (p=0.012)
- supermax      : n= 33, β_ppg = +0.0670 (p=0.001)
