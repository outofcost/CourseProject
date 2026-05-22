"""M1 V1 — base salary regressions, перезапуск на data_analysis_v1.csv.

V1 vs V0: только данные (experience fix для undrafted, Toronto in tax,
shooting % flags). Спецификация М1a–М1d идентична V0.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (BASIC_STATS, COMBINED_STATS,  # noqa: E402
                             COMMON_NO_STRUCT, COMMON_STRUCT, COMMON_WITHIN)
from analysis_v1.utils_v1 import (combine_models, panel_index,  # noqa: E402
                                  prep_for_models, save_summary)


def run(df: pd.DataFrame) -> dict:
    print("\n" + "=" * 72)
    print("STEP 3 (V1): M1 base regression")
    print("=" * 72)

    d = prep_for_models(df, restrict_single_team=False)
    print(f"Sample: {len(d)} player-seasons (full, incl. 2TM/3TM/4TM)")

    d = panel_index(d)
    y = d["ln_salary"]

    X1a = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT])
    m1a = PooledOLS(y, X1a).fit(cov_type="clustered", cluster_entity=True)
    save_summary(m1a, "M1a_pooled_basic")

    X1b = sm.add_constant(d[BASIC_STATS + COMMON_NO_STRUCT])
    m1b = PanelOLS(y, X1b, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m1b, "M1b_basic_yearFE")

    X1c = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT])
    m1c = PanelOLS(y, X1c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m1c, "M1c_combined_yearFE")

    X1d = d[COMBINED_STATS + COMMON_WITHIN]
    m1d = PanelOLS(y, X1d, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m1d, "M1d_2wayFE_combined")

    combine_models(
        {"M1a (pooled, basic)": m1a,
         "M1b (basic, year FE)": m1b,
         "M1c (combined, year FE)": m1c,
         "M1d (combined, player+year FE)": m1d},
        "M1_all_models.csv",
    )

    print(f"\nM1a: nobs={int(m1a.nobs)}, R²={m1a.rsquared:.4f}")
    print(f"M1b: nobs={int(m1b.nobs)}, R²={m1b.rsquared:.4f}")
    print(f"M1c: nobs={int(m1c.nobs)}, R²={m1c.rsquared:.4f}")
    print(f"M1d (within): nobs={int(m1d.nobs)}, R²_within={m1d.rsquared_within:.4f}")
    for v in ("post_cba_2017", "post_covid"):
        if v in m1a.params.index:
            print(f"M1a: {v} = {m1a.params[v]:.4f} (p={m1a.pvalues[v]:.4f})")

    return {"M1a": m1a, "M1b": m1b, "M1c": m1c, "M1d": m1d}
