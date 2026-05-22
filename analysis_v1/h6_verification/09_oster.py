"""Этап 9. Oster (2019) sensitivity bounds для M3c_canonical.

Идея. Сравниваем коэффициент β_cy в:
    - короткой регрессии (без controls):     β_short, R²_short
    - длинной регрессии (с controls):         β_long,  R²_long

Bound β*, предполагая selection on unobservables = δ × selection on
observables и R²_max = min(1.3·R²_long, 1):

    β* = β_long − δ × (β_short − β_long) × (R²_max − R²_long) / (R²_long − R²_short)

δ — needed strength of unobserved confounding, чтобы β_true = 0:

    δ_for_zero = β_long × (R²_long − R²_short) / [(β_short − β_long) × (R²_max − R²_long)]

Для null-результатов H6 это даёт ответ на вопрос: насколько устойчив null к
omitted variable bias?

Outputs:
    output/h6_verification/09_oster_sensitivity.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.config import COMBINED_STATS, COMMON_NO_STRUCT  # noqa: E402
from analysis_v1.h6_verification.alt_cy_helper import attach_alt_cy  # noqa: E402

OUT = ROOT / "output" / "h6_verification"
OUT.mkdir(parents=True, exist_ok=True)
MULTI = {"2TM", "3TM", "4TM", "TOT"}


def fit_pair(df: pd.DataFrame, cy_var: str) -> dict:
    """Возвращает β_short, R²_short, β_long, R²_long на одной выборке."""
    d = df[~df["team_abbr"].isin(MULTI)].copy()
    need = ["ln_salary", "salary_next", "salary_usd",
            cy_var] + COMBINED_STATS + COMMON_NO_STRUCT
    d = d.dropna(subset=need)
    d["dln_salary"] = np.log(d["salary_next"]) - np.log(d["salary_usd"])
    d[cy_var] = d[cy_var].astype(int)
    d = d.set_index(["player_id", "season"])

    # Short: только cy_var + year FE
    Xs = sm.add_constant(d[[cy_var]])
    rs = PanelOLS(d["dln_salary"], Xs, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    # Long: cy_var + stats + struct + year FE
    Xl = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT + [cy_var]])
    rl = PanelOLS(d["dln_salary"], Xl, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    return {
        "cy_var":      cy_var,
        "n":           int(rs.nobs),
        "beta_short":  float(rs.params[cy_var]),
        "R2_short":    float(rs.rsquared),
        "beta_long":   float(rl.params[cy_var]),
        "R2_long":     float(rl.rsquared),
        "se_long":     float(rl.std_errors[cy_var]),
        "p_long":      float(rl.pvalues[cy_var]),
    }


def oster_bound(beta_short, R2_short, beta_long, R2_long,
                R2_max_mult: float = 1.3, delta: float = 1.0) -> dict:
    """Возвращает β* при заданном δ и R²_max = mult · R²_long.

    β* = β_long − δ · (β_short − β_long) · (R²_max − R²_long) / (R²_long − R²_short)
    """
    R2_max = min(R2_max_mult * R2_long, 1.0)
    denom = (R2_long - R2_short)
    if abs(denom) < 1e-9:
        return {"beta_star": np.nan, "R2_max": R2_max,
                "delta_for_zero": np.nan}
    beta_star = beta_long - delta * (beta_short - beta_long) * (R2_max - R2_long) / denom
    # δ нужный, чтобы β_true = 0
    num_d = beta_long
    denom_d = (beta_short - beta_long) * (R2_max - R2_long) / denom
    if abs(denom_d) < 1e-9:
        delta_for_zero = np.nan
    else:
        delta_for_zero = num_d / denom_d
    return {"beta_star_delta1": beta_star, "R2_max": R2_max,
            "delta_for_zero": delta_for_zero}


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    df = attach_alt_cy(df)

    rows = []
    for cy in ["cy_exogenous", "contract_year", "cy_walk_back",
               "cy_canonical_extended"]:
        rec = fit_pair(df, cy)
        bound = oster_bound(rec["beta_short"], rec["R2_short"],
                             rec["beta_long"], rec["R2_long"])
        rec.update(bound)
        rows.append(rec)

    rdf = pd.DataFrame(rows)
    rdf.to_csv(OUT / "09_oster_sensitivity.csv", index=False)
    print(rdf.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
