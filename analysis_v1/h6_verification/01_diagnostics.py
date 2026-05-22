"""Этап 1. Диагностика самой переменной `cy_exogenous`.

Производит:
    output/h6_verification/01_cy_exogenous_diagnostics.csv     — по сезонам
    output/h6_verification/01_cy_by_age.csv                    — по возрастным группам
    output/h6_verification/01_cy_components.csv                — доли компонентов
    output/h6_verification/01_dsalary_by_group.csv             — Δlog_salary по группам
    output/h6_verification/01_summary.md                       — резюме
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


def load_data() -> pd.DataFrame:
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    # Δlog_salary при наличии salary_next
    has = df["salary_next"].notna() & (df["salary_usd"] > 0)
    df["dln_salary"] = np.nan
    df.loc[has, "dln_salary"] = np.log(df.loc[has, "salary_next"]) - np.log(df.loc[has, "salary_usd"])
    # Cap-deflated Δsalary
    df["dln_salary_cap_share"] = np.nan
    has2 = df["salary_cap_share_next"].notna() & (df["salary_cap_share_t"] > 0)
    df.loc[has2, "dln_salary_cap_share"] = (
        np.log(df.loc[has2, "salary_cap_share_next"]) - np.log(df.loc[has2, "salary_cap_share_t"])
    )
    return df


def by_season(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for s, g in df.groupby("season"):
        rows.append({
            "season": int(s),
            "n_total": len(g),
            "n_cy_exogenous_1": int((g["cy_exogenous"] == 1).sum()),
            "n_cy_exogenous_0": int((g["cy_exogenous"] == 0).sum()),
            "n_cy_exogenous_NA": int(g["cy_exogenous"].isna().sum()),
            "n_contract_year_1": int((g["contract_year"] == 1).sum()),
            "n_cy_A_up_1": int((g["cy_A_up"] == 1).sum()),
            "n_cy_B_offseason_1": int((g["cy_B_offseason"] == 1).sum()),
            "n_cy_C_1": int((g["cy_C"] == 1).sum()),
        })
    return pd.DataFrame(rows)


def by_age(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["age_bin"] = pd.cut(df["age"],
                            bins=[0, 22, 25, 28, 31, 35, 50],
                            labels=["<23", "23-25", "26-28", "29-31", "32-35", "36+"])
    rows = []
    for ab, g in df.groupby("age_bin", observed=True):
        rows.append({
            "age_bin": str(ab),
            "n": len(g),
            "n_cy_exogenous_1": int((g["cy_exogenous"] == 1).sum()),
            "share_cy_exogenous": float((g["cy_exogenous"] == 1).sum() / max(g["cy_exogenous"].notna().sum(), 1)),
            "n_cy_C_only": int(((g["cy_C"] == 1) & (g["cy_B_offseason"] == 0)).sum()),
            "n_cy_B_only": int(((g["cy_B_offseason"] == 1) & (g["cy_C"] == 0)).sum()),
            "n_both_B_and_C": int(((g["cy_B_offseason"] == 1) & (g["cy_C"] == 1)).sum()),
        })
    return pd.DataFrame(rows)


def components(df: pd.DataFrame) -> pd.DataFrame:
    """Какие компоненты дают cy_exogenous=1: только B, только C, или оба."""
    m = df.dropna(subset=["cy_exogenous"]).copy()
    cy1 = m[m["cy_exogenous"] == 1].copy()
    n_total = len(cy1)
    is_B = (cy1["cy_B_offseason"] == 1)
    is_C = (cy1["cy_C"] == 1)
    rows = [
        {"group": "cy_B_offseason only", "n": int((is_B & ~is_C).sum()), "share": float((is_B & ~is_C).sum() / n_total)},
        {"group": "cy_C only",            "n": int((~is_B & is_C).sum()), "share": float((~is_B & is_C).sum() / n_total)},
        {"group": "Both B & C",            "n": int((is_B & is_C).sum()),  "share": float((is_B & is_C).sum() / n_total)},
        {"group": "Total cy_exogenous=1", "n": n_total, "share": 1.0},
    ]
    return pd.DataFrame(rows)


def _stat_block(s: pd.Series) -> dict:
    s = s.dropna()
    return {
        "n":          int(len(s)),
        "mean":       float(s.mean()) if len(s) else np.nan,
        "median":     float(s.median()) if len(s) else np.nan,
        "sd":         float(s.std()) if len(s) > 1 else np.nan,
        "share_pos":  float((s > 0).mean()) if len(s) else np.nan,
        "share_near0": float((s.abs() <= 0.05).mean()) if len(s) else np.nan,
        "share_neg":  float((s < 0).mean()) if len(s) else np.nan,
        "p25":        float(s.quantile(0.25)) if len(s) else np.nan,
        "p75":        float(s.quantile(0.75)) if len(s) else np.nan,
    }


def dsalary_by_group(df: pd.DataFrame) -> pd.DataFrame:
    """Распределение Δlog_salary внутри групп."""
    rows = []
    base = df.dropna(subset=["dln_salary", "cy_exogenous"]).copy()
    base = base[~base["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])]

    groups = {
        "All (cy_exogenous obs)":             base,
        "cy_exogenous=0":                      base[base["cy_exogenous"] == 0],
        "cy_exogenous=1 (any)":               base[base["cy_exogenous"] == 1],
        "cy_exogenous=1, C only":              base[(base["cy_exogenous"] == 1) & (base["cy_C"] == 1) & (base["cy_B_offseason"] == 0)],
        "cy_exogenous=1, B only":              base[(base["cy_exogenous"] == 1) & (base["cy_C"] == 0) & (base["cy_B_offseason"] == 1)],
        "cy_exogenous=1, B and C":             base[(base["cy_exogenous"] == 1) & (base["cy_C"] == 1) & (base["cy_B_offseason"] == 1)],
        "cy_A_up=1, cy_exogenous=0":           base[(base["cy_A_up"] == 1) & (base["cy_exogenous"] == 0)],
        "contract_year=1, cy_exogenous=0":     base[(base["contract_year"] == 1) & (base["cy_exogenous"] == 0)],
        "contract_year=1, cy_exogenous=1":     base[(base["contract_year"] == 1) & (base["cy_exogenous"] == 1)],
        "contract_year=0":                     base[base["contract_year"] == 0],
    }
    for name, sub in groups.items():
        block = _stat_block(sub["dln_salary"])
        block_cs = _stat_block(sub["dln_salary_cap_share"])
        rows.append({
            "group": name,
            **{f"dln_{k}": v for k, v in block.items()},
            **{f"dlncap_{k}": v for k, v in block_cs.items()},
        })
    return pd.DataFrame(rows)


def downward_fa(df: pd.DataFrame) -> pd.DataFrame:
    """Внутри cy_B_offseason=1: какая доля имеет Δlog_salary < 0 / ≈ 0 / > 0?"""
    base = df.dropna(subset=["dln_salary", "cy_B_offseason"]).copy()
    base = base[~base["team_abbr"].isin(["2TM", "3TM", "4TM", "TOT"])]
    rows = []
    for name, sub in [
        ("cy_B_offseason=1, all",       base[base["cy_B_offseason"] == 1]),
        ("cy_B_offseason=1, cy_C=0",     base[(base["cy_B_offseason"] == 1) & (base["cy_C"] == 0)]),
        ("cy_B_offseason=1, age<28",     base[(base["cy_B_offseason"] == 1) & (base["age"] < 28)]),
        ("cy_B_offseason=1, age>=28",    base[(base["cy_B_offseason"] == 1) & (base["age"] >= 28)]),
    ]:
        rows.append({
            "group": name,
            **_stat_block(sub["dln_salary"]),
        })
    return pd.DataFrame(rows)


def write_summary(out_dir: Path, season_df, age_df, comp_df, dsal_df, dfa_df) -> None:
    md = []
    md.append("# Этап 1 — Диагностика `cy_exogenous` (резюме)\n")
    md.append("Файлы: `01_cy_exogenous_diagnostics.csv`, `01_cy_by_age.csv`, `01_cy_components.csv`, `01_dsalary_by_group.csv`, `01_downward_fa.csv`.\n")

    md.append("## 1.1. Распределение по сезонам\n")
    md.append(season_df.to_markdown(index=False))
    md.append("\n")

    md.append("## 1.2. Распределение по возрасту\n")
    md.append(age_df.to_markdown(index=False))
    md.append("\n")

    md.append("## 1.3. Из чего состоит `cy_exogenous = 1`\n")
    md.append(comp_df.to_markdown(index=False))
    md.append("\n")

    md.append("## 1.4. Δlog_salary по группам (single-team, Δlog non-NA)\n")
    md.append(dsal_df.round(4).to_markdown(index=False))
    md.append("\n")

    md.append("## 1.5. Селекционное смещение в `cy_B_offseason`\n")
    md.append(dfa_df.round(4).to_markdown(index=False))
    md.append("\n")

    (out_dir / "01_summary.md").write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    df = load_data()
    sea = by_season(df)
    age = by_age(df)
    comp = components(df)
    dsal = dsalary_by_group(df)
    dfa = downward_fa(df)

    sea.to_csv(OUT / "01_cy_exogenous_diagnostics.csv", index=False)
    age.to_csv(OUT / "01_cy_by_age.csv", index=False)
    comp.to_csv(OUT / "01_cy_components.csv", index=False)
    dsal.to_csv(OUT / "01_dsalary_by_group.csv", index=False)
    dfa.to_csv(OUT / "01_downward_fa.csv", index=False)

    write_summary(OUT, sea, age, comp, dsal, dfa)
    print("[Этап 1] OK")


if __name__ == "__main__":
    main()
