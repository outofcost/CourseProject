"""Sequential R² decomposition (the headline new chapter of the coursework).

For each cumulative block addition, compute ΔR² and (cluster-bootstrap) 95% CI.

Block ordering (per plan3.md lines 122):
  1. Performance       (ppg, rpg, apg, spg, bpg, mpg, gp, per, ws, vorp, usg_pct)
  2. Age + experience  (age, age_sq, experience)
  3. Demographics      (allstar, undrafted, log_draft_pick, pos_*)
  4. International     (born_canada, born_europe, born_latam, born_africa, born_asia_oceania)
  5. Awards            (all_nba_lag1, career_all_nba_count, career_allstar_count)
  6. Structural        (post_cba_2017, post_covid, no_income_tax)
  7. Market            (top5_market)
  8. Team controls     (team_win_pct_lag1, team_made_playoffs_lag1, team_over_luxury_tax_t)
  9. Durability        (games_missed_lag1, games_missed_3y_cum)

Bootstrap: 200 cluster-resamples on player_id. Refit all cumulative specs per rep.
Save output to:
  analysis_v2/output/tables/r2_decomposition.csv

Also runs a reverse-order spec (durability → performance) and saves
  analysis_v2/output/tables/r2_decomposition_reverse.csv
to show order-dependence — motivates the Shapley alternative (heavy, optional).

Run:
    python3 -m analysis_v2.h_decomposition
"""
from __future__ import annotations

import itertools
import logging
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis_v2.m1_full import add_features, prep_for_full  # noqa: E402

log = logging.getLogger("analysis_v2.decomp")
OUT_DIR = ROOT / "analysis_v2" / "output" / "tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BLOCKS: list[tuple[str, list[str]]] = [
    ("Performance", ["ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
                     "per", "ws", "vorp", "usg_pct"]),
    ("Age",         ["age", "age_sq", "experience"]),
    ("Demographics", ["allstar", "undrafted", "log_draft_pick",
                      "pos_PG", "pos_SG", "pos_SF", "pos_PF"]),
    ("International", ["born_canada", "born_europe", "born_latam",
                       "born_africa", "born_asia_oceania"]),
    ("Awards",      ["all_nba_lag1", "career_all_nba_count",
                     "career_allstar_count"]),
    ("Structural",  ["post_cba_2017", "post_covid", "no_income_tax"]),
    ("Market",      ["top5_market"]),
    ("Team",        ["team_win_pct_lag1", "team_made_playoffs_lag1",
                     "team_over_luxury_tax_t"]),
    ("Durability",  ["games_missed_lag1", "games_missed_3y_cum"]),
]


def fit_ols_rsquared(d: pd.DataFrame, regs: list[str]) -> float:
    """OLS R² (in-sample). Skip cluster-SE — only need R² for decomposition."""
    if not regs:
        return 0.0
    sub = d.dropna(subset=regs + ["ln_salary"])
    y = sub["ln_salary"]
    X = sm.add_constant(sub[regs].astype(float))
    try:
        res = sm.OLS(y, X).fit()
    except Exception as e:
        log.warning("OLS fit failed for %d regressors: %s", len(regs), e)
        return np.nan
    return float(res.rsquared)


def cumulative_r2(d: pd.DataFrame, blocks: list[tuple[str, list[str]]]) -> pd.DataFrame:
    """Return DataFrame with one row per cumulative step."""
    rows = []
    accum: list[str] = []
    prev_r2 = 0.0
    rows.append({"step": 0, "block": "(intercept only)", "n_regs": 0, "R2": 0.0, "dR2": 0.0})
    for i, (name, regs) in enumerate(blocks, start=1):
        accum = accum + regs
        r2 = fit_ols_rsquared(d, accum)
        dr2 = r2 - prev_r2
        rows.append({
            "step": i,
            "block": name,
            "n_regs": len(accum),
            "R2": r2,
            "dR2": dr2,
        })
        prev_r2 = r2
    return pd.DataFrame(rows)


def cluster_bootstrap_dr2(
    d: pd.DataFrame,
    blocks: list[tuple[str, list[str]]],
    n_reps: int = 200,
    seed: int = 1729,
) -> pd.DataFrame:
    """Cluster-bootstrap (resample player_id with replacement). Return per-rep ΔR² table."""
    rng = np.random.default_rng(seed)
    clusters = d["player_id"].unique()
    n_c = len(clusters)
    cluster_groups = {c: d[d["player_id"] == c] for c in clusters}

    all_runs: list[pd.DataFrame] = []
    for rep in range(n_reps):
        sample_clusters = rng.choice(clusters, size=n_c, replace=True)
        # Concat with fresh keys so identical clusters duplicate (proper cluster boot).
        bs = pd.concat(
            [cluster_groups[c] for c in sample_clusters], ignore_index=True
        )
        run = cumulative_r2(bs, blocks)
        run["rep"] = rep
        all_runs.append(run)
        if (rep + 1) % 50 == 0:
            log.info("  bootstrap rep %d / %d", rep + 1, n_reps)
    return pd.concat(all_runs, ignore_index=True)


