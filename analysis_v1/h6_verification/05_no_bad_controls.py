"""Этап 5. M3c_canonical без bad controls + альтернативные DV.

Базовая претензия Линии 5: в M3c_canonical V1 на правой стороне ppg/rpg/apg/
per/ws/vorp/usg — это **современная** производительность. Если по Stiroh-
гипотезе ContractYear → ↑performance → ↑salary, то контролировать на
performance — bad control.

Спецификации:
    (а) Полная (V1 baseline): Δlog_salary ~ stats + structural + cy
    (б) Без stats:            Δlog_salary ~ structural + cy
    (в) Минимальная:          Δlog_salary ~ age + age² + experience + pos + year FE + cy
    (г) DV = cap-share Δ:     Δ(salary/cap)~ stats + structural + cy
    (д) DV = log ratio:       log(salary_{t+1}/salary_t) уже = Δln_salary (то же)
    (е) DV = nominal:         salary_{t+1}/salary_t - 1

Каждое — для cy_exogenous и для contract_year и для cy_walk_back.

Outputs:
    output/h6_verification/05_m3c_no_bad_controls.csv
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

STRUCT = COMMON_NO_STRUCT  # age, age_sq, experience, allstar, undrafted, log_draft_pick, pos_*
MINIMAL = ["age", "age_sq", "experience", "pos_PG", "pos_SG", "pos_SF", "pos_PF"]


def fit_m3c_variant(df: pd.DataFrame, cy_var: str, dv: str, controls: list[str],
                    label: str) -> dict:
    d = df[~df["team_abbr"].isin(MULTI)].copy()
    need = ["ln_salary", "salary_usd", "salary_next", "salary_cap_share_t",
            "salary_cap_share_next", cy_var] + controls
    d = d.dropna(subset=need)
    d[cy_var] = d[cy_var].astype(int)

    if dv == "dln_salary":
        d["_y"] = np.log(d["salary_next"]) - np.log(d["salary_usd"])
    elif dv == "dln_cap_share":
        d["_y"] = np.log(d["salary_cap_share_next"]) - np.log(d["salary_cap_share_t"])
    elif dv == "ratio_minus_1":
        d["_y"] = d["salary_next"] / d["salary_usd"] - 1.0
    else:
        raise ValueError(dv)

    d = d.set_index(["player_id", "season"])
    X = sm.add_constant(d[controls + [cy_var]])
    res = PanelOLS(d["_y"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    return {
        "spec":      label,
        "cy_var":    cy_var,
        "dv":        dv,
        "controls":  ",".join(controls),
        "n":         int(res.nobs),
        "n_cy_1":    int(d[cy_var].sum()),
        "beta_cy":   float(res.params[cy_var]),
        "se_cy":     float(res.std_errors[cy_var]),
        "p_cy":      float(res.pvalues[cy_var]),
        "MDE_cy":    2.8 * float(res.std_errors[cy_var]),
        "r2":        float(res.rsquared),
    }


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    df = attach_alt_cy(df)

    rows = []
    for cy in ["cy_exogenous", "contract_year", "cy_walk_back"]:
        # (а) полная V1 — для контроля воспроизводимости
        rows.append(fit_m3c_variant(
            df, cy, "dln_salary", COMBINED_STATS + STRUCT,
            label="(а) full V1: dln_salary ~ stats + struct + cy"))
        # (б) без stats
        rows.append(fit_m3c_variant(
            df, cy, "dln_salary", STRUCT,
            label="(б) no stats: dln_salary ~ struct + cy"))
        # (в) минимальная (без allstar/undrafted/draft_pick)
        rows.append(fit_m3c_variant(
            df, cy, "dln_salary", MINIMAL,
            label="(в) minimal: dln_salary ~ age+pos+exp + cy"))
        # (г) cap-share DV
        rows.append(fit_m3c_variant(
            df, cy, "dln_cap_share", COMBINED_STATS + STRUCT,
            label="(г) cap-share DV: dln(salary/cap) ~ stats + struct + cy"))
        rows.append(fit_m3c_variant(
            df, cy, "dln_cap_share", STRUCT,
            label="(г') cap-share DV, no stats"))
        # (е) nominal ratio
        rows.append(fit_m3c_variant(
            df, cy, "ratio_minus_1", STRUCT,
            label="(е) ratio: salary_next/salary - 1 ~ struct + cy"))

    rdf = pd.DataFrame(rows)
    rdf.to_csv(OUT / "05_m3c_no_bad_controls.csv", index=False)
    print(rdf[["spec", "cy_var", "n", "beta_cy", "se_cy", "p_cy", "MDE_cy"]
              ].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
