"""§5.1 — Quantile regression M1a на τ ∈ {0.10, 0.25, 0.50, 0.75, 0.90}.

Содержательная интуиция: cap structure делает зависимость salary ↔ stats
вогнутой (concave). На верхнем дециле упор в max contract → marginal PPG
менее ценен. На нижнем дециле — упор в minimum salary. Линейная регрессия
на conditional mean это сглаживает.

Cluster bootstrap SE по player_id (199 реплик, для скорости — для финальной
версии достаточно).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import BASIC_STATS, COMMON_STRUCT, DATA_CLEAN  # noqa: E402
from analysis_v1.utils_v1 import OUT_TABLES_V1, prep_for_models  # noqa: E402

warnings.filterwarnings("ignore")

TAUS = [0.10, 0.25, 0.50, 0.75, 0.90]
KEY_VARS = ["ppg", "age", "experience", "allstar", "undrafted",
            "post_cba_2017", "post_covid"]


def _cluster_bootstrap_qreg(y, X, tau, cluster_ids, n_boot=199, seed=42):
    """Cluster-by-player bootstrap SE для одного quantile fit."""
    rng = np.random.default_rng(seed)
    unique_clusters = np.unique(cluster_ids)
    coefs = []
    for b in range(n_boot):
        boot_clusters = rng.choice(unique_clusters,
                                    size=len(unique_clusters), replace=True)
        # Bool-mask по выбранным кластерам (с дубликатами).
        idx = []
        for c in boot_clusters:
            idx.extend(np.where(cluster_ids == c)[0].tolist())
        idx = np.array(idx)
        y_b = y[idx]
        X_b = X[idx]
        try:
            res = QuantReg(y_b, X_b).fit(q=tau, max_iter=200)
            coefs.append(np.asarray(res.params))
        except Exception:
            pass
    if not coefs:
        return np.full(X.shape[1], np.nan)
    return np.std(np.array(coefs), axis=0)


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)
    y = d["ln_salary"].astype(float).to_numpy()
    X = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT].astype(float))
    X_arr = X.to_numpy()
    cluster_ids = d["player_id"].to_numpy()

    print(f"Sample: {len(d)} player-seasons, fitting τ ∈ {TAUS}")

    results = {}
    for tau in TAUS:
        res = QuantReg(y, X_arr).fit(q=tau, max_iter=500)
        se_boot = _cluster_bootstrap_qreg(y, X_arr, tau, cluster_ids,
                                            n_boot=199, seed=42 + int(tau * 100))
        results[tau] = {
            "params": pd.Series(res.params, index=X.columns),
            "se":     pd.Series(se_boot, index=X.columns),
            "p":      pd.Series(2 * (1 - sm.stats.stattools.stats.norm.cdf(
                          np.abs(res.params / np.where(se_boot > 0, se_boot, np.nan))
                      )), index=X.columns),
            "nobs":   len(y),
        }
        print(f"  τ={tau:.2f}: ppg={results[tau]['params']['ppg']:.4f} "
              f"(SE={results[tau]['se']['ppg']:.4f})")

    # Build wide table: variable × τ
    rows = []
    for v in X.columns:
        row = {"variable": v}
        for tau in TAUS:
            b = results[tau]["params"][v]
            s = results[tau]["se"][v]
            p = results[tau]["p"][v]
            stars = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else ""))
            row[f"τ={tau:.2f}"] = f"{b:.4f}{stars}\n({s:.4f})"
        rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLES_V1 / "quantile_M1a.csv", index=False, encoding="utf-8")
    print(f"\nWrote {OUT_TABLES_V1 / 'quantile_M1a.csv'}")

    # Для фигуры — отдельный long-format
    long_rows = []
    for tau in TAUS:
        for v in KEY_VARS:
            if v in results[tau]["params"].index:
                long_rows.append({
                    "tau": tau,
                    "variable": v,
                    "beta": results[tau]["params"][v],
                    "se":   results[tau]["se"][v],
                })
    long_df = pd.DataFrame(long_rows)
    long_df.to_csv(OUT_TABLES_V1 / "quantile_M1a_long.csv", index=False)

    print("\nКлючевые регрессоры:")
    pivot = long_df.pivot(index="variable", columns="tau", values="beta")
    print(pivot.to_string())


if __name__ == "__main__":
    main()
