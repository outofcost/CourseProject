"""Step 1: data preparation — tax JOIN, NaN handling, position normalization."""
from __future__ import annotations

import numpy as np
import pandas as pd

from analysis.config import DATA_CLEAN, DATA_LOOKUPS, TEAM_ABBR_FIX


def run() -> pd.DataFrame:
    print("\n" + "=" * 72)
    print("STEP 1: data prep — tax JOIN, NaN handling, position normalization")
    print("=" * 72)

    df = pd.read_csv(DATA_CLEAN / "data_merged.csv")
    print(f"Loaded data_merged.csv: {len(df)} rows × {df.shape[1]} cols")

    df["team_abbr_lookup"] = df["team_abbr"].replace(TEAM_ABBR_FIX)

    # state_tax wide → long, JOIN
    tax = pd.read_csv(DATA_LOOKUPS / "state_tax.csv")
    year_cols = [c for c in tax.columns if c.isdigit()]
    tax_long = tax.melt(
        id_vars=["team_abbr", "no_income_tax"],
        value_vars=year_cols,
        var_name="season",
        value_name="state_tax_rate",
    )
    tax_long["season"] = tax_long["season"].astype(int)
    tax_long["state_tax_rate"] = (
        tax_long["state_tax_rate"].str.rstrip("%").astype(float) / 100.0
    )

    df = df.merge(
        tax_long,
        left_on=["team_abbr_lookup", "season"],
        right_on=["team_abbr", "season"],
        how="left",
        suffixes=("", "_drop"),
    )
    df = df.drop(columns=[c for c in df.columns if c.endswith("_drop")])

    multi_team = df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])
    print(f"Multi-team rows (2TM/3TM/4TM): {multi_team.sum()} "
          f"({multi_team.mean()*100:.1f}%) — tax = NaN by design")
    print(f"Single-team rows with tax matched: "
          f"{df.loc[~multi_team, 'state_tax_rate'].notna().sum()} / "
          f"{(~multi_team).sum()}")

    # experience NaN for undrafted → 0
    n_exp_nan = df["experience"].isna().sum()
    df["experience"] = df["experience"].fillna(0)
    print(f"experience NaN filled with 0: {n_exp_nan} rows (all undrafted)")

    # shooting % NaN (no attempts) → 0
    for col in ["fg3_pct", "fg2_pct", "ft_pct", "fg_pct", "efg_pct", "ts_pct"]:
        if col in df.columns:
            n_nan = df[col].isna().sum()
            if n_nan > 0:
                df[col] = df[col].fillna(0)
                print(f"{col} NaN filled with 0: {n_nan} rows")
    df["no_3pt_attempts"] = (
        df.get("fg3a", pd.Series(0, index=df.index)) == 0
    ).astype(int)

    # position: take main role only (e.g. "SF-PF" → "SF"), then dummies (C ref)
    df["position_main"] = df["position"].astype(str).str.split("-").str[0]
    valid_pos = {"PG", "SG", "SF", "PF", "C"}
    df["position_main"] = df["position_main"].where(
        df["position_main"].isin(valid_pos), "G"
    )
    for p in ["PG", "SG", "SF", "PF"]:
        df[f"pos_{p}"] = (df["position_main"] == p).astype(int)
    print(f"Position distribution:\n{df['position_main'].value_counts().to_string()}")

    # draft_pick: impute 61 for undrafted, then log
    df["draft_pick_imp"] = df["draft_pick"].fillna(61)
    df["log_draft_pick"] = np.log(df["draft_pick_imp"])

    out = DATA_CLEAN / "data_analysis.csv"
    df.to_csv(out, index=False)
    print(f"\nWrote {out} ({len(df)} rows × {df.shape[1]} cols)")
    return df
