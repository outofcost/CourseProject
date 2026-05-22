"""§5.2 — Event-study вокруг CBA 2017 (упрощённая версия для бакалавра).

CBA 2017 подписан летом 2017, действует с сезона 2017/18 (season_end=2018).

Регрессия:
    ln_salary = β_0 + Σ_{τ ≠ −1} β_τ · 1{event_time = τ}
                + Stats + Controls + ε
где event_time = season − 2018, τ = −1 — reference.

Year FE *не включаются* — они полностью absorb-нули бы event-dummies.

Pre-trends test: F-test на β_{−2}. Если pre-trend близок к нулю —
DiD-интерпретация валидна.
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
from linearmodels.panel import PooledOLS

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import BASIC_STATS, COMMON_STRUCT, DATA_CLEAN  # noqa: E402
from analysis_v1.utils_v1 import (OUT_FIGURES_V1, OUT_TABLES_V1,  # noqa: E402
                                  panel_index, prep_for_models, save_summary)

warnings.filterwarnings("ignore")

EVENT_YEAR = 2018  # season_end CBA implementation
TAU_RANGE = range(-2, 7)  # 2016/17 (−2), ..., 2023/24 (+6)
REF_TAU = -1


def main() -> None:
    df = pd.read_csv(DATA_CLEAN / "data_analysis_v1.csv")
    d = prep_for_models(df, restrict_single_team=False).copy()
    d["event_time"] = d["season"] - EVENT_YEAR

    # Drop τ outside [-2, +6] на всякий случай (у нас сезоны 2016-2024).
    d = d[d["event_time"].isin(list(TAU_RANGE))].copy()

    # Дамми для каждого τ ≠ −1
    event_cols = []
    for tau in TAU_RANGE:
        if tau == REF_TAU:
            continue
        col = f"event_t_{tau:+d}".replace("+", "p").replace("-", "m")
        d[col] = (d["event_time"] == tau).astype(int)
        event_cols.append(col)

    # COMMON_STRUCT содержит post_cba_2017, post_covid — убираем (collinear).
    controls = [c for c in COMMON_STRUCT if c not in ("post_cba_2017", "post_covid")]

    d_idx = panel_index(d)
    y = d_idx["ln_salary"]
    X = sm.add_constant(d_idx[BASIC_STATS + controls + event_cols])

    # Без year FE — event dummies *заменяют* year FE.
    res = PooledOLS(y, X).fit(cov_type="clustered", cluster_entity=True)
    save_summary(res, "event_study_CBA2017")

    # Извлекаем коэффициенты event-time
    coefs, ses, taus = [], [], []
    for tau in TAU_RANGE:
        if tau == REF_TAU:
            coefs.append(0.0); ses.append(0.0); taus.append(tau)
            continue
        col = f"event_t_{tau:+d}".replace("+", "p").replace("-", "m")
        coefs.append(res.params[col])
        ses.append(res.std_errors[col])
        taus.append(tau)

    es_df = pd.DataFrame({
        "tau": taus,
        "beta": coefs,
        "se": ses,
        "ci_low":  np.array(coefs) - 1.96 * np.array(ses),
        "ci_high": np.array(coefs) + 1.96 * np.array(ses),
    })
    es_df.to_csv(OUT_TABLES_V1 / "event_study_CBA2017.csv", index=False)
    print("Event-study coefficients (τ vs ln_salary):")
    print(es_df.to_string(index=False))

    # Pre-trend F-test: β_{−2} = 0 ?
    pre_col = f"event_t_{-2:+d}".replace("+", "p").replace("-", "m")
    pre_p = res.pvalues[pre_col]
    print(f"\nPre-trend test (β_{{-2}} = 0): p = {pre_p:.4f}")
    print("  → if p > 0.10: парallel-trends правдоподобны (DiD валиден).")
    print("  → if p < 0.05: pre-trends есть → DiD скомпрометирован.")

    # Фигура
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(es_df["tau"], es_df["beta"],
                yerr=1.96 * es_df["se"],
                marker="o", capsize=4, color="black", lw=1.2)
    ax.axhline(0, ls="--", color="gray", lw=0.8)
    ax.axvline(0, ls=":", color="red", lw=1.0)
    ax.set_xlabel("Event time (сезон − 2018, CBA 2017 takes effect)")
    ax.set_ylabel("β (coefficient on event-time dummy)")
    ax.set_title("Event-study: ln(salary) around CBA 2017")
    ax.text(0.05, -0.08, "ref: τ = −1", color="gray", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(OUT_FIGURES_V1 / "event_study_cba2017.png", dpi=150)
    print(f"Saved {OUT_FIGURES_V1 / 'event_study_cba2017.png'}")


if __name__ == "__main__":
    main()
