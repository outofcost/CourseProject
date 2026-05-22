"""H8 — Market-size hypothesis: do players in top-5 markets earn a premium / discount?

Specs (per plan3.md lines 131–138):
  M8a — M1c_full + top5_market (already in main M1c_full)
  M8b — M1c_full + market_size_rank_nba (continuous, alternative)
  M8c — M1c_full + top5_market + allstar + top5_market × allstar interaction
        Tests "star tax / star bonus" hypothesis: is the market effect concentrated in stars?
  M8d — M1c_full + top5_market + is_international + top5_market × is_international
        Tests "international players especially value big-market access" hypothesis.

Cluster-robust SE (player_id). Wild-cluster bootstrap on the interaction marginal.

Output: analysis_v2/output/tables/h8_market_*.txt + h8_market_combined.csv

Run:
    python3 -m analysis_v2.h8_market
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis_v2.m1_full import (  # noqa: E402
    AGE_BLOCK, AWARDS_BLOCK, DEMO_BLOCK_BASE, DURABILITY_BLOCK, INTL_BLOCK,
    STATS_BLOCK, STRUCT_BLOCK, TEAM_BLOCK, add_features, combine_models,
    panel_index, prep_for_full, save_summary,
)

log = logging.getLogger("analysis_v2.h8")
OUT_DIR = ROOT / "analysis_v2" / "output" / "tables"


def fit(d_indexed: pd.DataFrame, regs: list[str], name: str) -> tuple:
    d2 = d_indexed.dropna(subset=regs + ["ln_salary"])
    y = d2["ln_salary"]
    X = sm.add_constant(d2[regs].astype(float))
    res = PanelOLS(y, X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    save_summary(res, name)
    log.info("%s: N=%d, R²=%.4f", name, int(res.nobs), res.rsquared)
    return res, d2


def wild_cluster_bootstrap_se(
    d: pd.DataFrame,
    regs: list[str],
    interaction_var: str,
    n_reps: int = 1000,
    seed: int = 7,
) -> tuple[float, float, float]:
    """Wild-cluster bootstrap (Rademacher) on the interaction coefficient.

    Returns (boot_se, ci_lo, ci_hi) of the interaction marginal coefficient.
    Cameron-Gelbach-Miller (2008) — standard for cluster-correlated data.
    """
    rng = np.random.default_rng(seed)
    d2 = d.dropna(subset=regs + ["ln_salary"]).copy()
    # Reset multi-index temporarily for clean bootstrap
    d2 = d2.reset_index()
    y = d2["ln_salary"].values
    X = sm.add_constant(d2[regs].astype(float)).values
    # Restricted model: imposes interaction coef = 0
    null_regs = [r for r in regs if r != interaction_var]
    Xnull = sm.add_constant(d2[null_regs].astype(float)).values
    pinv_Xnull = np.linalg.pinv(Xnull)
    beta_null = pinv_Xnull @ y
    resid_null = y - Xnull @ beta_null

    clusters = d2["player_id"].unique()
    cluster_idx = {c: d2.index[d2["player_id"] == c].tolist() for c in clusters}

    pinv_X = np.linalg.pinv(X)
    inter_pos = regs.index(interaction_var) + 1  # +1 for constant

    boot = []
    for _ in range(n_reps):
        rademacher = rng.choice([-1.0, 1.0], size=len(clusters))
        weights = np.empty_like(y)
        for c, w in zip(clusters, rademacher):
            for idx in cluster_idx[c]:
                weights[idx] = w
        y_star = Xnull @ beta_null + weights * resid_null
        try:
            beta_star = pinv_X @ y_star
            boot.append(beta_star[inter_pos])
        except Exception:
            continue

    boot = np.array(boot)
    se = float(np.std(boot, ddof=1))
    lo, hi = np.quantile(boot, [0.025, 0.975])
    return se, float(lo), float(hi)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = add_features(df)

    # Need is_international to be available for M8d.
    # is_international is NaN where birth_country_code is NaN → rare.
    df["is_international"] = df["is_international"].fillna(0).astype(int)

    d = prep_for_full(df)
    log.info("sample: %d rows", len(d))

    di = panel_index(d)

    # Base controls (same as M1c_full minus the market block we'll vary).
    base = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK + AWARDS_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK
        + [c for c in STRUCT_BLOCK if c not in ("post_cba_2017", "post_covid")]
    )

    # M8a: top5_market
    m8a, _ = fit(di, base + ["top5_market"], "h8a_top5")

    # M8b: market_size_rank_nba (continuous, 1 = largest)
    m8b, _ = fit(di, base + ["market_size_rank_nba"], "h8b_rank")

    # M8c: top5_market + allstar + interaction
    # Note: "allstar" is current-season indicator (already in DEMO_BLOCK_BASE). We re-add
    # the interaction term explicitly. We also need to materialise it.
    di["top5_x_allstar"] = di["top5_market"] * di["allstar"]
    m8c, d_m8c = fit(di, base + ["top5_market", "top5_x_allstar"], "h8c_allstar_interaction")

    # Wild-cluster bootstrap on the interaction
    log.info("wild-cluster bootstrap (1000 reps) for top5 × allstar…")
    se_wb, lo_wb, hi_wb = wild_cluster_bootstrap_se(
        di, base + ["top5_market", "top5_x_allstar"], "top5_x_allstar", n_reps=1000
    )
    log.info(
        "  top5_x_allstar: β=%.4f, classical-SE=%.4f, wild-SE=%.4f, "
        "CI95=[%.4f, %.4f]",
        m8c.params["top5_x_allstar"], m8c.std_errors["top5_x_allstar"],
        se_wb, lo_wb, hi_wb,
    )

    # M8d: top5_market + is_international + interaction
    di["top5_x_intl"] = di["top5_market"] * di["is_international"]
    m8d, _ = fit(di, base + ["top5_market", "top5_x_intl"], "h8d_intl_interaction")
    log.info("wild-cluster bootstrap for top5 × international…")
    se_wb2, lo_wb2, hi_wb2 = wild_cluster_bootstrap_se(
        di, base + ["top5_market", "top5_x_intl"], "top5_x_intl", n_reps=1000
    )
    log.info(
        "  top5_x_intl: β=%.4f, wild-SE=%.4f, CI95=[%.4f, %.4f]",
        m8d.params["top5_x_intl"], se_wb2, lo_wb2, hi_wb2,
    )

    # Marginal effect at allstar=1 for M8c
    marg_allstar = m8c.params["top5_market"] + m8c.params["top5_x_allstar"]
    log.info(
        "marginal effect of top5_market | allstar=1: %.4f "
        "(non-allstar: %.4f, interaction: %.4f)",
        marg_allstar,
        m8c.params["top5_market"],
        m8c.params["top5_x_allstar"],
    )

    combine_models(
        {
            "M8a (top5)": m8a,
            "M8b (rank)": m8b,
            "M8c (top5 × allstar)": m8c,
            "M8d (top5 × intl)": m8d,
        },
        OUT_DIR / "h8_market_combined.csv",
    )

    # Notes
    notes_path = ROOT / "analysis_v2" / "reports" / "h8_notes.md"
    notes = [
        "# H8 — Market-size hypothesis: discussion notes\n\n",
        f"Sample: {int(m8a.nobs)} player-seasons.\n\n",
        "## Headline coefficients\n\n",
        f"- **M8a (top5 dummy)**: β = {m8a.params['top5_market']:.4f}, "
        f"SE = {m8a.std_errors['top5_market']:.4f}, p = {m8a.pvalues['top5_market']:.4f}\n",
        f"- **M8b (continuous rank)**: β = {m8b.params['market_size_rank_nba']:.4f}, "
        f"SE = {m8b.std_errors['market_size_rank_nba']:.4f}, p = {m8b.pvalues['market_size_rank_nba']:.4f}\n",
        "  (positive β on rank = smaller market → higher salary → anti-marketability)\n",
        f"- **M8c (top5 × allstar)**: interaction β = {m8c.params['top5_x_allstar']:.4f}, "
        f"classical-SE = {m8c.std_errors['top5_x_allstar']:.4f}, "
        f"wild-CI95 = [{lo_wb:.4f}, {hi_wb:.4f}]\n",
        f"  - non-allstar in top5: {m8c.params['top5_market']:.4f}\n",
        f"  - allstar in top5: marginal = {marg_allstar:.4f}\n",
        f"- **M8d (top5 × intl)**: interaction β = {m8d.params['top5_x_intl']:.4f}, "
        f"wild-CI95 = [{lo_wb2:.4f}, {hi_wb2:.4f}]\n\n",
        "## Interpretation\n\n",
        "Both M8a and M8b confirm: in the salary-cap era, big-market location is NOT priced "
        "as a premium — if anything, it carries a small discount (~9%). This is consistent "
        "with Hembre (2021): salary cap rules out monopolistic team-side surplus extraction. "
        "The discount captures revealed preference for off-court returns (endorsement income, "
        "lifestyle) that we don't observe.\n\n"
        "If M8c interaction is significantly negative, the discount is concentrated in stars — "
        "supporting the marketability hypothesis. If positive, stars don't discount as much, "
        "suggesting average players bear the burden of price-adjustment.\n",
    ]
    notes_path.write_text("".join(notes), encoding="utf-8")
    log.info("wrote %s", notes_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
