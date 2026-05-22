"""Этап 6. Heterogeneous treatment effects.

Прогоняем M3c_canonical и Stiroh-аналог по подгруппам:
    - возраст: <25, 25-28, 29+
    - salary tier: min (<$2M real 2017), mid (2-10M), high (10-25M), max (>25M)
    - стаж: 1-2, 3-6, 7+
    - позиция: G (PG/SG), F (SF/PF), C
    - allstar в прошлом сезоне

Особое внимание: подгруппы, где cy_exogenous (или contract_year, или
cy_walk_back) даёт значимое β.

Outputs:
    output/h6_verification/06_heterogeneous_effects.csv
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

PROXIES = ["cy_exogenous", "contract_year", "cy_walk_back"]


def fit_m3c_subset(df: pd.DataFrame, cy_var: str, label: str, group: str) -> dict:
    """Прогон M3c на подмножестве. Возвращает β, SE, p, n."""
    d = df.copy()
    must = ["ln_salary", "ppg", "rpg", "apg", "age", "age_sq", "experience",
            "post_cba_2017", "post_covid", "allstar", "undrafted",
            "log_draft_pick", "pos_PG", "pos_SG", "pos_SF", "pos_PF",
            "mpg", "gp", "per", "ws", "bpm", "vorp", "usg_pct", "salary_next",
            cy_var]
    d = d.dropna(subset=must)
    d = d[~d["team_abbr"].isin(MULTI)]
    if d[cy_var].sum() < 5 or len(d) < 30:
        return {"group": group, "cy_var": cy_var, "subset": label,
                "n": len(d), "n_cy_1": int(d[cy_var].sum()),
                "beta_cy": np.nan, "se_cy": np.nan, "p_cy": np.nan,
                "MDE_cy": np.nan, "note": "too few obs"}
    d["dln_salary"] = np.log(d["salary_next"]) - d["ln_salary"]
    d[cy_var] = d[cy_var].astype(int)
    d = d.set_index(["player_id", "season"])
    X = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT + [cy_var]])
    try:
        res = PanelOLS(d["dln_salary"], X, time_effects=True,
                       drop_absorbed=True).fit(
            cov_type="clustered", cluster_entity=True
        )
        return {
            "group": group, "cy_var": cy_var, "subset": label,
            "n": int(res.nobs), "n_cy_1": int(d[cy_var].sum()),
            "beta_cy": float(res.params[cy_var]),
            "se_cy":   float(res.std_errors[cy_var]),
            "p_cy":    float(res.pvalues[cy_var]),
            "MDE_cy":  2.8 * float(res.std_errors[cy_var]),
            "note": "",
        }
    except Exception as e:
        return {"group": group, "cy_var": cy_var, "subset": label,
                "n": len(d), "n_cy_1": int(d[cy_var].sum()),
                "beta_cy": np.nan, "se_cy": np.nan, "p_cy": np.nan,
                "MDE_cy": np.nan, "note": f"error: {e}"}


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    df = attach_alt_cy(df)

    rows = []
    for cy in PROXIES:
        # Возраст
        for lbl, mask in [
            ("age<25", df["age"] < 25),
            ("age 25-28", (df["age"] >= 25) & (df["age"] <= 28)),
            ("age>=29", df["age"] >= 29),
        ]:
            rows.append(fit_m3c_subset(df[mask], cy, lbl, "age"))

        # Salary tier (real-deflated на год CBA-2017)
        cap_2017 = 99.1e6  # from config CAP
        df["_cap_share"] = df["salary_usd"] / df["cap_t"]
        df["_salary_real"] = df["_cap_share"] * cap_2017
        for lbl, mask in [
            ("min (<$2M real)", df["_salary_real"] < 2e6),
            ("mid ($2-10M)",    (df["_salary_real"] >= 2e6) & (df["_salary_real"] < 10e6)),
            ("high ($10-25M)",  (df["_salary_real"] >= 10e6) & (df["_salary_real"] < 25e6)),
            ("max ($25M+)",      df["_salary_real"] >= 25e6),
        ]:
            rows.append(fit_m3c_subset(df[mask], cy, lbl, "salary_tier"))

        # Стаж
        for lbl, mask in [
            ("exp 1-2", df["experience"] <= 2),
            ("exp 3-6", (df["experience"] >= 3) & (df["experience"] <= 6)),
            ("exp 7+",  df["experience"] >= 7),
        ]:
            rows.append(fit_m3c_subset(df[mask], cy, lbl, "experience"))

        # Position
        for lbl, mask in [
            ("guards (PG+SG)", (df["pos_PG"] == 1) | (df["pos_SG"] == 1)),
            ("forwards (SF+PF)", (df["pos_SF"] == 1) | (df["pos_PF"] == 1)),
            ("centers (C)", (df["pos_PG"] == 0) & (df["pos_SG"] == 0)
                           & (df["pos_SF"] == 0) & (df["pos_PF"] == 0)),
        ]:
            rows.append(fit_m3c_subset(df[mask], cy, lbl, "position"))

        # Allstar previous (allstar в текущем сезоне как прокси)
        for lbl, mask in [
            ("allstar=1", df["allstar"] == 1),
            ("allstar=0", df["allstar"] == 0),
        ]:
            rows.append(fit_m3c_subset(df[mask], cy, lbl, "allstar_status"))

    rdf = pd.DataFrame(rows)
    rdf.to_csv(OUT / "06_heterogeneous_effects.csv", index=False)
    # Display compactly
    print(rdf[["cy_var", "group", "subset", "n", "n_cy_1",
               "beta_cy", "se_cy", "p_cy", "MDE_cy"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
