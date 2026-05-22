"""Step 2 (V1): contract_year heuristic — переделан с учётом A1, A4, C5.

Мотивация (см. revisions_v1/PROBLEMS.md, §A1/§A4):
    V0 имела циркулярность: `cy_A` определялась через |Δsalary| > 25%,
    и затем регрессия Δlog_salary ~ contract_year в M3c фактически
    регрессировала размер изменения зарплаты на индикатор большого
    изменения зарплаты. Кроме того, V0 cy_A засчитывала и понижения
    зарплаты (324 из 1005 cy_A=1) как «contract year», смешивая
    pay raises и pay cuts.

В V1 разделяем 6 сигналов:

    cy_A_up         — real_salary_change > +0.25
                      (повышение реальной cap-share более 25%).
                      Эндогенный, циркулярный — для контраста с
                      cy_exogenous в M3.
    cy_A_down       — real_salary_change < -0.25
                      (понижение более 25%). Никогда не учитывается
                      в contract_year — это не контрактный год, это
                      pay cut.
    cy_B_offseason  — team_abbr_t ≠ team_abbr_{t+1}, и ни в году t,
                      ни в году t+1 нет mid-season trade. Сигнал
                      free-agency / sign-and-trade в межсезонье.
                      Экзогенный (не использует s_{t+1}).
    cy_B_trade      — team_abbr_t ∈ {2TM, 3TM, 4TM, TOT}: игрок был
                      обменян в середине сезона t. Информативный, но
                      НЕ канонический сигнал нового контракта.
    cy_C            — rookie-scale endpoint: round-1 picks с
                      experience == 3, round-2 picks с experience == 1.
                      Экзогенный (определяется правилами CBA).

Композитные:

    contract_year   = max(cy_A_up, cy_B_offseason, cy_C)
                      Используется как баланс между статистической
                      силой и эндогенностью. cy_A_up даёт долю; но
                      его эндогенность нужно держать в уме при
                      интерпретации.

    cy_exogenous    = max(cy_B_offseason, cy_C)
                      Сигнал контрактного года, НЕ использующий
                      будущую зарплату. Регрессия Δlog_salary на
                      cy_exogenous — настоящий canonical test
                      гипотезы H6 (см. M3 V1).

Multi-team строки (team_abbr ∈ {2TM, 3TM, 4TM, TOT}) — cy_A_up/down
и cy_B_offseason для них NA; cy_B_trade = 1; contract_year/cy_exogenous
ставятся NA (ambiguous attribution: salary в multi-team — сумма по
командам, переход некорректно определяется).

Последний сезон панели (salary_next NaN) — cy_A_up/down/cy_B_offseason
NA; cy_C может быть определён; итоговые contract_year/cy_exogenous —
NA если ни один компонент не = 1.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import CAP, DATA_CLEAN  # noqa: E402

MULTI_TEAM = {"2TM", "3TM", "4TM", "TOT"}
A_THRESH = 0.25


def run(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 72)
    print("STEP 2 (V1): contract_year heuristic — A_up/A_down/B_off/B_trade/C")
    print("=" * 72)

    df = df.sort_values(["player_id", "season"]).reset_index(drop=True)

    # Drop V0 cy_* columns if present (we rebuild from scratch).
    drop_cols = [
        "salary_next", "team_next", "season_next",
        "cap_t", "cap_next", "salary_cap_share_t", "salary_cap_share_next",
        "real_salary_change",
        "cy_A", "cy_B", "cy_C", "team_changed", "contract_year",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

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

    multi_team_t = df["team_abbr"].isin(MULTI_TEAM)
    multi_team_next = df["team_next"].isin(MULTI_TEAM)

    # ── cy_A_up / cy_A_down (signed; disjoint by construction) ───────────
    df["cy_A_up"] = (df["real_salary_change"] > A_THRESH).astype("Int64")
    df["cy_A_down"] = (df["real_salary_change"] < -A_THRESH).astype("Int64")
    na_a = df["salary_next"].isna() | df["salary_usd"].isna()
    df.loc[na_a, "cy_A_up"] = pd.NA
    df.loc[na_a, "cy_A_down"] = pd.NA
    # Multi-team t: salary attribution к команде некорректна → NA.
    df.loc[multi_team_t, "cy_A_up"] = pd.NA
    df.loc[multi_team_t, "cy_A_down"] = pd.NA

    # ── cy_B_offseason / cy_B_trade ──────────────────────────────────────
    # offseason: team changed AND no mid-season move in either year.
    df["cy_B_offseason"] = (
        (~multi_team_t)
        & (~multi_team_next)
        & (df["team_next"].notna())
        & (df["team_abbr"] != df["team_next"])
    ).astype("Int64")
    df.loc[df["team_next"].isna(), "cy_B_offseason"] = pd.NA
    df.loc[multi_team_t, "cy_B_offseason"] = pd.NA
    df.loc[multi_team_next, "cy_B_offseason"] = pd.NA

    # trade: mid-season movement в году t.
    df["cy_B_trade"] = multi_team_t.astype("Int64")

    # ── cy_C ─────────────────────────────────────────────────────────────
    df["cy_C"] = 0
    is_r1 = (df["draft_round"] == 1) & (df["experience"] == 3)
    is_r2 = (df["draft_round"] == 2) & (df["experience"] == 1)
    df.loc[is_r1 | is_r2, "cy_C"] = 1
    df["cy_C"] = df["cy_C"].astype("Int64")

    # ── Composite signals ────────────────────────────────────────────────
    def _compose(components: list[str]) -> pd.Series:
        any_one = pd.Series(False, index=df.index)
        for c in components:
            any_one = any_one | (df[c].fillna(0) == 1)
        out = any_one.astype("Int64")
        # NA только если все компоненты NA И ни один не = 1.
        all_na_or_zero = pd.Series(True, index=df.index)
        for c in components:
            all_na_or_zero = all_na_or_zero & (df[c].isna() | (df[c] == 0))
        any_na = pd.Series(False, index=df.index)
        for c in components:
            any_na = any_na | df[c].isna()
        # Если все компоненты = 0, оставляем 0.
        # Если есть хотя бы одна 1 — оставляем 1.
        # Если все = NA или (NA + 0), но ни одна = 1 — ставим NA.
        out[all_na_or_zero & any_na] = pd.NA
        return out

    df["contract_year"] = _compose(["cy_A_up", "cy_B_offseason", "cy_C"])
    df["cy_exogenous"] = _compose(["cy_B_offseason", "cy_C"])

    # Multi-team t — итог ставим NA (несмотря на cy_C, attribution неоднозначна).
    df.loc[multi_team_t, "contract_year"] = pd.NA
    df.loc[multi_team_t, "cy_exogenous"] = pd.NA

    # ── Reporting ────────────────────────────────────────────────────────
    print("\nКомпоненты (sum == 1):")
    for c in ["cy_A_up", "cy_A_down", "cy_B_offseason", "cy_B_trade", "cy_C"]:
        n1 = (df[c] == 1).sum()
        nna = df[c].isna().sum()
        print(f"  {c:18s}: 1 -> {n1:5d}, NA -> {nna:5d}")

    print("\ncontract_year distribution:")
    print(df["contract_year"].value_counts(dropna=False).to_string())
    print("\ncy_exogenous distribution:")
    print(df["cy_exogenous"].value_counts(dropna=False).to_string())

    print("\nBy season (contract_year=1, cy_exogenous=1):")
    by_season = df.groupby("season").agg(
        n=("contract_year", "count"),
        n_cy=("contract_year", lambda s: (s == 1).sum()),
        n_cyx=("cy_exogenous", lambda s: (s == 1).sum()),
    )
    print(by_season.to_string())

    # Доли (excluding NA)
    cy_share = (df["contract_year"] == 1).sum() / df["contract_year"].notna().sum()
    cyx_share = (df["cy_exogenous"] == 1).sum() / df["cy_exogenous"].notna().sum()
    print(f"\ncontract_year=1 доля (non-NA): {cy_share:.3f}")
    print(f"cy_exogenous=1 доля (non-NA):  {cyx_share:.3f}")

    # Diagnostic dump
    diag_cols = [
        "player_id", "player_name", "season", "team_abbr", "team_next",
        "salary_usd", "salary_next", "real_salary_change",
        "draft_round", "experience",
        "cy_A_up", "cy_A_down", "cy_B_offseason", "cy_B_trade", "cy_C",
        "contract_year", "cy_exogenous",
    ]
    diag_path = DATA_CLEAN / "contract_year_v1_diagnostics.csv"
    df[diag_cols].to_csv(diag_path, index=False)
    print(f"\nWrote {diag_path}")

    out_path = DATA_CLEAN / "data_analysis_v1.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}  ({len(df)} rows, {df.shape[1]} cols)")
    return df


def _verify(df: pd.DataFrame) -> None:
    import numpy as np

    print("\n" + "=" * 72)
    print("VERIFICATION (план §1.1)")
    print("=" * 72)

    # 1. cy_A_up и cy_A_down disjoint.
    both = ((df["cy_A_up"] == 1) & (df["cy_A_down"] == 1)).sum()
    print(f"1. cy_A_up & cy_A_down overlap: {both}  (ожидаем 0)")
    assert both == 0, "cy_A_up и cy_A_down не disjoint"

    # 2. corr(cy_exogenous, dlog_salary) < 0.30 по модулю.
    sub = df.dropna(subset=["salary_next", "cy_exogenous", "salary_usd"]).copy()
    sub = sub[sub["salary_usd"] > 0]
    sub["dlog"] = np.log(sub["salary_next"] / sub["salary_usd"])
    corr = np.corrcoef(sub["cy_exogenous"].astype(float), sub["dlog"])[0, 1]
    print(f"2. corr(cy_exogenous, Δlog_salary) = {corr:.4f}  (|·| < 0.30)")
    assert abs(corr) < 0.30, f"cy_exogenous всё ещё подозрителен: corr={corr:.3f}"

    # Для контраста — то же по старому cy_A_up (циркулярный сигнал).
    corr_up = np.corrcoef(sub["cy_A_up"].astype(float), sub["dlog"])[0, 1]
    print(f"   corr(cy_A_up,      Δlog_salary) = {corr_up:.4f}  (ожидаемо высокая — циркулярность)")

    # 3. Распределение.
    print(f"\n3. contract_year value_counts:")
    print(df["contract_year"].value_counts(dropna=False).to_string())

    # 4. cy_C invariant: те же rows, что и в V0 (фикс A2 не повлияет на drafted).
    print(f"\n4. cy_C=1 count: {(df['cy_C']==1).sum()}")

    print("\n[OK] §1.1 verification passed.")


if __name__ == "__main__":
    # Предпочтительный вход — output prep_v1; fallback на V0 data_analysis.csv.
    src_v1 = DATA_CLEAN / "data_analysis_v1.csv"
    src_v0 = DATA_CLEAN / "data_analysis.csv"
    src = src_v1 if src_v1.exists() else src_v0
    print(f"Reading {src}")
    df = pd.read_csv(src)
    print(f"  loaded: {len(df)} rows, {df.shape[1]} cols")

    df = run(df)
    _verify(df)
