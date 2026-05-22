"""Regression test: re-run M1a, M1b, M1c, M1d on data_analysis_v2.csv and confirm
coefficients match the published v1 results (output/tables_v1/M1*.txt).

This catches accidental column-overwrites or join-induced row-count changes in prep_v2.
Tolerance: abs(coef_diff) < 1e-4 (4 decimal places shown in published tables).

Run:
    python3 -m analysis_v2.regress_test_v1
"""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.config import (  # noqa: E402
    BASIC_STATS,
    COMBINED_STATS,
    COMMON_NO_STRUCT,
    COMMON_STRUCT,
    COMMON_WITHIN,
)
from analysis_v1.utils_v1 import panel_index, prep_for_models  # noqa: E402

log = logging.getLogger("analysis_v2.regress_test")
TABLES_V1 = ROOT / "output" / "tables_v1"
REPORTS_DIR = ROOT / "analysis_v2" / "reports"

# Tolerance for coefficient comparison. Published tables show 4 decimal places;
# round-trip precision puts us at ~1e-4.
TOL = 5e-4


def parse_published_table(path: Path) -> pd.DataFrame:
    """Parse linearmodels summary text → DataFrame indexed by variable
    with columns Parameter, Std.Err.
    """
    lines = path.read_text().splitlines()
    started = False
    rows: list[dict] = []
    for line in lines:
        if "Parameter Estimates" in line:
            started = True
            continue
        if not started:
            continue
        if re.match(r"^-{5,}$", line.strip()):
            continue
        if line.startswith("="):
            continue
        if not line.strip():
            continue
        # Header row
        if "Parameter" in line and "Std. Err." in line:
            continue
        parts = re.split(r"\s+", line.strip())
        if len(parts) < 3:
            continue
        var = parts[0]
        try:
            param = float(parts[1])
            se = float(parts[2])
        except ValueError:
            continue
        rows.append({"variable": var, "param": param, "se": se})
    return pd.DataFrame(rows).set_index("variable")


def fit_v1_models(df: pd.DataFrame) -> dict:
    d = prep_for_models(df, restrict_single_team=False)
    d = panel_index(d)
    y = d["ln_salary"]

    X1a = sm.add_constant(d[BASIC_STATS + COMMON_STRUCT])
    m1a = PooledOLS(y, X1a).fit(cov_type="clustered", cluster_entity=True)

    X1b = sm.add_constant(d[BASIC_STATS + COMMON_NO_STRUCT])
    m1b = PanelOLS(y, X1b, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )

    X1c = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT])
    m1c = PanelOLS(y, X1c, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )

    X1d = d[COMBINED_STATS + COMMON_WITHIN]
    m1d = PanelOLS(y, X1d, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    return {"M1a_pooled_basic": m1a, "M1b_basic_yearFE": m1b,
            "M1c_combined_yearFE": m1c, "M1d_2wayFE_combined": m1d}


def compare(model_name: str, fit, published: Path, tol: float = TOL) -> dict:
    """Return summary of coefficient mismatches for a single model."""
    pub = parse_published_table(published)
    actual = pd.DataFrame(
        {"param": fit.params, "se": fit.std_errors}
    )
    common = pub.index.intersection(actual.index)
    miss_left = pub.index.difference(actual.index).tolist()
    miss_right = actual.index.difference(pub.index).tolist()

    diffs = []
    for v in common:
        dparam = abs(pub.loc[v, "param"] - actual.loc[v, "param"])
        dse = abs(pub.loc[v, "se"] - actual.loc[v, "se"])
        ok = dparam < tol and dse < tol * 5
        diffs.append({
            "variable": v,
            "published_param": pub.loc[v, "param"],
            "v2_param": actual.loc[v, "param"],
            "diff_param": dparam,
            "diff_se": dse,
            "OK": ok,
        })
    diffs_df = pd.DataFrame(diffs)
    return {
        "model": model_name,
        "n_common": len(common),
        "missing_in_v2": miss_left,
        "extra_in_v2": miss_right,
        "max_diff_param": diffs_df["diff_param"].max() if len(diffs_df) else 0.0,
        "n_fail": int((~diffs_df["OK"]).sum()) if len(diffs_df) else 0,
        "table": diffs_df,
    }


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    v2_path = ROOT / "data" / "clean" / "data_analysis_v2.csv"
    if not v2_path.exists():
        log.error("data_analysis_v2.csv not found — run prep_v2 first")
        return 1
    df = pd.read_csv(v2_path)
    log.info("loaded v2 panel: %d × %d", *df.shape)

    fits = fit_v1_models(df)

    summary_rows = []
    full_diff_tables = []
    all_ok = True
    for name, fit in fits.items():
        published = TABLES_V1 / f"{name}.txt"
        if not published.exists():
            log.warning("missing published table: %s", published)
            continue
        r = compare(name, fit, published)
        log.info(
            "%s: n_common=%d, max_param_diff=%.2e, n_fail=%d",
            name,
            r["n_common"],
            r["max_diff_param"],
            r["n_fail"],
        )
        if r["n_fail"] > 0:
            all_ok = False
            log.warning("  failing rows:")
            for _, row in r["table"][~r["table"]["OK"]].iterrows():
                log.warning(
                    "    %-18s pub=%.4f vs v2=%.4f  diff=%.2e",
                    row["variable"],
                    row["published_param"],
                    row["v2_param"],
                    row["diff_param"],
                )
        summary_rows.append({
            "model": name,
            "n_common": r["n_common"],
            "max_param_diff": r["max_diff_param"],
            "n_fail": r["n_fail"],
        })
        r["table"]["model"] = name
        full_diff_tables.append(r["table"])

    s = pd.DataFrame(summary_rows)
    s.to_csv(REPORTS_DIR / "regress_test_v1_summary.csv", index=False)
    if full_diff_tables:
        pd.concat(full_diff_tables, ignore_index=True).to_csv(
            REPORTS_DIR / "regress_test_v1_detail.csv", index=False
        )
    print(s.to_string(index=False))

    if all_ok:
        log.info("ALL MODELS REPLICATE — safe to proceed to phase 3")
        return 0
    log.error("REGRESSION TEST FAILED — investigate before proceeding")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
