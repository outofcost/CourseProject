"""Этап 4. Канонический Stiroh-тест: эффект contract year на ПРОИЗВОДИТЕЛЬНОСТЬ.

Гипотеза Stiroh (2007) — про производительность, не про Δsalary. Спецификация:

    Y_perf_it = α_i + λ_t + β·ContractYear_it + γ·Age + δ·Age² + ε_it

Two-way FE (player + season), cluster SE по player. Прогон по каждой мере
производительности и по двум прокси (composite и canonical exogenous).

Доп. спецификация: ContractYear × Age30+ (H3 in Stiroh).

Outputs:
    output/h6_verification/04_stiroh_performance_test.csv  (полная таблица)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "output" / "h6_verification"
OUT.mkdir(parents=True, exist_ok=True)

PERF_VARS = ["ppg", "rpg", "apg", "per", "ws", "vorp", "usg_pct", "ts_pct", "mpg"]
CY_PROXIES = ["contract_year", "cy_exogenous", "cy_walk_back",
              "cy_canonical_extended", "cy_age_based"]


def fit_perf_on_cy(df: pd.DataFrame, y_var: str, cy_var: str,
                   age_interaction: bool = False) -> dict:
    d = df[~df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])].copy()
    need = [y_var, cy_var, "age", "age_sq", "experience", "allstar"]
    d = d.dropna(subset=need)
    d[cy_var] = d[cy_var].astype(int)

    if age_interaction:
        d["age30plus"] = (d["age"] >= 30).astype(int)
        d["cy_x_age30"] = d[cy_var] * d["age30plus"]
    d = d.set_index(["player_id", "season"])
    if age_interaction:
        regs = ["experience", "allstar", cy_var, "age30plus", "cy_x_age30"]
    else:
        regs = ["experience", "allstar", cy_var]
    X = d[regs]
    y = d[y_var]
    try:
        res = PanelOLS(y, X, entity_effects=True, time_effects=True,
                       drop_absorbed=True).fit(
            cov_type="clustered", cluster_entity=True
        )
    except Exception as e:
        return {"y": y_var, "cy_var": cy_var, "age_interaction": age_interaction,
                "n": len(d), "n_cy_1": int(d[cy_var].sum()), "error": str(e)}

    out = {
        "y":            y_var,
        "cy_var":       cy_var,
        "age_interaction": age_interaction,
        "n":            int(res.nobs),
        "n_cy_1":       int(d[cy_var].sum()),
        "beta_cy":      float(res.params.get(cy_var, np.nan)),
        "se_cy":        float(res.std_errors.get(cy_var, np.nan)),
        "p_cy":         float(res.pvalues.get(cy_var, np.nan)),
        "MDE_cy":       2.8 * float(res.std_errors.get(cy_var, np.nan)),
    }
    if age_interaction:
        out["beta_cy_x_age30"] = float(res.params.get("cy_x_age30", np.nan))
        out["se_cy_x_age30"] = float(res.std_errors.get("cy_x_age30", np.nan))
        out["p_cy_x_age30"] = float(res.pvalues.get("cy_x_age30", np.nan))

    # In-sample mean of Y (for MDE-in-%-of-mean)
    out["mean_y"] = float(y.mean())
    out["beta_pct_of_mean"] = out["beta_cy"] / max(abs(out["mean_y"]), 1e-9)
    return out


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    # Подмешиваем альтернативные cy из Этапа 3
    from analysis_v1.h6_verification.alt_cy_helper import attach_alt_cy
    df = attach_alt_cy(df)
    rows = []
    for y in PERF_VARS:
        for cy in CY_PROXIES:
            rows.append(fit_perf_on_cy(df, y, cy, age_interaction=False))
            rows.append(fit_perf_on_cy(df, y, cy, age_interaction=True))

    rdf = pd.DataFrame(rows)
    rdf.to_csv(OUT / "04_stiroh_performance_test.csv", index=False)
    print(rdf.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
