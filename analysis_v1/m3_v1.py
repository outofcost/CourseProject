"""M3 V1 — salary regression with contract_year. Включает M3c_canonical
(cy_exogenous, без circularity) — ключевое новшество V1.

V1 vs V0:
    contract_year — теперь без cy_A_down (pay-cut), без cy_B_trade
        (mid-season trade). Состав: max(cy_A_up, cy_B_offseason, cy_C).
    M3c_canonical — Δlog_salary ~ cy_exogenous = max(cy_B_offseason, cy_C).
        Этот сигнал не использует s_{t+1}, поэтому регрессия корректна
        (без circularity, в отличие от M3c с composite contract_year).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_WITHIN)
from analysis_v1.utils_v1 import (combine_models, panel_index,  # noqa: E402
                                  prep_for_models, save_summary)


def _fit(y, X, **kw):
    return PanelOLS(y, X, time_effects=True, **kw).fit(
        cov_type="clustered", cluster_entity=True
    )


def run(df: pd.DataFrame) -> dict:
    print("\n" + "=" * 72)
    print("STEP 5 (V1): M3 regression with contract_year + cy_exogenous")
    print("=" * 72)

    d = prep_for_models(df, restrict_single_team=True)
    d = d.dropna(subset=["contract_year"])
    d["contract_year"] = d["contract_year"].astype(int)
    print(f"Sample: {len(d)} player-seasons (single-team, contract_year observed)")

    d_idx = panel_index(d)
    y = d_idx["ln_salary"]

    # ── M3a level ────────────────────────────────────────────────────────
    X3a = sm.add_constant(d_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["contract_year"]])
    m3a = _fit(y, X3a)
    save_summary(m3a, "M3a_contract_year_level")

    # ── M3b interactions ─────────────────────────────────────────────────
    d2 = d_idx.copy()
    d2["cy_x_ppg"] = d2["contract_year"] * d2["ppg"]
    d2["cy_x_per"] = d2["contract_year"] * d2["per"]
    d2["cy_x_allstar"] = d2["contract_year"] * d2["allstar"]
    X3b = sm.add_constant(d2[COMBINED_STATS + COMMON_NO_STRUCT + [
        "contract_year", "cy_x_ppg", "cy_x_per", "cy_x_allstar"]])
    m3b = _fit(y, X3b)
    save_summary(m3b, "M3b_contract_year_interactions")

    # ── M3c Δ log_salary canonical with composite contract_year (с circularity) ──
    d_chg = d.dropna(subset=["salary_next"]).copy()
    d_chg["ln_salary_next"] = np.log(d_chg["salary_next"])
    d_chg["dln_salary"] = d_chg["ln_salary_next"] - d_chg["ln_salary"]
    d_chg_idx = d_chg.set_index(["player_id", "season"])
    y_chg = d_chg_idx["dln_salary"]
    X3c = sm.add_constant(
        d_chg_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["contract_year"]]
    )
    m3c = _fit(y_chg, X3c)
    save_summary(m3c, "M3c_delta_salary_composite_cy")

    # ── M3c_canonical: Δ log_salary on cy_exogenous (без circularity) ────
    d_chg_x = d_chg.dropna(subset=["cy_exogenous"]).copy()
    d_chg_x["cy_exogenous"] = d_chg_x["cy_exogenous"].astype(int)
    d_chg_x_idx = d_chg_x.set_index(["player_id", "season"])
    y_chg_x = d_chg_x_idx["dln_salary"]
    X3c_can = sm.add_constant(
        d_chg_x_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["cy_exogenous"]]
    )
    m3c_canonical = _fit(y_chg_x, X3c_can)
    save_summary(m3c_canonical, "M3c_canonical_cy_exogenous")

    # ── M3c_A_up: Δ log_salary on cy_A_up (намеренно circular — для контраста) ──
    d_chg_a = d_chg.dropna(subset=["cy_A_up"]).copy()
    d_chg_a["cy_A_up"] = d_chg_a["cy_A_up"].astype(int)
    d_chg_a_idx = d_chg_a.set_index(["player_id", "season"])
    y_chg_a = d_chg_a_idx["dln_salary"]
    X3c_a = sm.add_constant(
        d_chg_a_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["cy_A_up"]]
    )
    m3c_A = _fit(y_chg_a, X3c_a)
    save_summary(m3c_A, "M3c_circular_cy_A_up")

    # ── M3d 2-way FE ─────────────────────────────────────────────────────
    X3d = d_idx[COMBINED_STATS + COMMON_WITHIN + ["contract_year"]]
    m3d = PanelOLS(y, X3d, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(m3d, "M3d_2wayFE_contract_year")

    combine_models(
        {"M3a (level)": m3a,
         "M3b (level + interactions)": m3b,
         "M3c (Δ, composite cy)": m3c,
         "M3c_canonical (Δ, cy_exogenous)": m3c_canonical,
         "M3c_circular (Δ, cy_A_up)": m3c_A,
         "M3d (within)": m3d},
        "M3_all_models.csv",
    )

    for label, model, key in [
        ("M3a level", m3a, "contract_year"),
        ("M3c (composite)", m3c, "contract_year"),
        ("M3c_canonical", m3c_canonical, "cy_exogenous"),
        ("M3c_circular (cy_A_up)", m3c_A, "cy_A_up"),
        ("M3d within", m3d, "contract_year"),
    ]:
        if key in model.params.index:
            print(f"{label}: {key} = {model.params[key]:.4f} "
                  f"(p={model.pvalues[key]:.4f})")

    return {"M3a": m3a, "M3b": m3b, "M3c": m3c,
            "M3c_canonical": m3c_canonical, "M3c_circular": m3c_A, "M3d": m3d}
