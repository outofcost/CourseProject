"""Step 2: build contract_year using heuristic A+B+C.

A — real (cap-deflated) salary change > 25% between t and t+1.
B — team change between t and t+1 (free-agency proxy).
C — rookie-scale endpoint: round-1 picks with experience == 3,
    round-2 picks with experience == 1.

contract_year = max(A, B, C). NaN for last-panel season (2024) and for
multi-team rows (2TM/3TM/4TM) where the signals are not well-defined.
"""
from __future__ import annotations

import pandas as pd

from analysis.config import CAP, DATA_CLEAN


def run(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 72)
    print("STEP 2: contract_year heuristic A+B+C")
    print("=" * 72)

    df = df.sort_values(["player_id", "season"]).reset_index(drop=True)
    grp = df.groupby("player_id", sort=False)
    df["salary_next"] = grp["salary_usd"].shift(-1)
    df["team_next"] = grp["team_abbr"].shift(-1)
    df["season_next"] = grp["season"].shift(-1)

    df["cap_t"] = df["season"].map(CAP)
    df["cap_next"] = (df["season"] + 1).map(CAP)
    df["salary_cap_share_t"] = df["salary_usd"] / df["cap_t"]
    df["salary_cap_share_next"] = df["salary_next"] / df["cap_next"]
    df["real_salary_change"] = (
        df["salary_cap_share_next"] / df["salary_cap_share_t"] - 1.0
    )

    # A: salary jump
    A_thresh = 0.25
    df["cy_A"] = (df["real_salary_change"].abs() > A_thresh).astype("Int64")
    df.loc[df["salary_next"].isna(), "cy_A"] = pd.NA

    # B: team change (exclude multi-team current row — already ambiguous)
    df["team_changed"] = (df["team_abbr"] != df["team_next"]).astype("Int64")
    df.loc[df["team_next"].isna(), "team_changed"] = pd.NA
    multi_team_t = df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])
    df.loc[multi_team_t, "team_changed"] = pd.NA
    df["cy_B"] = df["team_changed"]

    # C: rookie scale endpoint
    df["cy_C"] = 0
    is_r1 = (df["draft_round"] == 1) & (df["experience"] == 3)
    is_r2 = (df["draft_round"] == 2) & (df["experience"] == 1)
    df.loc[is_r1 | is_r2, "cy_C"] = 1
    df["cy_C"] = df["cy_C"].astype("Int64")

    # combined
    cy = ((df["cy_A"].fillna(0) == 1)
          | (df["cy_B"].fillna(0) == 1)
          | (df["cy_C"].fillna(0) == 1)).astype("Int64")
    all_missing = (df["cy_A"].isna() & df["cy_B"].isna()
                   & (df["cy_C"].fillna(0) == 0))
    cy[all_missing] = pd.NA
    cy[multi_team_t] = pd.NA
    df["contract_year"] = cy

    print("\ncontract_year distribution:")
    print(df["contract_year"].value_counts(dropna=False).to_string())
    print("\nBy season:")
    print(df.groupby("season")["contract_year"]
          .agg(["count", lambda s: (s == 1).sum()])
          .rename(columns={"<lambda_0>": "n_contract_year"})
          .to_string())
    print("\nBy detection rule (non-mutually-exclusive):")
    print(f"  cy_A (salary jump): {(df['cy_A']==1).sum()}")
    print(f"  cy_B (team change): {(df['cy_B']==1).sum()}")
    print(f"  cy_C (rookie scale): {(df['cy_C']==1).sum()}")

    diag_path = DATA_CLEAN / "contract_year_diagnostics.csv"
    df[["player_id", "player_name", "season", "team_abbr", "salary_usd",
        "salary_next", "team_next", "real_salary_change", "draft_round",
        "experience", "cy_A", "cy_B", "cy_C", "contract_year"]].to_csv(
        diag_path, index=False
    )
    print(f"\nWrote {diag_path}")

    df.to_csv(DATA_CLEAN / "data_analysis.csv", index=False)
    return df
