"""§2.1 + §2.3 + §2.4 + §2.5 + §2.6 + §2.7 + §2.8 + §2.9 — альтернативные
спецификации M1.

Все варианты сохраняются как отдельные .txt + сводка alt_M1_comparison.csv.

    §2.1  M1c_minimal      — VORP + USG% вместо PER + WS + VORP + USG%
                             (фикс VIF: per VIF=67, ws VIF=39).
    §2.3  M1a_per36        — ppg_per36, rpg_per36 и т.д. (фикс эндогенности
                             stats↔minutes — B4).
    §2.4  M1a_age_only     — без experience.
          M1a_exp_only     — без age, age² (используем experience, experience²).
    §2.5  M1a_ts_only      — ts_pct вместо fg_pct/fg3_pct/ft_pct.
    §2.6  M1a_cap_share    — DV = ln(salary/cap_t) вместо ln(salary).
    §2.7  M1a_pg_ref       — PG как position reference, C — отдельный дамми.
    §2.8  M1a_multihot     — multi-position dummies (SG-SF → is_SG=1, is_SF=1).
    §2.9  M1a_cba_inter    — interactions ppg × post_cba, mpg × post_cba.
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
from analysis.config import (BASIC_STATS, COMBINED_STATS, COMMON_NO_STRUCT,  # noqa: E402
                             COMMON_STRUCT, DATA_CLEAN)
from analysis_v1.utils_v1 import (OUT_TABLES_V1, combine_models,  # noqa: E402
                                  panel_index, prep_for_models, save_summary)

warnings.filterwarnings("ignore")


COMBINED_MINIMAL = ["ppg", "rpg", "apg", "mpg", "gp", "vorp", "usg_pct"]


def _fit_pooled(y, X):
    return PooledOLS(y, X).fit(cov_type="clustered", cluster_entity=True)


def _fit_year_fe(y, X):
    return PanelOLS(y, X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")
    d = prep_for_models(df, restrict_single_team=False).copy()
    d_idx = panel_index(d)
    y = d_idx["ln_salary"]
    print(f"Sample (full): {len(d_idx)} player-seasons\n")

    results: dict[str, object] = {}

    # ── §2.1 M1c_minimal ────────────────────────────────────────────────
    X = sm.add_constant(d_idx[COMBINED_MINIMAL + COMMON_NO_STRUCT])
    m1c_min = _fit_year_fe(y, X)
    save_summary(m1c_min, "M1c_minimal_vorp_usg")
    results["M1c_minimal"] = m1c_min
    print(f"§2.1 M1c_minimal:    R²={m1c_min.rsquared:.4f}, "
          f"VORP={m1c_min.params['vorp']:.4f} (p={m1c_min.pvalues['vorp']:.4f})")

    # ── §2.3 M1a_per36 ──────────────────────────────────────────────────
    d_p36 = d.copy()
    for col in ["ppg", "rpg", "apg", "spg", "bpg"]:
        d_p36[f"{col}_per36"] = np.where(d_p36["mpg"] > 0,
                                         d_p36[col] * 36 / d_p36["mpg"], 0)
    PER36_STATS = ["ppg_per36", "rpg_per36", "apg_per36", "spg_per36",
                   "bpg_per36", "mpg", "gp", "fg_pct", "fg3_pct", "ft_pct"]
    d_p36_idx = panel_index(d_p36)
    X = sm.add_constant(d_p36_idx[PER36_STATS + COMMON_STRUCT])
    m1a_p36 = _fit_pooled(d_p36_idx["ln_salary"], X)
    save_summary(m1a_p36, "M1a_per36")
    results["M1a_per36"] = m1a_p36
    print(f"§2.3 M1a_per36:      R²={m1a_p36.rsquared:.4f}, "
          f"ppg_per36={m1a_p36.params['ppg_per36']:.4f} "
          f"(p={m1a_p36.pvalues['ppg_per36']:.4f})")

    # ── §2.4 M1a_age_only / M1a_exp_only ────────────────────────────────
    common_no_exp = [c for c in COMMON_STRUCT if c not in ("experience",)]
    X = sm.add_constant(d_idx[BASIC_STATS + common_no_exp])
    m1a_age_only = _fit_pooled(y, X)
    save_summary(m1a_age_only, "M1a_age_only")
    results["M1a_age_only"] = m1a_age_only

    common_no_age = [c for c in COMMON_STRUCT if c not in ("age", "age_sq")]
    d_exp = d.copy()
    d_exp["experience_sq"] = d_exp["experience"] ** 2
    d_exp_idx = panel_index(d_exp)
    X = sm.add_constant(d_exp_idx[BASIC_STATS + common_no_age + ["experience_sq"]])
    m1a_exp_only = _fit_pooled(d_exp_idx["ln_salary"], X)
    save_summary(m1a_exp_only, "M1a_exp_only")
    results["M1a_exp_only"] = m1a_exp_only

    # Implied peak возраста для каждой модели
    def _peak_age(model):
        if "age" in model.params.index and "age_sq" in model.params.index:
            b = model.params["age"]
            c = model.params["age_sq"]
            return -b / (2 * c) if c != 0 else np.nan
        return np.nan

    def _peak_exp(model):
        if "experience" in model.params.index and "experience_sq" in model.params.index:
            b = model.params["experience"]
            c = model.params["experience_sq"]
            return -b / (2 * c) if c != 0 else np.nan
        return np.nan

    # Перезапуск baseline M1a (age + exp), чтобы взять peak.
    X_base = sm.add_constant(d_idx[BASIC_STATS + COMMON_STRUCT])
    m1a_baseline = _fit_pooled(y, X_base)

    peak_rows = [
        {"model": "M1a_baseline (age + exp)",
         "age_peak": _peak_age(m1a_baseline),
         "exp_peak": "—"},
        {"model": "M1a_age_only (без exp)",
         "age_peak": _peak_age(m1a_age_only),
         "exp_peak": "—"},
        {"model": "M1a_exp_only (без age)",
         "age_peak": "—",
         "exp_peak": _peak_exp(m1a_exp_only)},
    ]
    pd.DataFrame(peak_rows).to_csv(OUT_TABLES_V1 / "age_peak_comparison.csv",
                                   index=False)
    print(f"§2.4 age_peak baseline (age+exp): {_peak_age(m1a_baseline):.2f}")
    print(f"     age_peak age_only:           {_peak_age(m1a_age_only):.2f}")
    print(f"     exp_peak exp_only:           {_peak_exp(m1a_exp_only):.2f}")

    # ── §2.5 M1a_ts_only ────────────────────────────────────────────────
    basic_ts = [c if c not in ("fg_pct", "fg3_pct", "ft_pct") else None
                for c in BASIC_STATS]
    basic_ts = [c for c in basic_ts if c is not None] + ["ts_pct"]
    X = sm.add_constant(d_idx[basic_ts + COMMON_STRUCT])
    m1a_ts = _fit_pooled(y, X)
    save_summary(m1a_ts, "M1a_ts_only")
    results["M1a_ts_only"] = m1a_ts
    print(f"§2.5 M1a_ts_only:    R²={m1a_ts.rsquared:.4f}, "
          f"ts_pct={m1a_ts.params['ts_pct']:.4f} "
          f"(p={m1a_ts.pvalues['ts_pct']:.4f})")

    # ── §2.6 M1a_cap_share ──────────────────────────────────────────────
    d_cap = d.copy()
    # cap_t уже есть в data_analysis_v1.csv (из contract_year_v1).
    d_cap["ln_cap_share"] = np.log(d_cap["salary_usd"] / d_cap["cap_t"])
    d_cap_idx = panel_index(d_cap)
    X = sm.add_constant(d_cap_idx[BASIC_STATS + COMMON_STRUCT])
    m1a_cap = _fit_pooled(d_cap_idx["ln_cap_share"], X)
    save_summary(m1a_cap, "M1a_cap_share")
    results["M1a_cap_share"] = m1a_cap
    print(f"§2.6 M1a_cap_share:  R²={m1a_cap.rsquared:.4f}, "
          f"post_cba={m1a_cap.params['post_cba_2017']:.4f} "
          f"(p={m1a_cap.pvalues['post_cba_2017']:.4f})  "
          f"[ожидается ↓ vs baseline]")

    X = sm.add_constant(d_cap_idx[BASIC_STATS + COMMON_NO_STRUCT])
    m1b_cap = _fit_year_fe(d_cap_idx["ln_cap_share"], X)
    save_summary(m1b_cap, "M1b_cap_share")
    results["M1b_cap_share"] = m1b_cap

    # ── §2.7 M1a_pg_ref ─────────────────────────────────────────────────
    d_pg = d.copy()
    for p in ["SG", "SF", "PF", "C"]:
        d_pg[f"pos_{p}"] = (d_pg["position_main"] == p).astype(int)
    common_pg = [c if c != "pos_PG" else None for c in COMMON_STRUCT]
    common_pg = [c for c in common_pg if c is not None] + ["pos_C"]
    d_pg_idx = panel_index(d_pg)
    X = sm.add_constant(d_pg_idx[BASIC_STATS + common_pg])
    m1a_pg = _fit_pooled(d_pg_idx["ln_salary"], X)
    save_summary(m1a_pg, "M1a_pg_ref")
    results["M1a_pg_ref"] = m1a_pg
    print(f"§2.7 M1a_pg_ref:     R²={m1a_pg.rsquared:.4f}")

    # ── §2.8 M1a_multihot ───────────────────────────────────────────────
    d_mh = d.copy()
    for p in ["PG", "SG", "SF", "PF", "C"]:
        d_mh[f"is_{p}"] = d_mh["position"].fillna("").str.contains(p).astype(int)
    common_mh = [c for c in COMMON_STRUCT if not c.startswith("pos_")]
    common_mh = common_mh + ["is_SG", "is_SF", "is_PF", "is_C"]
    d_mh_idx = panel_index(d_mh)
    X = sm.add_constant(d_mh_idx[BASIC_STATS + common_mh])
    m1a_mh = _fit_pooled(d_mh_idx["ln_salary"], X)
    save_summary(m1a_mh, "M1a_multihot")
    results["M1a_multihot"] = m1a_mh
    print(f"§2.8 M1a_multihot:   R²={m1a_mh.rsquared:.4f}")

    # ── §2.9 M1a_cba_inter ──────────────────────────────────────────────
    d_in = d.copy()
    d_in["ppg_x_postcba"] = d_in["ppg"] * d_in["post_cba_2017"]
    d_in["mpg_x_postcba"] = d_in["mpg"] * d_in["post_cba_2017"]
    d_in_idx = panel_index(d_in)
    X = sm.add_constant(d_in_idx[BASIC_STATS + COMMON_STRUCT
                                 + ["ppg_x_postcba", "mpg_x_postcba"]])
    m1a_in = _fit_pooled(d_in_idx["ln_salary"], X)
    save_summary(m1a_in, "M1a_cba_interactions")
    results["M1a_cba_inter"] = m1a_in
    print(f"§2.9 M1a_cba_inter:  R²={m1a_in.rsquared:.4f}, "
          f"ppg×postcba={m1a_in.params['ppg_x_postcba']:.4f} "
          f"(p={m1a_in.pvalues['ppg_x_postcba']:.4f})")

    # ── Сводка ──────────────────────────────────────────────────────────
    combine_models(
        {"M1a_baseline": m1a_baseline,
         "M1c_minimal (VORP+USG only)": m1c_min,
         "M1a_per36": m1a_p36,
         "M1a_age_only": m1a_age_only,
         "M1a_exp_only": m1a_exp_only,
         "M1a_ts_only": m1a_ts,
         "M1a_cap_share (DV=ln cap-share)": m1a_cap,
         "M1a_pg_ref": m1a_pg,
         "M1a_multihot": m1a_mh,
         "M1a_cba_inter": m1a_in},
        "alt_M1_comparison.csv",
    )
    save_summary(m1a_baseline, "M1a_baseline_V1")
    print(f"\nWrote alt_M1_comparison.csv")


if __name__ == "__main__":
    main()
