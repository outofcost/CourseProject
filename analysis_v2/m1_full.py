"""M1c-full and M1d-full — Mincer regression extended with the v2 feature set.

Specifications (per plan3.md, day 1–2 of Phase 3):
  - M1c_full          : pooled OLS + year FE, all blocks (Stats, Demo, Market, Awards, Durability, Team)
  - M1d_full          : two-way FE (player + season). Time-invariant predictors drop out (is_international,
                        market_size, born_*) — that is expected and noted in summary.
  - M1c_full_alt_mkt  : same as M1c_full but uses market_size_rank_nba instead of top5_market
  - M1c_full_no_collinear : drops `experience` (keeps age + age_sq) and `ws` (keeps `vorp`) after VIF > 10.

Awards block per discussed decision: use `all_nba_lag1 + career_all_nba_count + career_allstar_count`
(no `supermax_eligible_loose` in M1c-full to avoid r=0.78 collinearity with all_nba_lag1).
Supermax goes into H10 (separate H10b spec) and H11 (combined model).

Outputs:
  analysis_v2/output/tables/M1c_full.txt
  analysis_v2/output/tables/M1d_full.txt
  analysis_v2/output/tables/M1c_full_alt_mkt.txt
  analysis_v2/output/tables/M1c_full_no_collinear.txt
  analysis_v2/output/tables/vif_M1c_full.csv
  analysis_v2/output/tables/M1_full_combined.csv  (wide: coef (SE) star per spec)

Run:
    python3 -m analysis_v2.m1_full
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, PooledOLS
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

log = logging.getLogger("analysis_v2.m1_full")
OUT_DIR = ROOT / "analysis_v2" / "output" / "tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Continent grouping for birth_country (per plan3.md: USA / Europe / Latin America / Africa / Asia).
EUROPEAN = {
    "France", "Spain", "Italy", "Germany", "Serbia", "Slovenia", "Croatia",
    "Bosnia and Herzegovina", "North Macedonia", "Montenegro", "Lithuania",
    "Latvia", "Estonia", "Russia", "Ukraine", "Turkey", "Greece", "Israel",
    "Switzerland", "Austria", "Belgium", "Netherlands", "Sweden", "Norway",
    "Finland", "Denmark", "Ireland", "United Kingdom", "Czech Republic",
    "Poland", "Romania", "Bulgaria", "Hungary", "Cyprus", "Georgia", "Belarus",
}
LATIN_AMERICA = {
    "Brazil", "Argentina", "Mexico", "Dominican Republic", "Puerto Rico",
    "Cuba", "Haiti", "Jamaica", "Bahamas", "Trinidad and Tobago", "Venezuela",
    "Colombia", "Chile", "Peru", "Uruguay", "Saint Lucia", "Antigua and Barbuda",
    "US Virgin Islands", "French Guiana",
}
AFRICA = {
    "Nigeria", "Cameroon", "Senegal", "Republic of the Congo",
    "Democratic Republic of the Congo", "Mali", "Tunisia", "Egypt",
    "South Africa", "Sudan", "South Sudan", "Ghana", "Angola", "Gabon",
    "Guinea", "Rwanda", "Ethiopia",
}
ASIA_OCEANIA = {
    "Japan", "China", "Taiwan", "South Korea", "Philippines", "Iran",
    "Lebanon", "Uzbekistan", "Australia", "New Zealand",
}
CANADA = {"Canada"}


def _continent(country: str) -> str:
    if pd.isna(country):
        return "unknown"
    if country == "USA":
        return "usa"
    if country in CANADA:
        return "canada"
    if country in EUROPEAN:
        return "europe"
    if country in LATIN_AMERICA:
        return "latam"
    if country in AFRICA:
        return "africa"
    if country in ASIA_OCEANIA:
        return "asia_oceania"
    return "other"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived columns the regressions reference."""
    out = df.copy()

    # Continent dummies (USA = reference; only born_* for non-USA categories).
    out["continent"] = out["birth_country"].map(_continent)
    for c in ["canada", "europe", "latam", "africa", "asia_oceania"]:
        out[f"born_{c}"] = (out["continent"] == c).astype(int)

    # Team luxury-tax indicator (computed from panel salary aggregation).
    team_payroll = (
        out.groupby(["team_abbr", "season"])["salary_usd"].sum().reset_index()
        .rename(columns={"salary_usd": "team_salary_committed_t"})
    )
    out = out.merge(team_payroll, on=["team_abbr", "season"], how="left")
    out["team_cap_space_t"] = out["cap_t"] - out["team_salary_committed_t"]
    out["team_over_luxury_tax_t"] = (
        out["team_salary_committed_t"] > out["luxury_tax"]
    ).astype(int)

    # Robust-spec binaries for awards "veteran legend vs first-time elite" distinction.
    # See Chapter 5 discussion: cumulative count is contaminated by aging-veteran
    # selection (Carmelo/Wade etc. on minimum contracts).
    out["has_career_all_nba"] = (out.get("career_all_nba_count", 0).fillna(0) >= 1).astype(int)
    out["has_career_allstar"] = (out.get("career_allstar_count", 0).fillna(0) >= 1).astype(int)
    out["multi_all_nba"] = (out.get("career_all_nba_count", 0).fillna(0) >= 3).astype(int)

    return out


