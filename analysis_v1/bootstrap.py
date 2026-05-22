"""§4.1 — Two-way clustering + wild cluster bootstrap для ключевых
коэффициентов.

V0 использовал только player-clustered SE (cluster_entity=True). С 9 годами
two-way clustering (player × season) даёт более консервативные SE, особенно
для year-variant регрессоров (post_cba_2017, post_covid).

Wild cluster bootstrap по player_id с Rademacher-весами (999 replications)
— альтернативная оценка p-value, не зависящая от асимптотических предпосылок.
Применяется к 4 ключевым коэффициентам:
    M1a post_cba_2017
    M2c state_tax_rate
    M3c_canonical cy_exogenous
    R1  contract_year
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_STRUCT, BASIC_STATS, DATA_CLEAN)
from analysis_v1.utils_v1 import (OUT_TABLES_V1, panel_index,  # noqa: E402
                                  prep_for_models)

warnings.filterwarnings("ignore")


def two_way_clustering(df: pd.DataFrame) -> pd.DataFrame:
    """Сравнение SE: cluster_entity vs cluster_entity+cluster_time."""
    rows = []

    # M1a baseline
    d = prep_for_models(df, restrict_single_team=False)
    d_idx = panel_index(d)
    y = d_idx["ln_salary"]
    X = sm.add_constant(d_idx[BASIC_STATS + COMMON_STRUCT])

    m_player = PooledOLS(y, X).fit(cov_type="clustered", cluster_entity=True)
    m_two    = PooledOLS(y, X).fit(cov_type="clustered",
                                    cluster_entity=True, cluster_time=True)
    for v in ["post_cba_2017", "post_covid", "age", "experience",
              "undrafted", "ppg"]:
        rows.append({
            "model": "M1a",
            "var": v,
            "β": m_player.params[v],
            "SE_player": m_player.std_errors[v],
            "SE_two_way": m_two.std_errors[v],
            "p_player": m_player.pvalues[v],
            "p_two_way": m_two.pvalues[v],
        })

    # M2c
    d2 = prep_for_models(df, restrict_single_team=True).dropna(
        subset=["state_tax_rate", "no_income_tax"]
    )
    d2_idx = panel_index(d2)
    X = sm.add_constant(d2_idx[COMBINED_STATS + COMMON_NO_STRUCT
                               + ["state_tax_rate"]])
    m_player = PanelOLS(d2_idx["ln_salary"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    m_two = PanelOLS(d2_idx["ln_salary"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True, cluster_time=True
    )
    for v in ["state_tax_rate", "vorp"]:
        rows.append({
            "model": "M2c",
            "var": v,
            "β": m_player.params[v],
            "SE_player": m_player.std_errors[v],
            "SE_two_way": m_two.std_errors[v],
            "p_player": m_player.pvalues[v],
            "p_two_way": m_two.pvalues[v],
        })

    # M3c_canonical
    d3 = d2.dropna(subset=["contract_year", "salary_next", "cy_exogenous"]).copy()
    d3["dln_salary"] = np.log(d3["salary_next"]) - d3["ln_salary"]
    d3_idx = d3.set_index(["player_id", "season"])
    X = sm.add_constant(d3_idx[COMBINED_STATS + COMMON_NO_STRUCT
                               + ["cy_exogenous"]])
    m_player = PanelOLS(d3_idx["dln_salary"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    m_two = PanelOLS(d3_idx["dln_salary"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True, cluster_time=True
    )
    rows.append({
        "model": "M3c_canonical",
        "var": "cy_exogenous",
        "β": m_player.params["cy_exogenous"],
        "SE_player": m_player.std_errors["cy_exogenous"],
        "SE_two_way": m_two.std_errors["cy_exogenous"],
        "p_player": m_player.pvalues["cy_exogenous"],
        "p_two_way": m_two.pvalues["cy_exogenous"],
    })

    # R1
    d_r1 = d2.dropna(subset=["contract_year"]).copy()
    d_r1["contract_year"] = d_r1["contract_year"].astype(int)
    d_r1_idx = panel_index(d_r1)
    X = sm.add_constant(d_r1_idx[COMBINED_STATS + COMMON_NO_STRUCT
                                  + ["no_income_tax", "contract_year"]])
    m_player = PanelOLS(d_r1_idx["ln_salary"], X, time_effects=True,
                         check_rank=False).fit(
        cov_type="clustered", cluster_entity=True
    )
    m_two = PanelOLS(d_r1_idx["ln_salary"], X, time_effects=True,
                      check_rank=False).fit(
        cov_type="clustered", cluster_entity=True, cluster_time=True
    )
    for v in ["contract_year", "no_income_tax"]:
        rows.append({
            "model": "R1",
            "var": v,
            "β": m_player.params[v],
            "SE_player": m_player.std_errors[v],
            "SE_two_way": m_two.std_errors[v],
            "p_player": m_player.pvalues[v],
            "p_two_way": m_two.pvalues[v],
        })

    out = pd.DataFrame(rows)
    out["SE_ratio (two_way/player)"] = out["SE_two_way"] / out["SE_player"]
    out.to_csv(OUT_TABLES_V1 / "two_way_clustering.csv", index=False)
    return out


def wild_cluster_bootstrap(
    y: np.ndarray,
    X: np.ndarray,
    cluster_ids: np.ndarray,
    test_col: int,
    n_boot: int = 999,
    seed: int = 42,
) -> dict:
    """Wild cluster bootstrap по `cluster_ids` с Rademacher-весами.

    Возвращает {'t_obs', 'p_boot_two_sided'}. Использует null-restricted
    DGP: y* = Xβ_null + ε̂ * w_g (где w_g ∈ {−1, +1}, общий для всех
    наблюдений кластера g).
    """
    n, k = X.shape
    rng = np.random.default_rng(seed)

    # Full OLS
    beta_full, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid_full = y - X @ beta_full
    # SE on full (homoskedastic — для t-stat normalization)
    sigma2 = (resid_full @ resid_full) / (n - k)
    XtX_inv = np.linalg.inv(X.T @ X)
    se_full = np.sqrt(sigma2 * np.diag(XtX_inv))
    t_obs = beta_full[test_col] / se_full[test_col]

    # Null-restricted: drop test_col
    keep = [i for i in range(k) if i != test_col]
    X_null = X[:, keep]
    beta_null, *_ = np.linalg.lstsq(X_null, y, rcond=None)
    y_null = X_null @ beta_null
    resid_null = y - y_null

    # Bootstrap
    unique_clusters = np.unique(cluster_ids)
    cluster_to_idx = {c: i for i, c in enumerate(unique_clusters)}
    cluster_idx_arr = np.array([cluster_to_idx[c] for c in cluster_ids])
    n_clusters = len(unique_clusters)

    t_boots = np.empty(n_boot)
    for b in range(n_boot):
        w = rng.choice([-1.0, 1.0], size=n_clusters)
        w_per_obs = w[cluster_idx_arr]
        y_b = y_null + resid_null * w_per_obs
        beta_b, *_ = np.linalg.lstsq(X, y_b, rcond=None)
        resid_b = y_b - X @ beta_b
        sigma2_b = (resid_b @ resid_b) / (n - k)
        se_b = np.sqrt(sigma2_b * np.diag(XtX_inv))
        t_boots[b] = beta_b[test_col] / se_b[test_col]

    p_two = float(np.mean(np.abs(t_boots) >= np.abs(t_obs)))
    return {
        "beta": beta_full[test_col],
        "t_obs": float(t_obs),
        "p_boot_two_sided": p_two,
        "p_analytic_homosk": float(2 * (1 - sm.stats.stattools.stats.t.cdf(
            abs(t_obs), df=n - k))) if False else None,
    }


def run_wild_bootstrap(df: pd.DataFrame, n_boot: int = 999) -> pd.DataFrame:
    """Wild cluster bootstrap на 4 ключевых коэффициентах."""
    rows = []

    # M1a post_cba_2017 (full sample)
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)
    X = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT]).astype(float)
    cols = X.columns.tolist()
    test_idx = cols.index("post_cba_2017")
    res = wild_cluster_bootstrap(
        d["ln_salary"].to_numpy(), X.to_numpy(),
        d["player_id"].to_numpy(), test_idx, n_boot=n_boot,
    )
    rows.append({"model": "M1a", "var": "post_cba_2017", **res})

    # M2c state_tax_rate (single-team + tax matched).
    # Используем pooled OLS с year-dummies вместо PanelOLS — для wild cluster
    # достаточно линейного OLS с dummy-кодированием year FE.
    d2 = prep_for_models(df, restrict_single_team=True).dropna(
        subset=["state_tax_rate", "no_income_tax"]
    ).reset_index(drop=True)
    year_dummies = pd.get_dummies(d2["season"], prefix="yr", drop_first=True)
    X2 = pd.concat([
        sm.add_constant(d2[COMBINED_STATS + COMMON_NO_STRUCT
                            + ["state_tax_rate"]].astype(float)),
        year_dummies.astype(float),
    ], axis=1)
    test_idx2 = X2.columns.tolist().index("state_tax_rate")
    res2 = wild_cluster_bootstrap(
        d2["ln_salary"].to_numpy(), X2.to_numpy(),
        d2["player_id"].to_numpy(), test_idx2, n_boot=n_boot,
    )
    rows.append({"model": "M2c", "var": "state_tax_rate", **res2})

    # M3c_canonical cy_exogenous (Δlog_salary sample)
    d3 = d2.dropna(subset=["contract_year", "salary_next", "cy_exogenous"]).copy()
    d3["dln_salary"] = np.log(d3["salary_next"]) - d3["ln_salary"]
    d3 = d3.reset_index(drop=True)
    yr3 = pd.get_dummies(d3["season"], prefix="yr", drop_first=True)
    X3 = pd.concat([
        sm.add_constant(d3[COMBINED_STATS + COMMON_NO_STRUCT
                            + ["cy_exogenous"]].astype(float)),
        yr3.astype(float),
    ], axis=1)
    test_idx3 = X3.columns.tolist().index("cy_exogenous")
    res3 = wild_cluster_bootstrap(
        d3["dln_salary"].to_numpy(), X3.to_numpy(),
        d3["player_id"].to_numpy(), test_idx3, n_boot=n_boot,
    )
    rows.append({"model": "M3c_canonical", "var": "cy_exogenous", **res3})

    # R1 contract_year (with no_income_tax)
    d_r1 = d2.dropna(subset=["contract_year"]).copy()
    d_r1["contract_year"] = d_r1["contract_year"].astype(int)
    d_r1 = d_r1.reset_index(drop=True)
    yr_r1 = pd.get_dummies(d_r1["season"], prefix="yr", drop_first=True)
    X_r1 = pd.concat([
        sm.add_constant(d_r1[COMBINED_STATS + COMMON_NO_STRUCT
                              + ["no_income_tax", "contract_year"]].astype(float)),
        yr_r1.astype(float),
    ], axis=1)
    test_idx_r1 = X_r1.columns.tolist().index("contract_year")
    res_r1 = wild_cluster_bootstrap(
        d_r1["ln_salary"].to_numpy(), X_r1.to_numpy(),
        d_r1["player_id"].to_numpy(), test_idx_r1, n_boot=n_boot,
    )
    rows.append({"model": "R1", "var": "contract_year", **res_r1})

    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLES_V1 / "wild_bootstrap_pvalues.csv", index=False)
    return out


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")

    print("=" * 72)
    print("§4.1a — Two-way clustering (player × season)")
    print("=" * 72)
    tw = two_way_clustering(df)
    with pd.option_context("display.float_format", "{:.4f}".format,
                            "display.width", 200):
        print(tw.to_string(index=False))

    print("\n" + "=" * 72)
    print("§4.1b — Wild cluster bootstrap (player, Rademacher, 999 reps)")
    print("=" * 72)
    wb = run_wild_bootstrap(df, n_boot=999)
    with pd.option_context("display.float_format", "{:.4f}".format,
                            "display.width", 200):
        print(wb.to_string(index=False))


if __name__ == "__main__":
    main()
