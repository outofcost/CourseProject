"""Step 1 (V1): data prep — фиксы A2 (experience), A3 (Toronto tax), C13 (shooting % flags).

Изменения относительно V0 (analysis/prep.py):

    §1.2 (A2) — experience для undrafted:
        В V0:   df["experience"] = df["experience"].fillna(0)
        Эффект: все 612 undrafted получали exp=0 (вкл. ветеранов
        типа VanVleet с 8 сезонами), что делало undrafted ≡
        (experience=0) и засоряло R3.
        В V1:   drafted сохраняют experience = season − draft_year;
                undrafted получают experience = cumcount + 1 по
                player_id, отсортированному по season.

    §1.2 (доп.) — experience_career_total:
        Сквозной счётчик «карьерных сезонов в выборке» для каждого
        игрока. Используется для альтернативной спецификации M1.

    §1.3 (A3) — Toronto state_tax:
        TOR теперь имеет state_tax_rate в state_tax.csv (49.53% для
        2016, 53.53% начиная с 2017). Добавляем флаг is_canada=1
        для TOR (для робастности — отделить эффект «налог высокий»
        от эффекта «лига за рубежом»).

    §1.5 (C13) — NaN-флаги для shooting %:
        В V0: fg3_pct.fillna(0) → потеря информации «бросал ли вообще».
        В V1: для каждой % колонки сначала добавляем
              no_<col>_attempts = isna(col).astype(int),
              затем fillna(0).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import DATA_CLEAN, DATA_LOOKUPS, TEAM_ABBR_FIX  # noqa: E402

PCT_COLS = ["fg3_pct", "fg2_pct", "ft_pct", "fg_pct", "efg_pct", "ts_pct"]


def run() -> pd.DataFrame:
    print("\n" + "=" * 72)
    print("STEP 1 (V1): prep — A2 experience, A3 Toronto, C13 shooting flags")
    print("=" * 72)

    df = pd.read_csv(DATA_CLEAN / "data_merged.csv")
    print(f"Loaded data_merged.csv: {len(df)} rows × {df.shape[1]} cols")

    df["team_abbr_lookup"] = df["team_abbr"].replace(TEAM_ABBR_FIX)

    # ── state_tax (теперь с Toronto) ────────────────────────────────────
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
        tax_long["state_tax_rate"].astype(str).str.rstrip("%").astype(float) / 100.0
    )

    df = df.merge(
        tax_long,
        left_on=["team_abbr_lookup", "season"],
        right_on=["team_abbr", "season"],
        how="left",
        suffixes=("", "_drop"),
    )
    df = df.drop(columns=[c for c in df.columns if c.endswith("_drop")])

    df["is_canada"] = (df["team_abbr"] == "TOR").astype(int)

    multi_team = df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])
    print(f"Multi-team rows: {multi_team.sum()} ({multi_team.mean()*100:.1f}%)")
    print(f"Single-team rows with tax matched: "
          f"{df.loc[~multi_team, 'state_tax_rate'].notna().sum()} / "
          f"{(~multi_team).sum()}")
    tor_mask = df["team_abbr"] == "TOR"
    print(f"TOR rows: {tor_mask.sum()}, tax notna: "
          f"{df.loc[tor_mask, 'state_tax_rate'].notna().sum()}")

    # ── experience fix (A2) ─────────────────────────────────────────────
    n_exp_nan_before = df["experience"].isna().sum()
    df = df.sort_values(["player_id", "season"]).reset_index(drop=True)

    undrafted_mask = df["undrafted"] == 1
    # Для undrafted: cumcount + 1 (1-я NBA сезонная позиция = 1).
    cc = df[undrafted_mask].groupby("player_id").cumcount() + 1
    df.loc[undrafted_mask, "experience"] = cc.astype(float)

    n_exp_nan_after = df["experience"].isna().sum()
    print(f"experience NaN: {n_exp_nan_before} → {n_exp_nan_after}")

    # experience_career_total (для всех игроков — сквозной счётчик в выборке)
    df["experience_career_total"] = df.groupby("player_id").cumcount() + 1

    # ── shooting % flags + fillna (C13) ─────────────────────────────────
    for col in PCT_COLS:
        if col in df.columns:
            flag = f"no_{col.replace('_pct','')}_attempts"
            df[flag] = df[col].isna().astype(int)
            n_nan = df[col].isna().sum()
            if n_nan > 0:
                df[col] = df[col].fillna(0)
                print(f"{col} NaN flag set (n={n_nan}), filled with 0")
    # Совместимость со старым именем no_3pt_attempts:
    if "no_fg3_attempts" in df.columns:
        df["no_3pt_attempts"] = df["no_fg3_attempts"]

    # ── position normalization (как в V0) ────────────────────────────────
    df["position_main"] = df["position"].astype(str).str.split("-").str[0]
    valid_pos = {"PG", "SG", "SF", "PF", "C"}
    df["position_main"] = df["position_main"].where(
        df["position_main"].isin(valid_pos), "G"
    )
    for p in ["PG", "SG", "SF", "PF"]:
        df[f"pos_{p}"] = (df["position_main"] == p).astype(int)

    # draft_pick impute (как в V0)
    df["draft_pick_imp"] = df["draft_pick"].fillna(61)
    df["log_draft_pick"] = np.log(df["draft_pick_imp"])

    out = DATA_CLEAN / "data_analysis_v1.csv"
    df.to_csv(out, index=False)
    print(f"\nWrote {out} ({len(df)} rows × {df.shape[1]} cols)")
    return df


def _verify(df: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("VERIFICATION (план §1.2 + §1.3 + §1.5)")
    print("=" * 72)

    # 1. VanVleet experience 1..N (он 2017-2024, undrafted).
    vv = df[df["player_name"].str.contains("VanVleet", na=False)].sort_values("season")
    print(f"\n1. VanVleet seasons / experience:")
    print(vv[["player_name", "season", "team_abbr", "experience"]].to_string(index=False))
    vv_exp = vv["experience"].tolist()
    expected = list(range(1, len(vv) + 1))
    assert vv_exp == [float(x) for x in expected], (
        f"VanVleet experience mismatch: got {vv_exp}, expected {expected}"
    )

    # 2. exp=0 count < undrafted count (после фикса должно стать 0).
    exp0 = (df["experience"] == 0).sum()
    und = (df["undrafted"] == 1).sum()
    print(f"\n2. experience=0: {exp0}, undrafted=1: {und}")
    assert exp0 < und, f"experience fix не сработал: exp0={exp0}, und={und}"

    # 3. TOR имеет state_tax_rate, between 0.45 and 0.56.
    tor = df[df["team_abbr"] == "TOR"]
    print(f"\n3. TOR rows: {len(tor)}, tax notna: {tor['state_tax_rate'].notna().sum()}")
    print(tor.groupby("season")["state_tax_rate"].first().to_string())
    assert tor["state_tax_rate"].notna().all(), "TOR имеет NaN state_tax_rate"
    assert tor["state_tax_rate"].between(0.45, 0.56).all(), "TOR tax вне ожидаемого диапазона"

    # 4. is_canada
    assert (df["is_canada"] == (df["team_abbr"] == "TOR").astype(int)).all()

    # 5. Shooting % flags
    print(f"\n4. Shooting % flags:")
    for col in PCT_COLS:
        flag = f"no_{col.replace('_pct','')}_attempts"
        if flag in df.columns:
            print(f"  {flag}: sum = {df[flag].sum()}")

    print("\n[OK] §1.2 + §1.3 + §1.5 verification passed.")


if __name__ == "__main__":
    df = run()
    _verify(df)
