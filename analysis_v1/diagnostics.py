"""§2.1 + §4.2 + §4.3 + §4.4 + §4.5 + §4.6 — диагностики V1.

Содержит:
    §2.1  VIF table для M1c (multicollinearity check)
    §4.2  Breusch-Pagan / White тесты на гетероскедастичность
    §4.3  Power analysis (MDE для null-результатов)
    §4.4  FDR-correction (Benjamini-Hochberg) для ключевых p-values
    §4.5  Influence diagnostics (Cook's distance, leverage)
    §4.6  Sample attrition по шагам обработки

Все таблицы → output/tables_v1/.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import (BASIC_STATS, COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_STRUCT, DATA_CLEAN)
from analysis_v1.utils_v1 import (OUT_TABLES_V1, panel_index,  # noqa: E402
                                  prep_for_models)

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────────
# §2.1 VIF
# ─────────────────────────────────────────────────────────────────────────
def vif_table(X: pd.DataFrame, name: str) -> pd.DataFrame:
    """VIF для каждого столбца X (без константы)."""
    cols = [c for c in X.columns if c != "const"]
    rows = []
    Xn = X[cols].to_numpy(dtype=float)
    for i, c in enumerate(cols):
        vif = variance_inflation_factor(Xn, i)
        rows.append({"variable": c, "VIF": vif})
    out = pd.DataFrame(rows).sort_values("VIF", ascending=False)
    out.to_csv(OUT_TABLES_V1 / f"vif_{name}.csv", index=False)
    return out


# ─────────────────────────────────────────────────────────────────────────
# §4.2 Heteroskedasticity tests
# ─────────────────────────────────────────────────────────────────────────
def heteroskedasticity_tests(fits: dict[str, tuple]) -> pd.DataFrame:
    """BP + White на residuals каждой модели.

    fits — dict{label: (residuals, X_with_const)}.
    """
    rows = []
    for label, (resid, X) in fits.items():
        Xn = X.to_numpy(dtype=float)
        r = np.asarray(resid, dtype=float)
        bp_stat, bp_p, _, _ = het_breuschpagan(r, Xn)
        try:
            w_stat, w_p, _, _ = het_white(r, Xn)
        except Exception:
            w_stat, w_p = np.nan, np.nan
        rows.append({"model": label, "BP_stat": bp_stat, "BP_p": bp_p,
                     "White_stat": w_stat, "White_p": w_p,
                     "reject_homosked_5%": "yes" if bp_p < 0.05 else "no"})
    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLES_V1 / "heteroskedasticity_tests.csv", index=False)
    return out


# ─────────────────────────────────────────────────────────────────────────
# §4.3 Power analysis (MDE at 80%)
# ─────────────────────────────────────────────────────────────────────────
def power_analysis(coef_rows: list[dict]) -> pd.DataFrame:
    """MDE = 2.8 × SE для каждого null-кандидата."""
    out_rows = []
    for r in coef_rows:
        se = r["SE"]
        mde = 2.8 * se
        # Перевод в экономическую интерпретацию для continuous variables.
        scale = r.get("scale_note", "—")
        out_rows.append({
            "model": r["model"],
            "variable": r["var"],
            "β": r["beta"],
            "SE": se,
            "p": r["p"],
            "MDE_β (power=0.80)": mde,
            "interpretation": scale,
            "plausibility": r.get("plausibility", ""),
        })
    out = pd.DataFrame(out_rows)
    out.to_csv(OUT_TABLES_V1 / "power_analysis.csv", index=False)
    return out


# ─────────────────────────────────────────────────────────────────────────
# §4.4 FDR (Benjamini-Hochberg)
# ─────────────────────────────────────────────────────────────────────────
def fdr_correction(test_rows: list[dict]) -> pd.DataFrame:
    """test_rows = [{model, var, raw_p}, ...] → BH-adjusted."""
    df = pd.DataFrame(test_rows)
    rejected, p_adj, _, _ = multipletests(df["raw_p"].values, method="fdr_bh")
    df["adj_p_BH"] = p_adj
    df["reject_raw_5%"] = (df["raw_p"] < 0.05).astype(int)
    df["reject_BH_5%"]  = rejected.astype(int)
    df.to_csv(OUT_TABLES_V1 / "multiple_testing.csv", index=False)
    return df


# ─────────────────────────────────────────────────────────────────────────
# §4.5 Influence diagnostics
# ─────────────────────────────────────────────────────────────────────────
def influence_diagnostics(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Cook's distance + hat_diag для M1a (pooled OLS, statsmodels)."""
    cols = BASIC_STATS + COMMON_STRUCT
    X = sm.add_constant(d[cols].astype(float))
    y = d["ln_salary"].astype(float)
    ols = sm.OLS(y, X).fit()
    infl = ols.get_influence()
    cd = infl.cooks_distance[0]
    hat = infl.hat_matrix_diag
    diag = d[["player_id", "player_name", "season", "team_abbr",
              "salary_usd"]].copy()
    diag["cooks_d"] = cd
    diag["hat"] = hat
    top = diag.nlargest(10, "cooks_d")
    top.to_csv(OUT_TABLES_V1 / "top_influential.csv", index=False)

    # Re-fit без top-10
    top_idx = set(top.index)
    keep = ~d.index.isin(top_idx)
    X2 = sm.add_constant(d.loc[keep, cols].astype(float))
    y2 = d.loc[keep, "ln_salary"].astype(float)
    ols2 = sm.OLS(y2, X2).fit()

    # Сравнение коэффициентов
    comp_rows = []
    for v in cols + ["const"]:
        if v in ols.params.index and v in ols2.params.index:
            comp_rows.append({
                "variable": v,
                "β_full":     ols.params[v],
                "β_no_top10": ols2.params[v],
                "Δβ":         ols2.params[v] - ols.params[v],
                "pct_change": (ols2.params[v] - ols.params[v]) / abs(ols.params[v]) * 100
                              if ols.params[v] != 0 else np.nan,
            })
    comp = pd.DataFrame(comp_rows)
    comp.to_csv(OUT_TABLES_V1 / "M1a_no_outliers_comparison.csv", index=False)
    return top, {"M1a_full": ols, "M1a_no_top10": ols2, "comp": comp}