def summarize_bootstrap(bs_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate bootstrap reps → mean / 2.5pct / 97.5pct per block."""
    return (
        bs_df.groupby("block", sort=False)
        .agg(
            dR2_mean=("dR2", "mean"),
            dR2_lo=("dR2", lambda s: s.quantile(0.025)),
            dR2_hi=("dR2", lambda s: s.quantile(0.975)),
            R2_mean=("R2", "mean"),
        )
        .reset_index()
    )


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    src = ROOT / "data" / "clean" / "data_analysis_v2.csv"
    df = pd.read_csv(src)
    df = add_features(df)
    d = prep_for_full(df)
    log.info("decomposition sample: %d rows, %d unique players",
             len(d), d["player_id"].nunique())

    # Point estimate
    pt = cumulative_r2(d, BLOCKS)
    pt["share_of_total"] = pt["dR2"] / pt["dR2"].sum()
    pt.to_csv(OUT_DIR / "r2_decomposition.csv", index=False)
    log.info("\n%s", pt.to_string(index=False))

    # Bootstrap CIs
    log.info("running bootstrap (200 cluster-resamples on player_id)…")
    bs = cluster_bootstrap_dr2(d, BLOCKS, n_reps=200)
    summary = summarize_bootstrap(bs)
    # Merge point estimate + CI bands
    pt2 = pt.merge(summary, on="block", how="left", suffixes=("", "_bs"))
    pt2.to_csv(OUT_DIR / "r2_decomposition_with_ci.csv", index=False)
    log.info("\n%s", pt2[["block", "n_regs", "R2", "dR2", "dR2_lo", "dR2_hi",
                          "share_of_total"]].to_string(index=False))

    # Reverse-order spec (robustness)
    reverse_blocks = list(reversed(BLOCKS))
    pt_rev = cumulative_r2(d, reverse_blocks)
    pt_rev["share_of_total"] = pt_rev["dR2"] / pt_rev["dR2"].sum()
    pt_rev.to_csv(OUT_DIR / "r2_decomposition_reverse.csv", index=False)
    log.info("REVERSE-ORDER decomposition:")
    log.info("\n%s", pt_rev.to_string(index=False))

    # ---------------- Shapley decomposition (order-independent) -------------
    # For n=9 blocks: 2^9 = 512 subset R² fits. Each ~ms → ~10 sec total.
    log.info("computing Shapley values (2^%d = %d subset fits)…", len(BLOCKS), 2 ** len(BLOCKS))
    block_names = [b[0] for b in BLOCKS]
    n_blocks = len(BLOCKS)
    all_r2: dict[frozenset, float] = {}
    for k in range(0, n_blocks + 1):
        for S in itertools.combinations(range(n_blocks), k):
            regs = []
            for i in S:
                regs.extend(BLOCKS[i][1])
            all_r2[frozenset(S)] = fit_ols_rsquared(d, regs) if regs else 0.0
        log.info("  Shapley: k=%d done (%d subsets)", k, math.comb(n_blocks, k))

    shapleys = {i: 0.0 for i in range(n_blocks)}
    for i in range(n_blocks):
        others = [j for j in range(n_blocks) if j != i]
        for k in range(0, n_blocks):
            w = math.factorial(k) * math.factorial(n_blocks - k - 1) / math.factorial(n_blocks)
            for S in itertools.combinations(others, k):
                r_with = all_r2[frozenset(set(S) | {i})]
                r_without = all_r2[frozenset(S)]
                shapleys[i] += w * (r_with - r_without)

    full_r2 = all_r2[frozenset(range(n_blocks))]
    sh_df = pd.DataFrame(
        [
            {
                "block": block_names[i],
                "shapley_R2": shapleys[i],
                "share_of_explained": shapleys[i] / full_r2 if full_r2 else 0.0,
            }
            for i in range(n_blocks)
        ]
    ).sort_values("shapley_R2", ascending=False).reset_index(drop=True)
    sh_df.to_csv(OUT_DIR / "r2_shapley.csv", index=False)
    log.info("Shapley:\n%s", sh_df.to_string(index=False))
    log.info("sum(shapley) = %.4f, full R² = %.4f (should match)",
             sh_df["shapley_R2"].sum(), full_r2)

    log.info("DONE — outputs in %s", OUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
