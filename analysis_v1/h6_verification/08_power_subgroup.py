"""Этап 8. Power analysis в разрезе подгрупп.

Для каждой осмысленной подгруппы Этапа 6 считаем MDE при 80% мощности
(MDE = 2.8 × SE) и сравниваем с агрегатной MDE из V1 power_analysis.csv.

Выводы:
    - В каких подгруппах мощность достаточна для детектирования Stiroh-
      сопоставимого эффекта (≈+3% производительности → ≈+5–10% Δsalary)?
    - В каких подгруппах MDE > 0.20 (мы не могли бы обнаружить эффект Stiroh)?

Outputs:
    output/h6_verification/08_power_by_subgroup.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "output" / "h6_verification"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    df = pd.read_csv(OUT / "06_heterogeneous_effects.csv")
    df = df.dropna(subset=["beta_cy", "se_cy"]).copy()

    # MDE и benchmark
    df["MDE_pct_salary"] = df["MDE_cy"]  # β уже в log-points
    # Stiroh benchmark: 3% performance → ~5-10% salary at NBA earnings premia
    df["sufficient_for_stiroh_5pct"] = df["MDE_cy"] < 0.05
    df["sufficient_for_stiroh_10pct"] = df["MDE_cy"] < 0.10
    df["sufficient_for_stiroh_20pct"] = df["MDE_cy"] < 0.20
    df["significant_5pct"] = df["p_cy"] < 0.05
    df["sign"] = np.sign(df["beta_cy"]).astype(int)

    df.to_csv(OUT / "08_power_by_subgroup.csv", index=False)

    # Summary by cy_var
    print("\nMDE summary by proxy/group:")
    summary = df.groupby(["cy_var", "group"])["MDE_cy"].agg(["mean", "min", "max"])
    print(summary.round(4).to_string())

    print("\nПодгруппы, где |β| > MDE_80 (=> мощность достаточная для уровня эффекта):")
    above_mde = df[df["beta_cy"].abs() > df["MDE_cy"]]
    print(above_mde[["cy_var", "group", "subset", "beta_cy", "se_cy", "p_cy",
                      "MDE_cy"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
