"""Helpers shared across analysis modules."""
from __future__ import annotations

import pandas as pd

from analysis.config import OUT_TABLES


def prep_for_models(df: pd.DataFrame, restrict_single_team: bool) -> pd.DataFrame:
    """Filter to the estimation sample; drop NA in regressors."""
    d = df.copy()
    if restrict_single_team:
        d = d[~d["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])].copy()
    must_have = ["ln_salary", "ppg", "rpg", "apg", "age", "age_sq", "experience",
                 "post_cba_2017", "post_covid", "allstar", "undrafted",
                 "log_draft_pick", "pos_PG", "pos_SG", "pos_SF", "pos_PF",
                 "mpg", "gp", "per", "ws", "bpm", "vorp", "usg_pct"]
    return d.dropna(subset=must_have)


def panel_index(d: pd.DataFrame) -> pd.DataFrame:
    return d.set_index(["player_id", "season"])


def save_summary(res, name: str) -> None:
    path = OUT_TABLES / f"{name}.txt"
    path.write_text(str(res.summary), encoding="utf-8")


def combine_models(results: dict, fname: str) -> None:
    """Combine multiple regression results into a wide CSV table."""
    all_vars = []
    for r in results.values():
        for v in r.params.index:
            if v not in all_vars:
                all_vars.append(v)

    rows = []
    for v in all_vars:
        row = {"variable": v}
        for name, res in results.items():
            if v in res.params.index:
                c = res.params[v]
                s = res.std_errors[v]
                p = res.pvalues[v]
                stars = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else ""))
                row[name] = f"{c:.4f}{stars}\n({s:.4f})"
            else:
                row[name] = ""
        rows.append(row)

    stats = {"nobs": "N", "rsquared": "R²",
             "rsquared_within": "R² within", "rsquared_between": "R² between"}
    for stat_key, stat_label in stats.items():
        row = {"variable": stat_label}
        for name, res in results.items():
            try:
                val = getattr(res, stat_key)
                if isinstance(val, float):
                    row[name] = f"{val:.4f}" if abs(val) < 1e6 else f"{int(val)}"
                else:
                    row[name] = f"{int(val)}"
            except (AttributeError, KeyError):
                row[name] = ""
        rows.append(row)

    pd.DataFrame(rows).to_csv(OUT_TABLES / fname, index=False, encoding="utf-8")
    print(f"  -> {OUT_TABLES / fname}")
