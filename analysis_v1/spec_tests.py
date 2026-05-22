"""§5.3 — Specification tests: F-test poolability (year FE joint), F-test
player FE joint, Hausman-style сравнение FE vs RE.

Для бакалаврского уровня — три минимальных диагностики:
    1. F-test: year FE = 0 (в pooled OLS).
    2. F-test: player FE = 0 (в pooled vs within).
    3. Comparison FE vs RE (если RE доступна).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (BASIC_STATS, COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_STRUCT, DATA_CLEAN)
from analysis_v1.utils_v1 import OUT_TABLES_V1, prep_for_models  # noqa: E402

warnings.filterwarnings("ignore")


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")
    d = prep_for_models(df, restrict_single_team=False).reset_index(drop=True)

    print("=" * 72)
    print("§5.3 — Specification tests (M1)")
    print("=" * 72)

    rows = []

    # ── Test 1: F-test year FE = 0 ──────────────────────────────────────
    # Restricted (pooled, без year FE): M1a baseline
    X_rest = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT].astype(float))
    y = d["ln_salary"].astype(float)
    ols_rest = sm.OLS(y, X_rest).fit()

    # Unrestricted: + year dummies (8 dummies для 9 лет)
    year_dum = pd.get_dummies(d["season"], prefix="yr", drop_first=True).astype(float)
    # Drop post_cba/post_covid, чтобы избежать collinearity с year-dummies
    X_full = pd.concat([
        sm.add_constant(d[BASIC_STATS + [c for c in COMMON_STRUCT
                                          if c not in ("post_cba_2017", "post_covid")]
                          ].astype(float)),
        year_dum,
    ], axis=1)
    ols_full = sm.OLS(y, X_full).fit()

    # F-test: ssr_rest vs ssr_full
    df_diff = X_full.shape[1] - X_rest.shape[1]
    f_stat = ((ols_rest.ssr - ols_full.ssr) / df_diff) / (
        ols_full.ssr / ols_full.df_resid
    )
    f_p = 1 - sm.stats.stattools.stats.f.cdf(f_stat,
                                              df_diff, ols_full.df_resid)
    rows.append({
        "test": "Year FE jointly = 0 (M1)",
        "F": f_stat, "df_num": df_diff, "df_den": int(ols_full.df_resid),
        "p_value": f_p,
        "conclusion": "Reject — нужны year FE" if f_p < 0.05 else "Не отвергнуть",
    })
    print(f"1. Year FE F-test: F({df_diff}, {int(ols_full.df_resid)}) = {f_stat:.2f}, p = {f_p:.4f}")

    # ── Test 2: F-test player FE = 0 ────────────────────────────────────
    # Используем within transformation. Если within-R² значимо > 0 — FE нужны.
    # F = ((RSS_pooled − RSS_within) / (n_players − 1)) / (RSS_within / (n − n_players − k))
    n = len(d)
    n_players = d["player_id"].nunique()

    # Demean by player_id
    d_dem = d.copy()
    for c in BASIC_STATS + COMMON_STRUCT + ["ln_salary"]:
        d_dem[c] = d[c] - d.groupby("player_id")[c].transform("mean")
    X_w = d_dem[BASIC_STATS + COMMON_STRUCT].astype(float).to_numpy()
    y_w = d_dem["ln_salary"].astype(float).to_numpy()
    # Within OLS (no constant since demeaned)
    beta_w, *_ = np.linalg.lstsq(X_w, y_w, rcond=None)
    rss_w = float(np.sum((y_w - X_w @ beta_w) ** 2))

    # Pooled RSS (with constant)
    rss_p = float(ols_rest.ssr)
    k = X_w.shape[1]
    df_num = n_players - 1
    df_den = n - n_players - k
    f_stat_pl = ((rss_p - rss_w) / df_num) / (rss_w / df_den)
    f_p_pl = 1 - sm.stats.stattools.stats.f.cdf(f_stat_pl, df_num, df_den)
    rows.append({
        "test": f"Player FE jointly = 0 (M1, {n_players} players)",
        "F": f_stat_pl, "df_num": df_num, "df_den": df_den,
        "p_value": f_p_pl,
        "conclusion": "Reject — нужны player FE" if f_p_pl < 0.05 else "Не отвергнуть",
    })
    print(f"2. Player FE F-test: F({df_num}, {df_den}) = {f_stat_pl:.2f}, p = {f_p_pl:.4f}")

    # ── Test 3: Joint year-FE F-test для M2c sample ─────────────────────
    d2 = prep_for_models(df, restrict_single_team=True).dropna(
        subset=["state_tax_rate", "no_income_tax"]
    ).reset_index(drop=True)
    X_rest2 = sm.add_constant(
        d2[COMBINED_STATS + COMMON_NO_STRUCT + ["state_tax_rate"]].astype(float)
    )
    y2 = d2["ln_salary"].astype(float)
    ols_rest2 = sm.OLS(y2, X_rest2).fit()
    year_dum2 = pd.get_dummies(d2["season"], prefix="yr", drop_first=True).astype(float)
    X_full2 = pd.concat([X_rest2, year_dum2], axis=1)
    ols_full2 = sm.OLS(y2, X_full2).fit()
    df_diff2 = X_full2.shape[1] - X_rest2.shape[1]
    f_stat2 = ((ols_rest2.ssr - ols_full2.ssr) / df_diff2) / (
        ols_full2.ssr / ols_full2.df_resid
    )
    f_p2 = 1 - sm.stats.stattools.stats.f.cdf(f_stat2, df_diff2, ols_full2.df_resid)
    rows.append({
        "test": "Year FE jointly = 0 (M2c)",
        "F": f_stat2, "df_num": df_diff2, "df_den": int(ols_full2.df_resid),
        "p_value": f_p2,
        "conclusion": "Reject — нужны year FE" if f_p2 < 0.05 else "Не отвергнуть",
    })
    print(f"3. Year FE F-test (M2c): F({df_diff2}, {int(ols_full2.df_resid)}) = {f_stat2:.2f}, p = {f_p2:.4f}")

    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLES_V1 / "specification_tests.csv", index=False)
    print(f"\nWrote {OUT_TABLES_V1 / 'specification_tests.csv'}")


if __name__ == "__main__":
    main()
