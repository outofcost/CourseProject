"""§5.6 — все обязательные фигуры V1.

Все фигуры → output/figures_v1/. matplotlib only, minimal style.

Axis labels по-русски, titles по-английски (consistency с tex literature).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (BASIC_STATS, COMBINED_STATS,  # noqa: E402
                             COMMON_NO_STRUCT, COMMON_STRUCT,
                             COMMON_WITHIN, DATA_CLEAN)
from analysis_v1.utils_v1 import (OUT_FIGURES_V1, panel_index,  # noqa: E402
                                  prep_for_models)

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3})


def fig_1_distribution_salary(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    salaries = df["salary_usd"].dropna()
    ax.hist(np.log10(salaries), bins=50, color="steelblue", edgecolor="white")
    ax.set_xlabel("log₁₀(salary, USD)")
    ax.set_ylabel("Число игрок-сезонов")
    ax.set_title("Distribution of NBA salaries (2015/16 — 2023/24)")
    ax.axvline(np.log10(salaries.median()), color="red", ls="--",
               label=f"median = ${salaries.median()/1e6:.1f}M")
    ax.legend()
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_1_distribution_salary.png", dpi=150)
    plt.close(fig)


def fig_2_lnsalary_by_season(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    data = [df[df["season"] == s]["ln_salary"].dropna() for s in
            sorted(df["season"].unique())]
    seasons = sorted(df["season"].unique())
    ax.boxplot(data, tick_labels=seasons, showfliers=False)
    ax.set_xlabel("Сезон (season_end)")
    ax.set_ylabel("ln(salary)")
    ax.set_title("ln(salary) distribution by season")
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_2_distribution_lnsalary_by_season.png",
                dpi=150)
    plt.close(fig)


def fig_3_ppg_vs_salary(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sub = df.dropna(subset=["ppg", "ln_salary"])
    sc = ax.scatter(sub["ppg"], sub["ln_salary"], c=sub["season"],
                    s=8, alpha=0.4, cmap="viridis")
    plt.colorbar(sc, label="season")
    # Quadratic fit
    x = sub["ppg"].values
    y = sub["ln_salary"].values
    p = np.polyfit(x, y, 2)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, np.polyval(p, xs), "r-", lw=2, label=f"poly2 fit")
    ax.set_xlabel("PPG (очки за игру)")
    ax.set_ylabel("ln(salary)")
    ax.set_title("ln(salary) vs PPG, by season")
    ax.legend()
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_3_scatter_ppg_vs_salary.png", dpi=150)
    plt.close(fig)


def fig_4_age_profile(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    grp = df.groupby("age")["ln_salary"].agg(["mean", "count"])
    grp = grp[grp["count"] >= 20]
    ax.scatter(grp.index, grp["mean"], s=grp["count"] / 5, alpha=0.6,
               color="steelblue", edgecolor="navy",
               label="mean ln(salary) by age (point size ∝ N)")
    # Quadratic fit
    p = np.polyfit(grp.index, grp["mean"], 2)
    xs = np.linspace(grp.index.min(), grp.index.max(), 100)
    ax.plot(xs, np.polyval(p, xs), "r-", lw=2,
            label=f"poly2: peak ≈ {-p[1]/(2*p[0]):.1f}")
    ax.set_xlabel("Возраст")
    ax.set_ylabel("Mean ln(salary)")
    ax.set_title("Age profile (raw, unconditional)")
    ax.legend()
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_4_age_profile.png", dpi=150)
    plt.close(fig)


def fig_5_age_profile_conditional(df):
    """Partial regression: residualize ln_salary and age on other regressors."""
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)
    controls = [c for c in BASIC_STATS + COMMON_STRUCT
                if c not in ("age", "age_sq")]
    X_ctrl = sm.add_constant(d[controls].astype(float))
    y = d["ln_salary"].astype(float)
    age = d["age"].astype(float)
    res_y = sm.OLS(y, X_ctrl).fit().resid
    res_age = sm.OLS(age, X_ctrl).fit().resid

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(res_age, res_y, s=6, alpha=0.3, color="steelblue")
    p = np.polyfit(res_age, res_y, 2)
    xs = np.linspace(res_age.min(), res_age.max(), 100)
    ax.plot(xs, np.polyval(p, xs), "r-", lw=2, label="poly2 fit (partial)")
    ax.set_xlabel("residualised age")
    ax.set_ylabel("residualised ln(salary)")
    ax.set_title("Conditional age profile (partial regression)")
    ax.legend()
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_5_age_profile_conditional.png", dpi=150)
    plt.close(fig)


def fig_6_coefplot_M1(df):
    d = prep_for_models(df, restrict_single_team=False)
    d_idx = panel_index(d)
    y = d_idx["ln_salary"]
    fits = {
        "M1a": PooledOLS(y, sm.add_constant(d_idx[BASIC_STATS + COMMON_STRUCT])).fit(
            cov_type="clustered", cluster_entity=True),
        "M1b": PanelOLS(y, sm.add_constant(d_idx[BASIC_STATS + COMMON_NO_STRUCT]),
                        time_effects=True).fit(
            cov_type="clustered", cluster_entity=True),
        "M1c": PanelOLS(y, sm.add_constant(d_idx[COMBINED_STATS + COMMON_NO_STRUCT]),
                        time_effects=True).fit(
            cov_type="clustered", cluster_entity=True),
        "M1d": PanelOLS(y, d_idx[COMBINED_STATS + COMMON_WITHIN],
                        entity_effects=True, time_effects=True).fit(
            cov_type="clustered", cluster_entity=True),
    }
    key = ["ppg", "rpg", "apg", "age", "experience", "undrafted", "allstar"]
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.18
    for i, (name, fit) in enumerate(fits.items()):
        coefs, ses, pos = [], [], []
        for j, v in enumerate(key):
            if v in fit.params.index:
                coefs.append(fit.params[v])
                ses.append(fit.std_errors[v])
                pos.append(j + (i - 1.5) * width)
        ax.errorbar(coefs, pos, xerr=1.96 * np.asarray(ses), fmt="o",
                    label=name, capsize=2, markersize=4)
    ax.axvline(0, color="gray", ls="--", lw=0.8)
    ax.set_yticks(range(len(key)))
    ax.set_yticklabels(key)
    ax.set_xlabel("Coefficient (95% CI)")
    ax.set_title("M1a–M1d coefficient plot")
    ax.legend()
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_6_coefficient_plot_M1.png", dpi=150)
    plt.close(fig)


def fig_7_coefplot_M3(df):
    """M3 coefficient plot: contract_year (composite) vs cy_exogenous (canonical)
    vs cy_A_up (circular)."""
    rows = pd.read_csv(ROOT / "output" / "tables_v1" / "changes_summary.csv")
    fig, ax = plt.subplots(figsize=(8, 5))
    labels = [
        ("M3a level\ncontract_year (composite, V1)", -0.5332, 0.0246),
        ("M3c (Δ, composite cy)", 0.4545, 0.0219),
        ("M3c_canonical\n(Δ, cy_exogenous)", -0.0051, 0.0261),
        ("M3c_circular\n(Δ, cy_A_up)", 0.9155, 0.0208),
        ("M3d within\ncontract_year", -0.4462, 0.0325),
    ]
    coefs = [c for _, c, _ in labels]
    ses = [s for _, _, s in labels]
    names = [n for n, _, _ in labels]
    pos = list(range(len(labels)))
    colors = ["steelblue", "orange", "green", "red", "steelblue"]
    ax.errorbar(coefs, pos, xerr=[1.96 * s for s in ses],
                fmt="o", capsize=4, color="black",
                ecolor="gray", markersize=8)
    for i, (c, p) in enumerate(zip(coefs, pos)):
        ax.scatter([c], [p], color=colors[i], s=80, zorder=5)
    ax.axvline(0, color="gray", ls="--", lw=0.8)
    ax.set_yticks(pos)
    ax.set_yticklabels(names)
    ax.set_xlabel("Coefficient (95% CI)")
    ax.set_title("M3 — contract_year coefficients across specifications")
    ax.text(0.5, -0.5, "green = canonical (no circularity)\n"
                       "red = deliberately circular (for contrast)",
            fontsize=8, color="gray")
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_7_coefficient_plot_M3.png", dpi=150)
    plt.close(fig)


def fig_8_residuals_M1a(df):
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)
    X = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT].astype(float))
    y = d["ln_salary"].astype(float)
    fit = sm.OLS(y, X).fit()
    resid = fit.resid
    fitted = fit.fittedvalues

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(fitted, resid, s=5, alpha=0.4, color="steelblue")
    axes[0].axhline(0, color="red", ls="--", lw=0.8)
    axes[0].set_xlabel("Fitted ln(salary)")
    axes[0].set_ylabel("Residual")
    axes[0].set_title("Residuals vs Fitted (M1a)")

    axes[1].scatter(d["ppg"], resid, s=5, alpha=0.4, color="steelblue")
    axes[1].axhline(0, color="red", ls="--", lw=0.8)
    axes[1].set_xlabel("PPG")
    axes[1].set_ylabel("Residual")
    axes[1].set_title("Residuals vs PPG")
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_8_residuals_M1a.png", dpi=150)
    plt.close(fig)


def fig_9_predicted_vs_actual(df):
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)
    X = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT].astype(float))
    y = d["ln_salary"].astype(float)
    fit = sm.OLS(y, X).fit()
    pred = fit.fittedvalues

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(pred, y, s=5, alpha=0.4, color="steelblue")
    lims = [min(pred.min(), y.min()), max(pred.max(), y.max())]
    ax.plot(lims, lims, "r--", lw=1)
    ax.set_xlabel("Predicted ln(salary)")
    ax.set_ylabel("Actual ln(salary)")
    ax.set_title(f"Predicted vs Actual (M1a, R² = {fit.rsquared:.3f})")
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_9_predicted_vs_actual.png", dpi=150)
    plt.close(fig)


def fig_10_corr_heatmap(df):
    d = prep_for_models(df, restrict_single_team=False)
    stats = ["ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
             "per", "ws", "vorp", "usg_pct", "ts_pct"]
    corr = d[stats].corr()
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(stats))); ax.set_xticklabels(stats, rotation=45, ha="right")
    ax.set_yticks(range(len(stats))); ax.set_yticklabels(stats)
    for i in range(len(stats)):
        for j in range(len(stats)):
            ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center",
                    fontsize=7, color="white" if abs(corr.iloc[i,j]) > 0.5 else "black")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Correlation heatmap: stats × stats")
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_10_correlation_heatmap.png", dpi=150)
    plt.close(fig)


def fig_11_quantile_coefficients():
    long_df = pd.read_csv(ROOT / "output" / "tables_v1" / "quantile_M1a_long.csv")
    vars_ = ["ppg", "age", "undrafted", "experience",
             "post_cba_2017", "post_covid", "allstar"]
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for i, v in enumerate(vars_):
        ax = axes[i // 4, i % 4]
        sub = long_df[long_df["variable"] == v]
        ax.errorbar(sub["tau"], sub["beta"], yerr=1.96 * sub["se"],
                    fmt="o-", capsize=3, color="steelblue")
        ax.axhline(0, ls="--", color="gray", lw=0.8)
        ax.set_xlabel("τ (quantile)")
        ax.set_ylabel(f"β({v})")
        ax.set_title(v)
    axes[1, 3].axis("off")
    fig.suptitle("M1a quantile regression coefficients (95% CI, cluster bootstrap)",
                 fontsize=12)
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_11_quantile_coefficients.png", dpi=150)
    plt.close(fig)


def fig_13_tax_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    # средний state_tax_rate за весь период по командам
    tx = df.groupby("team_abbr")["state_tax_rate"].mean().dropna()
    tx = tx.sort_values()
    colors = ["red" if t == "TOR" else "steelblue" for t in tx.index]
    ax.bar(range(len(tx)), tx.values, color=colors)
    ax.set_xticks(range(len(tx))); ax.set_xticklabels(tx.index, rotation=90)
    ax.set_ylabel("state_tax_rate (mean across seasons)")
    ax.set_title("Distribution of state/provincial tax rates by team "
                 "(Toronto highlighted)")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_13_tax_distribution.png", dpi=150)
    plt.close(fig)


def fig_14_contract_year_diagnostic(df):
    """Δlog_salary distribution: V0 cy_A (legacy) vs V1 cy_exogenous (canonical)."""
    sub = df.dropna(subset=["salary_next", "salary_usd"]).copy()
    sub = sub[(sub["salary_usd"] > 0) & (sub["salary_next"] > 0)]
    sub["dlog"] = np.log(sub["salary_next"] / sub["salary_usd"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    # V0 cy_A: 1 if |real_salary_change| > 0.25 — recompute from data
    sub["cy_A_v0"] = (sub["real_salary_change"].abs() > 0.25).astype(int)
    for cy_val, color, label in [(0, "steelblue", "cy_A = 0"),
                                  (1, "orange", "cy_A = 1")]:
        d = sub[sub["cy_A_v0"] == cy_val]["dlog"]
        axes[0].hist(d, bins=40, alpha=0.6, color=color,
                     label=f"{label} (N={len(d)})", density=True)
    axes[0].axvline(0, color="black", ls="--", lw=0.8)
    axes[0].set_xlabel("Δlog(salary)")
    axes[0].set_ylabel("Density")
    axes[0].set_title("V0 cy_A (circular: defined from Δsalary)")
    axes[0].legend()
    axes[0].set_xlim(-2, 3)

    # V1 cy_exogenous
    sub2 = sub.dropna(subset=["cy_exogenous"])
    for cy_val, color, label in [(0, "steelblue", "cy_exogenous = 0"),
                                  (1, "orange", "cy_exogenous = 1")]:
        d = sub2[sub2["cy_exogenous"] == cy_val]["dlog"]
        axes[1].hist(d, bins=40, alpha=0.6, color=color,
                     label=f"{label} (N={len(d)})", density=True)
    axes[1].axvline(0, color="black", ls="--", lw=0.8)
    axes[1].set_xlabel("Δlog(salary)")
    axes[1].set_title("V1 cy_exogenous (canonical: no Δsalary in definition)")
    axes[1].legend()
    axes[1].set_xlim(-2, 3)

    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "fig_14_contract_year_diagnostic.png", dpi=150)
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")

    print("Generating figures...")
    fig_1_distribution_salary(df);         print("  ✓ fig_1")
    fig_2_lnsalary_by_season(df);          print("  ✓ fig_2")
    fig_3_ppg_vs_salary(df);               print("  ✓ fig_3")
    fig_4_age_profile(df);                 print("  ✓ fig_4")
    fig_5_age_profile_conditional(df);     print("  ✓ fig_5")
    fig_6_coefplot_M1(df);                 print("  ✓ fig_6")
    fig_7_coefplot_M3(df);                 print("  ✓ fig_7")
    fig_8_residuals_M1a(df);               print("  ✓ fig_8")
    fig_9_predicted_vs_actual(df);         print("  ✓ fig_9")
    fig_10_corr_heatmap(df);               print("  ✓ fig_10")
    fig_11_quantile_coefficients();         print("  ✓ fig_11")
    # fig_12 (event-study) уже сгенерирована event_study.py
    fig_13_tax_distribution(df);            print("  ✓ fig_13")
    fig_14_contract_year_diagnostic(df);    print("  ✓ fig_14")
    print(f"All figures saved to {OUT_FIGURES_V1}/")


if __name__ == "__main__":
    main()