# ─────────────────────────────────────────────────────────────────────────
# §4.6 Sample attrition
# ─────────────────────────────────────────────────────────────────────────
def sample_attrition(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n_start = len(df)
    rows.append({"stage": "0. data_merged loaded", "N": n_start, "dropped": 0})

    n_single = (~df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])).sum()
    rows.append({"stage": "1. single-team only", "N": int(n_single),
                 "dropped": n_start - n_single})

    must_have = ["ln_salary", "ppg", "rpg", "apg", "age", "age_sq", "experience",
                 "post_cba_2017", "post_covid", "allstar", "undrafted",
                 "log_draft_pick", "pos_PG", "pos_SG", "pos_SF", "pos_PF",
                 "mpg", "gp", "per", "ws", "bpm", "vorp", "usg_pct"]
    d_single = df[~df["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])]
    n_full_reg = d_single.dropna(subset=must_have).shape[0]
    rows.append({"stage": "2. + dropna in regressors (M2 base)", "N": n_full_reg,
                 "dropped": int(n_single) - n_full_reg})

    d_m2 = d_single.dropna(subset=must_have).dropna(
        subset=["state_tax_rate", "no_income_tax"]
    )
    rows.append({"stage": "3. + tax matched (M2 final)", "N": len(d_m2),
                 "dropped": n_full_reg - len(d_m2)})

    d_m3 = d_m2.dropna(subset=["contract_year"])
    rows.append({"stage": "4. + contract_year observed (M3a)", "N": len(d_m3),
                 "dropped": len(d_m2) - len(d_m3)})

    d_m3c = d_m3.dropna(subset=["salary_next"])
    rows.append({"stage": "5. + salary_next observed (M3c)", "N": len(d_m3c),
                 "dropped": len(d_m3) - len(d_m3c)})

    d_m3can = d_m3c.dropna(subset=["cy_exogenous"])
    rows.append({"stage": "6. + cy_exogenous observed (M3c_canonical)",
                 "N": len(d_m3can), "dropped": len(d_m3c) - len(d_m3can)})

    out = pd.DataFrame(rows)
    out.to_csv(OUT_TABLES_V1 / "sample_attrition.csv", index=False)
    return out


# ─────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")
    d = prep_for_models(df, restrict_single_team=False)

    print("\n" + "=" * 72)
    print("§2.1 — VIF table (M1c, combined stats + year FE controls)")
    print("=" * 72)
    d_idx = panel_index(d)
    X_M1c = sm.add_constant(d_idx[COMBINED_STATS + COMMON_NO_STRUCT])
    vif_M1c = vif_table(X_M1c, "M1c")
    print(vif_M1c.to_string(index=False))

    # VIF также для M1a (basic)
    X_M1a = sm.add_constant(d_idx[BASIC_STATS + COMMON_STRUCT])
    vif_M1a = vif_table(X_M1a, "M1a")
    print(f"\nM1a max VIF: {vif_M1a['VIF'].max():.2f}")

    print("\n" + "=" * 72)
    print("§4.2 — Heteroskedasticity tests")
    print("=" * 72)
    # Refit моделей для residuals (linearmodels-friendly)
    y = d_idx["ln_salary"]
    m1a_fit = PooledOLS(y, X_M1a).fit(cov_type="clustered", cluster_entity=True)
    m1c_fit = PanelOLS(y, X_M1c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    # M2c — на M2 sample
    d_m2 = prep_for_models(df, restrict_single_team=True).dropna(
        subset=["state_tax_rate", "no_income_tax"]
    )
    d_m2_idx = panel_index(d_m2)
    X_M2c = sm.add_constant(d_m2_idx[COMBINED_STATS + COMMON_NO_STRUCT
                                     + ["state_tax_rate"]])
    m2c_fit = PanelOLS(d_m2_idx["ln_salary"], X_M2c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    X_M2b = sm.add_constant(d_m2_idx[COMBINED_STATS + COMMON_NO_STRUCT
                                     + ["no_income_tax"]])
    m2b_fit = PanelOLS(d_m2_idx["ln_salary"], X_M2b, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    # M3c_canonical — на M3 Δ sample с cy_exogenous
    d_m3 = d_m2.dropna(subset=["contract_year", "salary_next", "cy_exogenous"]).copy()
    d_m3["dln_salary"] = np.log(d_m3["salary_next"]) - d_m3["ln_salary"]
    d_m3_idx = d_m3.set_index(["player_id", "season"])
    X_M3can = sm.add_constant(
        d_m3_idx[COMBINED_STATS + COMMON_NO_STRUCT + ["cy_exogenous"]]
    )
    m3can_fit = PanelOLS(d_m3_idx["dln_salary"], X_M3can, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )

    het = heteroskedasticity_tests({
        "M1a": (m1a_fit.resids, X_M1a),
        "M1c": (m1c_fit.resids, X_M1c),
        "M2c": (m2c_fit.resids, X_M2c),
        "M3c_canonical": (m3can_fit.resids, X_M3can),
    })
    print(het.to_string(index=False))

    print("\n" + "=" * 72)
    print("§4.3 — Power analysis")
    print("=" * 72)
    pa = power_analysis([
        {"model": "M1a", "var": "allstar",
         "beta": m1a_fit.params["allstar"],
         "SE": m1a_fit.std_errors["allstar"],
         "p": m1a_fit.pvalues["allstar"],
         "scale_note": "MDE × 1 = wage premium от All-Star",
         "plausibility": "Marginal: 17% wage premium может быть реален, но мы не детектируем"},
        {"model": "M2c", "var": "state_tax_rate",
         "beta": m2c_fit.params["state_tax_rate"],
         "SE": m2c_fit.std_errors["state_tax_rate"],
         "p": m2c_fit.pvalues["state_tax_rate"],
         "scale_note": "MDE × 0.535 (TX→CAN) = pre-tax wage shift",
         "plausibility": "Detectable: 21% pre-tax compensation за tax 0→53.5%"},
        {"model": "M2b", "var": "no_income_tax",
         "beta": m2b_fit.params["no_income_tax"],
         "SE":   m2b_fit.std_errors["no_income_tax"],
         "p":    m2b_fit.pvalues["no_income_tax"],
         "scale_note": "MDE = wage premium for tax-free state",
         "plausibility": "Detectable: 11% wage premium"},
        {"model": "M3c_canonical", "var": "cy_exogenous",
         "beta": m3can_fit.params["cy_exogenous"],
         "SE": m3can_fit.std_errors["cy_exogenous"],
         "p": m3can_fit.pvalues["cy_exogenous"],
         "scale_note": "MDE = Δlog_salary за контрактный год",
         "plausibility": "Tight: даже 7% бамп исключён → честный null"},
    ])
    print(pa.to_string(index=False))

    print("\n" + "=" * 72)
    print("§4.4 — FDR-correction")
    print("=" * 72)
    # Собираем ключевые p-values из главных моделей.
    tests = []

    def add_from(label, model, vars_):
        for v in vars_:
            if v in model.pvalues.index:
                tests.append({"model": label, "var": v,
                              "raw_p": float(model.pvalues[v])})

    add_from("M1a", m1a_fit,
             ["post_cba_2017", "post_covid", "ppg", "age",
              "experience", "undrafted", "allstar"])
    add_from("M1c", m1c_fit, ["vorp", "usg_pct", "per", "ws"])
    add_from("M2c", m2c_fit, ["state_tax_rate"])
    add_from("M3c_canonical", m3can_fit, ["cy_exogenous"])
    fdr = fdr_correction(tests)
    print(fdr.to_string(index=False))

    print("\n" + "=" * 72)
    print("§4.5 — Influence diagnostics (Cook's distance, M1a)")
    print("=" * 72)
    top, infl_out = influence_diagnostics(d.reset_index(drop=True))
    print("Top-10 most influential (Cook's distance):")
    print(top[["player_name", "season", "team_abbr", "salary_usd",
               "cooks_d", "hat"]].to_string(index=False))
    print("\nКоэффициенты ключевых регрессоров: full vs без top-10")
    key = ["ppg", "age", "experience", "undrafted", "allstar",
           "post_cba_2017", "post_covid"]
    print(infl_out["comp"][infl_out["comp"]["variable"].isin(key)].to_string(index=False))

    print("\n" + "=" * 72)
    print("§4.6 — Sample attrition")
    print("=" * 72)
    att = sample_attrition(df)
    print(att.to_string(index=False))


if __name__ == "__main__":
    main()
