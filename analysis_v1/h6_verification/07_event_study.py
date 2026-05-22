"""Этап 7. Mover analysis + event-study вокруг cy_exogenous.

Внутри игроков с хотя бы одним cy_exogenous=1: смотрим среднюю ΔlnSalary
по τ = season − cy_year, τ ∈ {-3,...,+3}. Аналогично для cy_walk_back.

Спецификация event-study:
    ln_salary_it = α_i + λ_t + Σ_{τ≠-1} β_τ · 1{event_offset_it = τ}
                   + Stats + ε

Outputs:
    output/h6_verification/07_event_study_around_cy.csv
    output/h6_verification/07_event_study_around_cy.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.config import COMBINED_STATS  # noqa: E402
from analysis_v1.h6_verification.alt_cy_helper import attach_alt_cy  # noqa: E402

OUT = ROOT / "output" / "h6_verification"
OUT.mkdir(parents=True, exist_ok=True)
MULTI = {"2TM", "3TM", "4TM", "TOT"}


def build_event_panel(df: pd.DataFrame, cy_col: str) -> pd.DataFrame:
    """Для каждого player_id определяем season первого cy_col=1; считаем offset."""
    d = df.copy()
    d = d[~d["team_abbr"].isin(MULTI)]
    d = d.dropna(subset=[cy_col])
    d = d.sort_values(["player_id", "season"])

    cy_seasons = (d[d[cy_col] == 1]
                  .groupby("player_id")["season"].min()
                  .rename("cy_first_season"))
    d = d.merge(cy_seasons, on="player_id", how="left")
    d = d.dropna(subset=["cy_first_season"])
    d["event_offset"] = d["season"] - d["cy_first_season"]

    # Ограничиваем |τ| ≤ 3, остальное в "out-of-window"
    d = d[d["event_offset"].between(-3, 3)].copy()
    d["event_offset"] = d["event_offset"].astype(int)
    return d


def fit_event_study(d: pd.DataFrame) -> pd.DataFrame:
    """ln_salary ~ Σ_τ≠-1 β_τ · 1{offset=τ} + stats + age + age² + experience + player FE + season FE."""
    d = d.dropna(subset=["ln_salary"] + COMBINED_STATS + ["age", "age_sq", "experience"])
    d = d.copy()
    offsets = sorted(d["event_offset"].unique().tolist())
    base = -1
    if base not in offsets:
        # Re-base to closest one
        base = offsets[0]
    for o in offsets:
        if o == base:
            continue
        d[f"E_{o:+d}"] = (d["event_offset"] == o).astype(int)
    event_cols = [c for c in d.columns if c.startswith("E_")]

    d = d.set_index(["player_id", "season"])
    X = d[event_cols + COMBINED_STATS + ["age", "age_sq", "experience"]]
    res = PanelOLS(d["ln_salary"], X, entity_effects=True, time_effects=True,
                    drop_absorbed=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    rows = [{"event_offset": base, "beta": 0.0, "se": 0.0, "p": np.nan,
             "ci_lo": 0.0, "ci_hi": 0.0, "ref": True}]
    for c in event_cols:
        tau = int(c.split("_")[1])
        b = float(res.params.get(c, np.nan))
        s = float(res.std_errors.get(c, np.nan))
        p = float(res.pvalues.get(c, np.nan))
        rows.append({"event_offset": tau, "beta": b, "se": s, "p": p,
                     "ci_lo": b - 1.96 * s, "ci_hi": b + 1.96 * s, "ref": False})
    return pd.DataFrame(rows).sort_values("event_offset")


def descriptive_dln(d: pd.DataFrame) -> pd.DataFrame:
    """Mean Δln_salary по offset."""
    sub = d.dropna(subset=["salary_next", "salary_usd"]).copy()
    sub["dln_salary"] = np.log(sub["salary_next"]) - np.log(sub["salary_usd"])
    g = sub.groupby("event_offset")["dln_salary"].agg(["count", "mean", "median", "std"])
    return g.reset_index()


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    df = attach_alt_cy(df)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    out_rows = []
    for ax, cy in zip(axes, ["cy_exogenous", "cy_walk_back"]):
        d = build_event_panel(df, cy)
        es = fit_event_study(d)
        desc = descriptive_dln(d)
        es["cy_var"] = cy
        desc["cy_var"] = cy
        out_rows.append(es)
        out_rows.append(desc.rename(columns={"count": "n_descriptive",
                                              "mean": "dln_mean",
                                              "median": "dln_median",
                                              "std": "dln_sd"}))

        ax.errorbar(es["event_offset"], es["beta"],
                    yerr=1.96 * es["se"], fmt="o-", capsize=4, color="steelblue",
                    label=f"β (95% CI)")
        ax.axhline(0, color="gray", lw=0.6)
        ax.axvline(0, color="red", lw=0.8, linestyle="--",
                   label="event year (τ=0)")
        ax.set_xlabel("event offset τ (season − first cy=1 season)")
        ax.set_ylabel("β_τ on ln_salary")
        ax.set_title(f"Event-study вокруг {cy}=1")
        ax.legend()

    plt.tight_layout()
    plt.savefig(OUT / "07_event_study_around_cy.png", dpi=140)
    plt.close()

    res = pd.concat(out_rows, ignore_index=True)
    res.to_csv(OUT / "07_event_study_around_cy.csv", index=False)
    print(res[res["event_offset"].notna()].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
