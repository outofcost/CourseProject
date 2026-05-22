"""§3 final: changes_summary.csv — ключевые коэффициенты V0 vs V1.

Парсит .txt summary файлы из output/tables/ (V0) и output/tables_v1/ (V1)
и собирает таблицу с β, SE, p, N для регрессоров, представляющих
гипотезы H1–H7.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

V0_TABLES = ROOT / "output" / "tables"
V1_TABLES = ROOT / "output" / "tables_v1"

# (model, variable, [list of (label, file_v0, file_v1)])
TARGETS = [
    ("M1a", "post_cba_2017", "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "post_covid",    "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "age",           "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "experience",    "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "undrafted",     "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "allstar",       "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1a", "ppg",           "M1a_pooled_basic", "M1a_pooled_basic"),
    ("M1d", "experience",    "M1d_2wayFE_combined", "M1d_2wayFE_combined"),
    ("M2c", "state_tax_rate","M2c_state_tax_rate", "M2c_state_tax_rate"),
    ("M2c", "no_income_tax", "M2b_no_income_tax",  "M2b_no_income_tax"),
    ("M3a", "contract_year", "M3a_contract_year_level", "M3a_contract_year_level"),
    ("M3c", "contract_year", "M3c_delta_salary_canonical", "M3c_delta_salary_composite_cy"),
    ("M3d", "contract_year", "M3d_2wayFE_contract_year", "M3d_2wayFE_contract_year"),
    # V1-only:
    ("M3c_canonical", "cy_exogenous", None, "M3c_canonical_cy_exogenous"),
    ("M3c_circular",  "cy_A_up",      None, "M3c_circular_cy_A_up"),
    ("R1", "contract_year",  "R1_full_tax_plus_contract", "R1_full_tax_plus_contract"),
    ("R1", "no_income_tax",  "R1_full_tax_plus_contract", "R1_full_tax_plus_contract"),
    ("R3", "contract_year",  "R3_excl_rookies", "R3_excl_first_year"),
]


_NUM = r"-?\d+\.\d+|\bnan\b"
_LINE_RE = re.compile(
    rf"^\s*([A-Za-z0-9_]+)\s+({_NUM})\s+({_NUM})\s+({_NUM})\s+({_NUM})",
    re.MULTILINE,
)


def _parse_summary(path: Path, varname: str) -> dict | None:
    """linearmodels / statsmodels coefficient table: var | param | SE | t/z | P> ..."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    # nobs
    n_match = re.search(r"No\.?\s*Observations:\s*(\d+)", text)
    n_obs = int(n_match.group(1)) if n_match else None

    for m in _LINE_RE.finditer(text):
        if m.group(1) == varname:
            return {
                "coef": float(m.group(2)),
                "se":   float(m.group(3)),
                "p":    float(m.group(5)),
                "N":    n_obs,
            }
    return None


def _stars(p: float | None) -> str:
    if p is None:
        return ""
    return "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else ""))


def main() -> None:
    rows = []
    for model, var, v0_file, v1_file in TARGETS:
        r0 = _parse_summary(V0_TABLES / f"{v0_file}.txt", var) if v0_file else None
        r1 = _parse_summary(V1_TABLES / f"{v1_file}.txt", var) if v1_file else None
        rows.append({
            "model": model,
            "variable": var,
            "V0_β": f"{r0['coef']:.4f}{_stars(r0['p'])}" if r0 else "—",
            "V0_SE": f"{r0['se']:.4f}" if r0 else "",
            "V0_p":  f"{r0['p']:.4f}" if r0 else "",
            "V0_N":  r0["N"] if r0 else "",
            "V1_β": f"{r1['coef']:.4f}{_stars(r1['p'])}" if r1 else "—",
            "V1_SE": f"{r1['se']:.4f}" if r1 else "",
            "V1_p":  f"{r1['p']:.4f}" if r1 else "",
            "V1_N":  r1["N"] if r1 else "",
        })

    out = pd.DataFrame(rows)
    out_path = V1_TABLES / "changes_summary.csv"
    out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Wrote {out_path}")
    # Полный вывод в консоль:
    with pd.option_context("display.max_colwidth", 30, "display.width", 200):
        print(out.to_string(index=False))


if __name__ == "__main__":
    main()
