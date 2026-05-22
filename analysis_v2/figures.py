"""Phase 5 — figures for the coursework.

Builds 7 publication-quality figures:
  F1 — Waterfall: Shapley R² decomposition (HEADLINE)
  F2 — Age profile: scatter + parabolic fit + peak marker
  F3 — Tier β_ppg by contract tier (H9 truncation pattern)
  F4 — Event study: ln(salary) around first All-NBA selection (τ = −2…+4)
  F5 — Boxplot of ln(salary) by contract tier (institutional pricing pattern)
  F6 — Forest plot: M_full main effects with 95% CI
  F7 — Sequential vs Shapley comparison (order-dependence diagnostic)

Output: analysis_v2/output/figures/F*.pdf + F*.png (300 dpi).

Run:
    python3 -m analysis_v2.figures
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis_v2.h9_tier import REFERENCE_TIER, TIERS, add_tier_dummies  # noqa: E402
from analysis_v2.m1_full import (  # noqa: E402
    AGE_BLOCK, AWARDS_BLOCK, DEMO_BLOCK_BASE, DURABILITY_BLOCK, INTL_BLOCK,
    STATS_BLOCK, STRUCT_BLOCK, TEAM_BLOCK, add_features, panel_index,
    prep_for_full,
)

log = logging.getLogger("analysis_v2.figures")
OUT_DIR = ROOT / "analysis_v2" / "output" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 100,
    "savefig.dpi": 300,
})

# Grayscale-safe palette
COL_MAIN = "#1f1f1f"
COL_ACCENT = "#7f7f7f"
COL_BG = "#dddddd"
COL_HIGHLIGHT = "#c44e52"


def _save(fig, name: str) -> None:
    pdf = OUT_DIR / f"{name}.pdf"
    png = OUT_DIR / f"{name}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, bbox_inches="tight")
    plt.close(fig)
    log.info("wrote %s.{pdf,png}", name)


# ===========================================================================
# F1 — Waterfall: Shapley R² decomposition
# ===========================================================================
def fig1_waterfall_shapley() -> None:
    shap = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "r2_shapley.csv"
    )
    # Order by descending Shapley value already (file is sorted).
    fig, ax = plt.subplots(figsize=(7, 4.5))

    cum = 0.0
    bottoms = []
    heights = []
    labels = []
    colors = []
    for _, row in shap.iterrows():
        bottoms.append(cum)
        heights.append(row["shapley_R2"])
        labels.append(row["block"])
        cum += row["shapley_R2"]
        # darker for bigger blocks
        intensity = max(0.15, min(0.85, 1.0 - row["share_of_explained"] * 1.5))
        colors.append(f"{intensity:.2f}")

    x = np.arange(len(labels))
    bars = ax.bar(x, heights, bottom=bottoms, color=colors,
                  edgecolor=COL_MAIN, linewidth=0.7)

    for i, (b, h, row) in enumerate(zip(bottoms, heights, shap.itertuples())):
        ax.text(i, b + h + 0.005,
                f"{h:.3f}\n({row.share_of_explained:.1%})",
                ha="center", va="bottom", fontsize=8)

    # Cumulative line
    cum_line = np.cumsum(heights)
    ax.plot(x, cum_line, "o-", color=COL_HIGHLIGHT, markersize=4,
            linewidth=1.2, label="Cumulative R²")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Shapley contribution to R²")
    ax.set_title("Декомпозиция R²: Shapley-вклад блоков факторов\n"
                 "(сумма = R² = 0.649, на 2 268 наблюдениях)")
    ax.set_ylim(0, 0.75)
    ax.legend(loc="upper right", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    _save(fig, "F1_waterfall_shapley")


# ===========================================================================
# F2 — Age profile
# ===========================================================================
def fig2_age_profile() -> None:
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = df.dropna(subset=["age", "ln_salary"])

    # Parabolic fit on ln_salary ~ age + age²
    X = sm.add_constant(pd.DataFrame({
        "age": df["age"], "age_sq": df["age"] ** 2,
    }))
    res = sm.OLS(df["ln_salary"], X).fit()
    a0, a1, a2 = res.params["const"], res.params["age"], res.params["age_sq"]
    peak_age = -a1 / (2 * a2)
    peak_value = a0 + a1 * peak_age + a2 * peak_age ** 2

    ages = np.linspace(df["age"].min(), df["age"].max(), 200)
    fit = a0 + a1 * ages + a2 * ages ** 2

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(df["age"] + np.random.uniform(-0.2, 0.2, len(df)),
               df["ln_salary"], s=4, alpha=0.18, color=COL_ACCENT)
    ax.plot(ages, fit, "-", color=COL_MAIN, linewidth=2,
            label=f"OLS fit: ln(s) = {a0:.1f} + {a1:.3f}·age "
                  f"− {abs(a2):.4f}·age²")
    ax.axvline(peak_age, color=COL_HIGHLIGHT, linestyle="--", linewidth=1,
               label=f"Peak: age = {peak_age:.1f}")
    ax.scatter([peak_age], [peak_value], color=COL_HIGHLIGHT, s=40, zorder=5)

    ax.set_xlabel("Age (years)")
    ax.set_ylabel("ln(salary, USD)")
    ax.set_title("Возрастной профиль зарплаты: параболическая аппроксимация")
    ax.legend(loc="lower center", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F2_age_profile")


# ===========================================================================
# F3 — β_ppg by contract tier (H9 truncation pattern)
# ===========================================================================
def fig3_tier_beta_ppg() -> None:
    ts = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "h9_tier_specific_betas.csv"
    )
    # Order tiers by economic seniority
    order = ["minimum", "rookie_scale", "mid_level", "high_mid",
             "max_25", "max_30", "max_35", "supermax"]
    ts["order"] = ts["tier"].map({k: i for i, k in enumerate(order)})
    ts = ts.dropna(subset=["order"]).sort_values("order")

    fig, ax = plt.subplots(figsize=(7, 4))
    y = np.arange(len(ts))
    ax.errorbar(
        ts["beta_ppg"], y,
        xerr=1.96 * ts["se_ppg"],
        fmt="o", color=COL_MAIN, capsize=3, markersize=6,
        ecolor=COL_ACCENT, elinewidth=1.0,
    )
    for i, (_, r) in enumerate(ts.iterrows()):
        ax.text(r["beta_ppg"] + 1.96 * r["se_ppg"] + 0.005, i,
                f"n={int(r['n'])}, p={r['p_ppg']:.3f}",
                va="center", fontsize=8, color=COL_ACCENT)

    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(ts["tier"])
    ax.set_xlabel(r"$\beta_{ppg}$ внутри tier (с кластер-SE на player_id)")
    ax.set_title("Tier-specific Mincer-регрессии: коэффициент при PPG\n"
                 "Cap-truncation подавляет цену performance в max-tiers")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F3_tier_beta_ppg")


# ===========================================================================
# F4 — Event study around first All-NBA
# ===========================================================================
def fig4_event_study_all_nba() -> None:
    es = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "h10_event_study.csv"
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    # Order: -2, -1, 0, 1, 2, 3, 4+
    label_order = ["-2", "-1", "0", "+1", "+2", "+3", "4plus"]
    es["pos"] = es["tau"].apply(lambda t: label_order.index(str(t)))
    es = es.sort_values("pos")

    ax.errorbar(es["pos"], es["beta"],
                yerr=[es["beta"] - es["ci_lo"], es["ci_hi"] - es["beta"]],
                fmt="o", color=COL_MAIN, capsize=3, markersize=6,
                ecolor=COL_ACCENT)

    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(label_order.index("0"), color=COL_HIGHLIGHT, linestyle="--",
               linewidth=0.8, label="Event: first All-NBA selection")
    ax.set_xticks(np.arange(len(label_order)))
    ax.set_xticklabels(["τ=−2", "τ=−1", "τ=0\n(year of)", "τ=+1", "τ=+2",
                        "τ=+3", "τ≥4"])
    ax.set_ylabel("Эффект на ln(salary), 95% CI")
    ax.set_title("Event-study: динамика salary вокруг первого All-NBA\n"
                 "Premium реализуется через 2-3 года (следующий контракт)")
    ax.legend(loc="upper left", frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F4_event_study_all_nba")


# ===========================================================================
# F5 — Boxplot ln(salary) by tier
# ===========================================================================
def fig5_tier_boxplot() -> None:
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    order = ["minimum", "rookie_scale", "mid_level", "high_mid",
             "max_25", "max_30", "max_35", "supermax"]
    df = df[df["contract_tier"].isin(order)].copy()

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    data = [df.loc[df["contract_tier"] == t, "ln_salary"].dropna().values
            for t in order]
    bp = ax.boxplot(data, tick_labels=order, patch_artist=True,
                    medianprops={"color": COL_HIGHLIGHT, "linewidth": 1.4},
                    boxprops={"facecolor": COL_BG, "edgecolor": COL_MAIN},
                    whiskerprops={"color": COL_MAIN},
                    capprops={"color": COL_MAIN},
                    flierprops={"marker": ".", "markersize": 2,
                                "markerfacecolor": COL_ACCENT,
                                "markeredgecolor": COL_ACCENT})
    # N annotations
    for i, t in enumerate(order):
        n = int(df["contract_tier"].eq(t).sum())
        ax.text(i + 1, ax.get_ylim()[0] + 0.2, f"n={n}",
                ha="center", fontsize=8, color=COL_ACCENT)

    ax.set_ylabel("ln(salary, USD)")
    ax.set_title("Распределение ln(salary) по контрактным tier\n"
                 "Дискретные ступени между tier — иллюстрация institutional pricing")
    ax.tick_params(axis="x", rotation=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F5_tier_boxplot")


# ===========================================================================
# F6 — Forest plot for M_full main effects
# ===========================================================================
def fig6_forest_M_full() -> None:
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v2.csv")
    df = add_features(df)
    df["supermax_eligible_loose"] = df["supermax_eligible_loose"].fillna(0).astype(int)
    d = prep_for_full(df)
    d, tier_cols = add_tier_dummies(d)
    di = panel_index(d)

    base = (
        STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK + AWARDS_BLOCK
        + DURABILITY_BLOCK + TEAM_BLOCK
        + [c for c in STRUCT_BLOCK if c not in ("post_cba_2017", "post_covid")]
        + ["top5_market"] + tier_cols + ["supermax_eligible_loose"]
    )
    d2 = di.dropna(subset=base + ["ln_salary"])
    X = sm.add_constant(d2[base].astype(float))
    y = d2["ln_salary"]
    res = PanelOLS(y, X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )

    # Select substantively interesting variables for forest plot (skip stats noise)
    keep = (
        ["ppg", "per", "vorp"]                              # performance
        + ["age", "age_sq", "experience"]                   # career arc
        + ["allstar", "undrafted", "log_draft_pick"]        # demo
        + ["born_canada", "born_europe", "born_asia_oceania"]
        + ["all_nba_lag1", "career_allstar_count"]
        + ["games_missed_lag1"]
        + ["team_win_pct_lag1", "team_over_luxury_tax_t"]
        + ["top5_market"]
        + tier_cols
        + ["supermax_eligible_loose"]
    )
    keep = [v for v in keep if v in res.params.index]

    params = res.params.loc[keep]
    se = res.std_errors.loc[keep]
    ci = res.conf_int().loc[keep]
    pvals = res.pvalues.loc[keep]

    # Order: tier_* first (top), then awards/durability, then perf/age (bottom)
    fig, ax = plt.subplots(figsize=(7.5, max(5, 0.3 * len(keep))))
    y_pos = np.arange(len(keep))[::-1]

    for i, var in enumerate(keep):
        pos = y_pos[i]
        p = pvals[var]
        color = COL_HIGHLIGHT if p < 0.05 else COL_MAIN
        ax.errorbar(
            params[var], pos,
            xerr=[[params[var] - ci.loc[var, "lower"]],
                  [ci.loc[var, "upper"] - params[var]]],
            fmt="o", color=color, markersize=5,
            ecolor=color, capsize=2.5, alpha=0.9,
        )

    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(keep)
    ax.set_xlabel("Coefficient (с 95% CI, cluster-robust по player_id)")
    ax.set_title(f"M_full: forest plot главных эффектов "
                 f"(R² = {res.rsquared:.3f}, N = {int(res.nobs)})")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F6_forest_M_full")


# ===========================================================================
# F7 — Sequential vs Shapley (order-dependence diagnostic)
# ===========================================================================
def fig7_seq_vs_shapley() -> None:
    seq = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "r2_decomposition.csv"
    )
    rev = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "r2_decomposition_reverse.csv"
    )
    shap = pd.read_csv(
        ROOT / "analysis_v2" / "output" / "tables" / "r2_shapley.csv"
    )

    seq = seq[seq["block"] != "(intercept only)"]
    rev = rev[rev["block"] != "(intercept only)"]
    seq_map = dict(zip(seq["block"], seq["dR2"]))
    rev_map = dict(zip(rev["block"], rev["dR2"]))
    shap_map = dict(zip(shap["block"], shap["shapley_R2"]))

    blocks = list(seq_map.keys())
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(blocks))
    width = 0.27

    ax.bar(x - width, [seq_map[b] for b in blocks], width,
           label="Sequential (plan-order)", color="#888888")
    ax.bar(x, [rev_map[b] for b in blocks], width,
           label="Sequential (reverse)", color="#444444")
    ax.bar(x + width, [shap_map[b] for b in blocks], width,
           label="Shapley", color=COL_HIGHLIGHT)

    ax.set_xticks(x)
    ax.set_xticklabels(blocks, rotation=30, ha="right")
    ax.set_ylabel("ΔR² attribution")
    ax.set_title("Order-dependence в декомпозиции R²:\n"
                 "sequential зависит от порядка, Shapley — нет")
    ax.legend(frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "F7_seq_vs_shapley")


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    fig1_waterfall_shapley()
    fig2_age_profile()
    fig3_tier_beta_ppg()
    fig4_event_study_all_nba()
    fig5_tier_boxplot()
    fig6_forest_M_full()
    fig7_seq_vs_shapley()

    # Index / metadata
    index_md = (ROOT / "analysis_v2" / "reports" / "figures_index.md")
    index_md.write_text(
        "# Figures index\n\n"
        "| File | Описание |\n|---|---|\n"
        "| F1_waterfall_shapley | Shapley-декомпозиция R² по 9 блокам — **главный рисунок работы** |\n"
        "| F2_age_profile | Возрастной профиль ln(salary) с параболической аппроксимацией |\n"
        "| F3_tier_beta_ppg | β_ppg внутри каждого contract tier — иллюстрация cap-truncation |\n"
        "| F4_event_study_all_nba | Event study вокруг первого All-NBA (τ = −2…+4) |\n"
        "| F5_tier_boxplot | Boxplot ln(salary) по 8 tier'ам — institutional pricing |\n"
        "| F6_forest_M_full | Forest plot main effects M_full с 95% CI |\n"
        "| F7_seq_vs_shapley | Sequential vs Shapley — order-dependence diagnostic |\n",
        encoding="utf-8",
    )
    log.info("wrote figures index → %s", index_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
