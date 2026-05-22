"""M2 V1 — salary regression with state tax. Перезапуск с Toronto в выборке.

V1 vs V0: state_tax_rate теперь определён для TOR (107 наблюдений), что
существенно расширяет верхнюю часть распределения tax (TOR ≈ 53.5%).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_WITHIN)
from analysis_v1.utils_v1 import (combine_models, panel_index,  # noqa: E402
                                  prep_for_models, save_summary)


def run(df: pd.DataFrame) -> dict:
    print("\n" + "=" * 72)
    print("STEP 4 (V1): M2 regression with state tax")
    print("=" * 72)

    d = prep_for_models(df, restrict_single_team=True)
    d = d.dropna(subset=["state_tax_rate", "no_income_tax"])
    print(f"Sample: {len(d)} player-seasons (single-team, tax matched)")
    print(f"TOR rows in sample: {(d['team_abbr']=='TOR').sum()}")

    d = panel_index(d)
    y = d["ln_salary"]

    X2a = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT])
    m2a = PanelOLS(y, X2a, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m2a, "M2a_base_restricted")

    X2b = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT + ["no_income_tax"]])
    m2b = PanelOLS(y, X2b, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m2b, "M2b_no_income_tax")

    X2c = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT + ["state_tax_rate"]])
    m2c = PanelOLS(y, X2c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m2c, "M2c_state_tax_rate")

    X2d = d[COMBINED_STATS + COMMON_WITHIN + ["no_income_tax"]]
    m2d = PanelOLS(y, X2d, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m2d, "M2d_playerFE_no_income_tax")

    combine_models(
        {"M2a (base)": m2a,
         "M2b (+no_income_tax)": m2b,
         "M2c (+state_tax_rate)": m2c,
         "M2d (within, +no_income_tax)": m2d},
        "M2_all_models.csv",
    )

    print(f"\nM2a: R²={m2a.rsquared:.4f}")
    for label, model, key in [("M2b", m2b, "no_income_tax"),
                              ("M2c", m2c, "state_tax_rate"),
                              ("M2d (within)", m2d, "no_income_tax")]:
        if key in model.params.index:
            print(f"{label}: {key} = {model.params[key]:.4f} "
                  f"(p={model.pvalues[key]:.4f})")
    return {"M2a": m2a, "M2b": m2b, "M2c": m2c, "M2d": m2d}