def prep_for_full(df: pd.DataFrame) -> pd.DataFrame:
    """Filter sample and drop rows missing core regressors."""
    must_have = [
        "ln_salary", "ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
        "per", "ws", "vorp", "usg_pct",
        "age", "age_sq", "experience",
        "allstar", "undrafted", "log_draft_pick",
        "pos_PG", "pos_SG", "pos_SF", "pos_PF",
        "post_cba_2017", "post_covid",
        "is_international", "born_canada", "born_europe", "born_latam",
        "born_africa", "born_asia_oceania",
        "top5_market",
        "all_nba_lag1", "career_all_nba_count", "career_allstar_count",
        "games_missed_lag1",
    ]
    # team_win_pct_lag1 and team_over_luxury_tax_t are NaN for TOT rows and 2016
    # — they're optional, NaN gets dropped per-spec.
    return df.dropna(subset=must_have)


def panel_index(d: pd.DataFrame) -> pd.DataFrame:
    return d.set_index(["player_id", "season"])


STATS_BLOCK = ["ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
               "per", "ws", "vorp", "usg_pct"]
AGE_BLOCK = ["age", "age_sq", "experience"]
DEMO_BLOCK_BASE = ["allstar", "undrafted", "log_draft_pick",
                   "pos_PG", "pos_SG", "pos_SF", "pos_PF"]
# Continent dummies (USA = reference). is_international is omitted from the main
# spec because it equals sum(born_*) exactly and would create perfect collinearity.
# Use is_international only in the `_intl_only` alt spec (drop continent dummies then).
INTL_BLOCK = ["born_canada", "born_europe", "born_latam", "born_africa", "born_asia_oceania"]
MARKET_BLOCK_TOP5 = ["top5_market"]
MARKET_BLOCK_RANK = ["market_size_rank_nba"]
AWARDS_BLOCK = ["all_nba_lag1", "career_all_nba_count", "career_allstar_count"]
DURABILITY_BLOCK = ["games_missed_lag1"]
TEAM_BLOCK = ["team_win_pct_lag1", "team_made_playoffs_lag1",
              "team_over_luxury_tax_t"]
STRUCT_BLOCK = ["post_cba_2017", "post_covid", "no_income_tax"]


def compute_vif(d: pd.DataFrame, regressors: list[str]) -> pd.DataFrame:
    X = sm.add_constant(d[regressors].astype(float))
    vifs = []
    for i, name in enumerate(X.columns):
        if name == "const":
            continue
        try:
            v = variance_inflation_factor(X.values, i)
        except Exception:
            v = np.nan
        vifs.append({"variable": name, "VIF": v})
    return pd.DataFrame(vifs).sort_values("VIF", ascending=False).reset_index(drop=True)


def fit_pooled(d: pd.DataFrame, regressors: list[str]) -> "PooledOLS":
    d2 = d.dropna(subset=regressors + ["ln_salary"])
    y = d2["ln_salary"]
    X = sm.add_constant(d2[regressors].astype(float))
    return PooledOLS(y, X).fit(cov_type="clustered", cluster_entity=True), d2


