"""Descriptive statistics for the final dataset."""
from __future__ import annotations

import pandas as pd

from analysis.config import OUT_TABLES


def run(df: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("Descriptive statistics")
    print("=" * 72)
    cols = ["salary_usd", "ln_salary", "age", "experience",
            "ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
            "fg_pct", "fg3_pct", "ft_pct",
            "per", "ws", "bpm", "vorp", "usg_pct",
            "allstar", "undrafted", "post_cba_2017", "post_covid",
            "state_tax_rate", "no_income_tax", "contract_year"]
    cols = [c for c in cols if c in df.columns]
    desc = df[cols].describe().T[["count", "mean", "std", "min", "50%", "max"]]
    desc.columns = ["N", "Mean", "SD", "Min", "Median", "Max"]
    desc = desc.round(4)
    desc.to_csv(OUT_TABLES / "descriptive_stats.csv")
    print(desc.to_string())
    print(f"\n -> {OUT_TABLES / 'descriptive_stats.csv'}")
