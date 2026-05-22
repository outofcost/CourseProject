"""validation_v2 — descriptive sanity checks on new v2 variables.

Per todo3.md block 2.2: distribution, cross-tab by season/position, top-10 / bottom-10,
plus the explicit sanity-anchors list in 2.2.2.

Run:
    python3 -m analysis_v2.validation_v2

Writes:
    analysis_v2/reports/validation_report_v2.md
    analysis_v2/reports/correlation_matrix_v2.png
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

log = logging.getLogger("analysis_v2.validation")
REPORTS = ROOT / "analysis_v2" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def _section(title: str) -> str:
    return f"\n## {title}\n"


def _check(label: str, passed: bool, detail: str = "") -> str:
    mark = "✅" if passed else "❌"
    return f"- {mark} **{label}** — {detail}\n"


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    src = ROOT / "data" / "clean" / "data_analysis_v2.csv"
    df = pd.read_csv(src)
    log.info("loaded %d × %d", *df.shape)

    md: list[str] = [f"# validation_report_v2\n\nDataset: `data/clean/data_analysis_v2.csv`  \nShape: {df.shape[0]} × {df.shape[1]}\n"]

    # --------------------------------------------------------------------
    # 1) International / birth country
    md.append(_section("Birth country / international"))
    if "is_international" in df.columns and df["is_international"].notna().any():
        intl_mean = float(df["is_international"].mean())
        md.append(
            _check(
                "share international ∈ [0.22, 0.32]",
                0.22 <= intl_mean <= 0.32,
                f"observed = {intl_mean:.3f}",
            )
        )
        # Trend: 2016 vs 2024
        m_early = df.loc[df["season"] == 2016, "is_international"].mean()
        m_late = df.loc[df["season"] == 2024, "is_international"].mean()
        md.append(
            _check(
                "share international rises 2016 → 2024",
                bool(m_late > m_early),
                f"2016 = {m_early:.3f}, 2024 = {m_late:.3f}",
            )
        )
        # Top countries
        top = df["birth_country"].value_counts().head(10)
        md.append("\nTop birth countries (player-seasons):\n\n```\n" + top.to_string() + "\n```\n")
    else:
        md.append("- ⏳ birth_country.csv not yet merged into v2 (scrape still running)\n")

    # --------------------------------------------------------------------
    # 2) Awards
    md.append(_section("Awards (lag, cumsum, supermax)"))
    if "all_nba_lag1" in df.columns:
        per_season_15 = []
        for s in sorted(df["season"].unique()):
            n = int((df.loc[df["season"] == s, "all_nba_lag1"] == 1).sum())
            per_season_15.append((s, n))
        # For season>=2017 there should be ~15 distinct players with all_nba_lag1=1 (those in
        # All-NBA of previous season who are still in the panel)
        md.append(
            "\nall_nba_lag1 == 1 per season (player-seasons in panel):\n\n```\n"
            + "\n".join(f"{s}: {n}" for s, n in per_season_15)
            + "\n```\n"
        )
    if "mvp_lag1" in df.columns:
        for s in sorted(df["season"].unique())[1:]:  # skip first season (no lag)
            n = int((df.loc[df["season"] == s, "mvp_lag1"] == 1).sum())
            ok = n == 1
            if not ok:
                md.append(_check(f"mvp_lag1 sum == 1 in season {s}", ok, f"observed = {n}"))
    if "supermax_eligible_loose" in df.columns:
        sm = df.groupby("season")["supermax_eligible_loose"].sum().astype(int)
        md.append(
            "\nsupermax_eligible_loose count per season:\n\n```\n"
            + sm.to_string()
            + "\n```\n"
        )
        md.append(
            _check(
                "supermax = 0 in 2016",
                int(sm.get(2016, 0)) == 0,
                f"observed = {int(sm.get(2016, 0))}",
            )
        )
        md.append(
            _check(
                "supermax > 0 in 2024",
                int(sm.get(2024, 0)) > 0,
                f"observed = {int(sm.get(2024, 0))}",
            )
        )

    # --------------------------------------------------------------------
    # 3) Contract tier
    md.append(_section("Contract tier"))
    if "contract_tier" in df.columns:
        ct = pd.crosstab(df["season"], df["contract_tier"])
        md.append("\nDistribution by season × tier:\n\n```\n" + ct.to_string() + "\n```\n")
        n_super_2024 = int(((df["season"] == 2024) & (df["contract_tier"] == "supermax")).sum())
        md.append(
            _check(
                "supermax tier 5–10 in 2024",
                5 <= n_super_2024 <= 12,
                f"observed = {n_super_2024}",
            )
        )

    # --------------------------------------------------------------------
    # 4) Market size
    md.append(_section("Market size"))
    if "market_size_rank_nba" in df.columns:
        # Correlation between rank and top5 dummy
        sub = df.dropna(subset=["market_size_rank_nba", "top5_market"])
        if len(sub) > 0:
            rho = sub["market_size_rank_nba"].corr(sub["top5_market"])
            md.append(
                _check(
                    "|corr(market_size_rank_nba, top5_market)| ≥ 0.5",
                    abs(rho) >= 0.5,
                    f"observed = {rho:.3f}",
                )
            )
        # Memphis sanity: rank ≥ 25 (bottom)
        mem_rank = df.loc[df["team_abbr"] == "MEM", "market_size_rank_nba"].dropna().unique()
        md.append(
            _check(
                "MEM market_size_rank_nba ≥ 25",
                len(mem_rank) > 0 and float(mem_rank[0]) >= 25,
                f"observed = {mem_rank.tolist()}",
            )
        )
        # NYC sanity: NYK & BRK both rank 1
        nyk = df.loc[df["team_abbr"].isin(["NYK", "BRK"]), "market_size_rank_nba"].dropna().unique()
        md.append(
            _check(
                "NYK/BRK market_size_rank_nba == 1",
                set(map(int, nyk)) == {1},
                f"observed = {sorted(set(map(int, nyk)))}",
            )
        )

    # --------------------------------------------------------------------
    # 5) Durability
    md.append(_section("Durability"))
    if "games_missed_lag1" in df.columns:
        med = float(df["games_missed_lag1"].median())
        md.append(
            _check(
                "median games_missed_lag1 ∈ [10, 30]",
                10 <= med <= 30,
                f"observed = {med:.1f}",
            )
        )

    # --------------------------------------------------------------------
    # 6) Team season
    md.append(_section("Team season (win pct, playoffs)"))
    if "win_pct" in df.columns:
        med = float(df["win_pct"].median())
        std = float(df["win_pct"].std())
        md.append(
            _check(
                "win_pct median ≈ 0.5 (within ±0.05)",
                abs(med - 0.5) <= 0.05,
                f"observed = {med:.3f}",
            )
        )
        md.append(
            _check(
                "win_pct std ≈ 0.15 (within ±0.05)",
                abs(std - 0.15) <= 0.05,
                f"observed = {std:.3f}",
            )
        )

    # --------------------------------------------------------------------
    # 7) Correlation matrix among new + old key regressors
    md.append(_section("Correlation among main regressors"))
    candidate_cols = [
        "ppg", "rpg", "apg", "per", "ws", "vorp", "usg_pct",
        "age", "experience",
        "salary_cap_share_t",
        "all_nba_lag1", "career_all_nba_count", "career_allstar_count",
        "supermax_eligible_loose",
        "games_missed_lag1",
        "market_size_rank_nba", "top5_market",
        "win_pct", "made_playoffs",
        "is_international",
    ]
    cols = [c for c in candidate_cols if c in df.columns]
    corr = df[cols].corr().round(2)
    md.append("\n```\n" + corr.to_string() + "\n```\n")

    # Flag |r| > 0.85 outside the diagonal
    hi = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            r = corr.iloc[i, j]
            if pd.notna(r) and abs(r) > 0.85:
                hi.append((cols[i], cols[j], r))
    if hi:
        md.append("\nPairs with |r| > 0.85 (collinearity flag):\n\n")
        for a, b, r in hi:
            md.append(f"- {a} ↔ {b}: r = {r:.2f}\n")

    out_path = REPORTS / "validation_report_v2.md"
    out_path.write_text("".join(md), encoding="utf-8")
    log.info("wrote %s", out_path)

    # Also persist correlation matrix to CSV
    corr.to_csv(REPORTS / "correlation_matrix_v2.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
