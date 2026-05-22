"""Step 5: M3 — salary regressions with contract_year.

M3a — level: ln_salary_t on contract_year_t (cross-sectional).
M3b — + interactions contract_year × {ppg, per, allstar}.
M3c — Δln_salary_{t→t+1} on contract_year_t (canonical contract-year test).
M3d — player + year FE on level spec.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

from analysis.config import COMBINED_STATS, COMMON_NO_STRUCT, COMMON_WITHIN
from analysis.utils import combine_models, panel_index, prep_for_models, save_summary


def run(df: pd.DataFrame) -> dict:
    print("\n" + "=" * 72)
    print("STEP 5: M3 regression with contract_year")
    print("=" * 72)

    d = prep_for_models(df, restrict_single_team=True)
    d = d.dropna(subset=["contract_year"])
    d["contract_year"] = d["contract_year"].astype(int)
    print(f"Sample: {len(d)} player-seasons (single-team, contract_year observed)")

    d_idx = panel_index(d)
    y = d_idx["ln_salary"]

    X3a = sm.add_constant(d_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["contract_year"]])
    m3a = PanelOLS(y, X3a, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m3a, "M3a_contract_year_level")

    d_idx2 = d_idx.copy()
    d_idx2["cy_x_ppg"] = d_idx2["contract_year"] * d_idx2["ppg"]
    d_idx2["cy_x_per"] = d_idx2["contract_year"] * d_idx2["per"]
    d_idx2["cy_x_allstar"] = d_idx2["contract_year"] * d_idx2["allstar"]
    X3b = sm.add_constant(d_idx2[COMBINED_STATS + COMMON_NO_STRUCT + [
        "contract_year", "cy_x_ppg", "cy_x_per", "cy_x_allstar"]])
    m3b = PanelOLS(y, X3b, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m3b, "M3b_contract_year_interactions")

    # Δ ln_salary canonical contract-year test
    d_chg = d.dropna(subset=["salary_next"]).copy()
    d_chg["ln_salary_next"] = np.log(d_chg["salary_next"])
    d_chg["dln_salary"] = d_chg["ln_salary_next"] - d_chg["ln_salary"]
    d_chg_idx = d_chg.set_index(["player_id", "season"])
    y_chg = d_chg_idx["dln_salary"]
    X3c = sm.add_constant(
        d_chg_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["contract_year"]]
    )
    m3c = PanelOLS(y_chg, X3c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m3c, "M3c_delta_salary_canonical")

    X3d = d_idx[COMBINED_STATS + COMMON_WITHIN + ["contract_year"]]
    m3d = PanelOLS(y, X3d, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m3d, "M3d_2wayFE_contract_year")

    combine_models(
        {"M3a (level)": m3a,
         "M3b (level + interactions)": m3b,
         "M3c (Δ ln_salary, canonical)": m3c,
         "M3d (within)": m3d},
        "M3_all_models.csv",
    )

    for label, model in [("M3a (level)", m3a), ("M3c (Δsalary)", m3c),
                         ("M3d (within)", m3d)]:
        if "contract_year" in model.params.index:
            print(f"{label}: contract_year = "
                  f"{model.params['contract_year']:.4f} "
                  f"(p={model.pvalues['contract_year']:.4f})")
    return {"M3a": m3a, "M3b": m3b, "M3c": m3c, "M3d": m3d}