def fit_panel_year_fe(d: pd.DataFrame, regressors: list[str]) -> "PanelOLS":
    d2 = d.dropna(subset=regressors + ["ln_salary"])
    y = d2["ln_salary"]
    X = sm.add_constant(d2[regressors].astype(float))
    return PanelOLS(y, X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    ), d2


def fit_panel_twoway_fe(d: pd.DataFrame, regressors: list[str]) -> "PanelOLS":
    d2 = d.dropna(subset=regressors + ["ln_salary"])
    y = d2["ln_salary"]
    X = d2[regressors].astype(float)
    # age becomes a linear function of (calendar year − birth_year) → perfectly
    # absorbed by player + year FE. drop_absorbed=True handles it gracefully.
    return PanelOLS(y, X, entity_effects=True, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True, debiased=False,
    ), d2


def save_summary(res, name: str) -> None:
    (OUT_DIR / f"{name}.txt").write_text(str(res.summary), encoding="utf-8")
    log.info("wrote %s.txt", name)


def _star(p: float) -> str:
    if pd.isna(p):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""


def combine_models(fits: dict, path: Path) -> None:
    """Wide CSV: rows = variables, columns = model name; cell = '{coef} ({se}){stars}'."""
    all_vars: list[str] = []
    for r in fits.values():
        for v in r.params.index:
            if v not in all_vars:
                all_vars.append(v)
    rows = []
    for v in all_vars:
        row = {"variable": v}
        for name, r in fits.items():
            if v in r.params.index:
                coef = r.params[v]
                se = r.std_errors[v]
                p = r.pvalues[v]
                row[name] = f"{coef:.4f} ({se:.4f}){_star(p)}"
            else:
                row[name] = ""
        rows.append(row)
    # Add summary stats footer
    foot_n = {"variable": "N"}
    foot_r2 = {"variable": "R^2"}
    for name, r in fits.items():
        foot_n[name] = int(r.nobs)
        try:
            foot_r2[name] = f"{r.rsquared:.4f}"
        except Exception:
            foot_r2[name] = "NA"
    pd.DataFrame(rows + [foot_n, foot_r2]).to_csv(path, index=False)
    log.info("wrote %s", path)


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    src = ROOT / "data" / "clean" / "data_analysis_v2.csv"
    df = pd.read_csv(src)
    log.info("loaded %d × %d", *df.shape)

    df = add_features(df)
    d = prep_for_full(df)
    log.info("after prep: %d rows", len(d))

    di = panel_index(d)

    # ------------- M1c_full (Pooled, year FE via dummies for true Pooled) ---
    # Note: PooledOLS doesn't auto-add year FE. To match v1's M1a style we add
    # post_cba_2017 + post_covid as structural dummies, OR use PanelOLS with
    # time_effects=True. We follow v1's pattern: PanelOLS time_effects for "year FE"
    # specifications, PooledOLS only for unweighted spec (M1a-style).
    main_specs = STATS_BLOCK + AGE_BLOCK + DEMO_BLOCK_BASE + INTL_BLOCK \
        + MARKET_BLOCK_TOP5 + AWARDS_BLOCK + DURABILITY_BLOCK \
        + TEAM_BLOCK + STRUCT_BLOCK

    log.info("M1c_full regressors: %d", len(main_specs))

    m1c, d_m1c = fit_panel_year_fe(di, [c for c in main_specs if c not in ("post_cba_2017", "post_covid")])
    # Year FE absorbs post_cba_2017 and post_covid → exclude them from regressor list
    save_summary(m1c, "M1c_full")
    log.info("M1c_full: N=%d, R²=%.4f", int(m1c.nobs), m1c.rsquared)

    # ------------- M1c_full_alt_mkt: market_size_rank_nba instead of top5_market
    alt_specs = [c for c in main_specs if c != "top5_market"] + ["market_size_rank_nba"]
    alt_specs = [c for c in alt_specs if c not in ("post_cba_2017", "post_covid")]
    m1c_alt, _ = fit_panel_year_fe(di, alt_specs)
    save_summary(m1c_alt, "M1c_full_alt_mkt")
    log.info("M1c_full_alt_mkt: N=%d, R²=%.4f", int(m1c_alt.nobs), m1c_alt.rsquared)

    # ------------- M1d_full: two-way FE (player + season).
    # Time-invariant regressors must be dropped: is_international, born_*, top5_market
    # (market_size_rank_nba), undrafted (constant per player), log_draft_pick.
    # log_draft_pick is technically constant per player → drops out.
    twoway_regs = [c for c in main_specs
                   if c not in INTL_BLOCK + MARKET_BLOCK_TOP5
                   + ["post_cba_2017", "post_covid", "undrafted", "log_draft_pick"]
                   + ["pos_PG", "pos_SG", "pos_SF", "pos_PF"]
                   + ["age", "age_sq", "experience"]]  # absorbed by player+year FE
    m1d, _ = fit_panel_twoway_fe(di, twoway_regs)
    save_summary(m1d, "M1d_full")
    log.info(
        "M1d_full (two-way FE, time-invariant dropped: intl, market, demo): "
        "N=%d, within-R²=%.4f",
        int(m1d.nobs), m1d.rsquared_within,
    )

    # ------------- VIF on M1c_full regressors -----------------------------------
    vif = compute_vif(d_m1c, [c for c in main_specs if c not in ("post_cba_2017", "post_covid")])
    vif.to_csv(OUT_DIR / "vif_M1c_full.csv", index=False)
    log.info(
        "VIF top-5:\n%s",
        vif.head(5).to_string(index=False),
    )

    # ------------- M1c_full_robust_awards: cumulative → binary -----------------
    # Replaces career_all_nba_count + career_allstar_count with binary indicators
    # to isolate "has been elite" effect from "aging vet residual" effect.
    robust_aw = [c for c in main_specs if c not in
                 ("career_all_nba_count", "career_allstar_count",
                  "post_cba_2017", "post_covid")] + ["has_career_all_nba",
                                                      "has_career_allstar",
                                                      "multi_all_nba"]
    m1c_ra, _ = fit_panel_year_fe(di, robust_aw)
    save_summary(m1c_ra, "M1c_full_robust_awards")
    log.info("M1c_full_robust_awards: N=%d, R²=%.4f", int(m1c_ra.nobs), m1c_ra.rsquared)

    # ------------- M1c_full_no_collinear: drop experience, ws ------------------
    nocoll = [c for c in main_specs if c not in ("experience", "ws",
                                                  "post_cba_2017", "post_covid")]
    m1c_nc, _ = fit_panel_year_fe(di, nocoll)
    save_summary(m1c_nc, "M1c_full_no_collinear")
    log.info("M1c_full_no_collinear: N=%d, R²=%.4f", int(m1c_nc.nobs), m1c_nc.rsquared)

    vif_nc = compute_vif(
        d.dropna(subset=nocoll + ["ln_salary"]),
        nocoll,
    )
    vif_nc.to_csv(OUT_DIR / "vif_M1c_full_no_collinear.csv", index=False)

    # Combined wide table
    combine_models(
        {
            "M1c_full (year FE)": m1c,
            "M1c_full_alt_mkt": m1c_alt,
            "M1c_full_robust_awards": m1c_ra,
            "M1c_full_no_collinear": m1c_nc,
            "M1d_full (2-way FE)": m1d,
        },
        OUT_DIR / "M1_full_combined.csv",
    )

    # Diagnostic note: M1c-full vs v1 M1c — what changed?
    note = []
    note.append("# M1c-full diagnostic notes\n")
    note.append(f"Sample: {int(m1c.nobs)} player-seasons after dropping TOT (market) and 2016 (lags)\n")
    note.append(f"R² = {m1c.rsquared:.4f} (v1 M1c R² was 0.86 — for direct comparison see combined table)\n")
    note.append("Key new findings (to discuss in Chapter 4):\n")
    # Print key new coefficients
    for var in ["all_nba_lag1", "career_all_nba_count", "career_allstar_count",
                "top5_market", "is_international", "born_europe", "born_africa",
                "games_missed_lag1", "team_win_pct_lag1", "team_over_luxury_tax_t"]:
        if var in m1c.params.index:
            note.append(
                f"- **{var}**: β = {m1c.params[var]:.4f}, SE = {m1c.std_errors[var]:.4f}, "
                f"p = {m1c.pvalues[var]:.4f}\n"
            )
    (OUT_DIR.parent.parent / "reports" / "m1_full_notes.md").write_text("".join(note), encoding="utf-8")

    log.info("DONE — outputs in %s", OUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
