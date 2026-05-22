"""Step 6: robustness checks.

R1 — full model: tax + contract_year jointly.
R2 — drop sub-$1M salaries (likely two-way / minimum deals).
R3 — drop rookies (experience == 0).
R4 — alternative contract_year: cy_B only (team change).
R5 — alternative contract_year: cy_A only (salary jump).
"""
from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

from analysis.config import COMBINED_STATS, COMMON_NO_STRUCT
from analysis.utils import combine_models, panel_index, prep_for_models, save_summary


def run(df: pd.DataFrame) -> dict:
    print("\n" + "=" * 72)
    print("STEP 6: robustness checks")
    print("=" * 72)

    d = prep_for_models(df, restrict_single_team=True)
    d = d.dropna(subset=["state_tax_rate", "no_income_tax", "contract_year"])
    d["contract_year"] = d["contract_year"].astype(int)

    base_cols = COMBINED_STATS + COMMON_NO_STRUCT

    d_idx = panel_index(d)
    y = d_idx["ln_salary"]
    X = sm.add_constant(d_idx[base_cols + ["no_income_tax", "contract_year"]])
    r1 = PanelOLS(y, X, time_effects=True, check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(r1, "R1_full_tax_plus_contract")

    d_high = d[d["salary_usd"] >= 1_000_000].copy()
    d_high_idx = panel_index(d_high)
    y_high = d_high_idx["ln_salary"]
    X_high = sm.add_constant(
        d_high_idx[base_cols + ["no_income_tax", "contract_year"]]
    )
    r2 = PanelOLS(y_high, X_high, time_effects=True, check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(r2, "R2_excl_minimum_contracts")
    print(f"R2: dropped {(d['salary_usd'] < 1_000_000).sum()} sub-$1M rows")

    d_vet = d[d["experience"] > 0].copy()
    d_vet_idx = panel_index(d_vet)
    y_vet = d_vet_idx["ln_salary"]
    # Drop undrafted in this sub-sample — for experience>0, undrafted players
    # have a stable history and `log_draft_pick=log(61)` constant for all of them,
    # which becomes near-collinear with the undrafted dummy after year FE.
    cols_vet = [c for c in base_cols if c not in ("undrafted",)]
    X_vet = sm.add_constant(
        d_vet_idx[cols_vet + ["no_income_tax", "contract_year"]]
    )
    r3 = PanelOLS(y_vet, X_vet, time_effects=True, check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(r3, "R3_excl_rookies")
    print(f"R3: dropped {(d['experience'] == 0).sum()} rookie rows")

    d_alt = d.copy()
    d_alt["contract_year_B"] = (d_alt["cy_B"].fillna(0) == 1).astype(int)
    d_alt_idx = panel_index(d_alt)
    y_alt = d_alt_idx["ln_salary"]
    X_alt = sm.add_constant(
        d_alt_idx[base_cols + ["no_income_tax", "contract_year_B"]]
    )
    r4 = PanelOLS(y_alt, X_alt, time_effects=True, check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(r4, "R4_alt_contract_year_team_only")

    d_alt2 = d.copy()
    d_alt2["contract_year_A"] = (d_alt2["cy_A"].fillna(0) == 1).astype(int)
    d_alt2_idx = panel_index(d_alt2)
    y_alt2 = d_alt2_idx["ln_salary"]
    X_alt2 = sm.add_constant(
        d_alt2_idx[base_cols + ["no_income_tax", "contract_year_A"]]
    )
    r5 = PanelOLS(y_alt2, X_alt2, time_effects=True, check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(r5, "R5_alt_contract_year_salary_only")

    combine_models(
        {"R1 (full)": r1,
         "R2 (excl <$1M)": r2,
         "R3 (excl rookies)": r3,
         "R4 (cy=team only)": r4,
         "R5 (cy=salary only)": r5},
        "R_robustness.csv",
    )

    print(f"\nR1: nobs={int(r1.nobs)}, R²={r1.rsquared:.4f}")
    print(f"R2: nobs={int(r2.nobs)}, R²={r2.rsquared:.4f}")
    print(f"R3: nobs={int(r3.nobs)}, R²={r3.rsquared:.4f}")
    print(f"R4: nobs={int(r4.nobs)}, R²={r4.rsquared:.4f}")
    print(f"R5: nobs={int(r5.nobs)}, R²={r5.rsquared:.4f}")
    return {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5}
