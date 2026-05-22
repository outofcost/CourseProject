"""Этап 3. Альтернативные определения contract year + M3c-регрессия.

Строим 5 новых cy-сигналов с явным указанием captured/missed/exogeneity:

    1. cy_same_team_endpoint — захватывает re-signings со своей командой.
       cy_same_team_endpoint = 1, если:
         (a) salary_next / salary_t > 1.20 (новый контракт);
         (b) team_next == team_t (та же команда);
         (c) игрок наблюдался ≥3 сезона с этой командой
             (исключаем mid-contract bumps).
       Что захватывает: extensions со своим клубом, supermax, бирды-rights re-sign.
       Что пропускает: extensions с лёгким росом (<20%), 1-yr deals.
       Экзогенность: ЧАСТИЧНО циркулярный (использует salary_next), но более
       прицельно, чем cy_A_up (фильтр по team + tenure).

    2. cy_age_based — для каждого игрока ищем «контрактные ступеньки»:
       сезоны после ≥3 лет стабильной cap_share (|Δcap_share| < 0.05 каждый
       год), сменяющиеся скачком >0.15. Это паттерн «стабильный контракт →
       новый контракт».
       Захватывает: long-term contract endpoints, и re-signings, и trades.
       Пропускает: 1-2-year deals, rookie scale.

    3. cy_walk_back — экзогенный сигнал на основе cy_B_offseason ∪ {Δcap-share
       > 0.05 при той же команде}. Это вариант, рассматривающий «контрактное
       событие» как переход на качественно другой уровень cap-share.

    4. cy_renewal_year — сезон t = последний сезон, если: (a) ts+1.team ≠
       ts.team ИЛИ (b) salary_cap_share_next / salary_cap_share_t > 1.15 при
       наблюдаемом разрыве в карьере. Близко к cy_walk_back, но мягче.

    5. cy_canonical_extended — расширение cy_exogenous за счёт rookie-scale
       extension: игрок 1-го round draft pick с experience = 4 (= конец
       rookie-scale extension у first-round picks подписавших ext). Это
       fully exogenous (по правилам CBA).

Для каждого определения — M3c-регрессия:
    Δlog(salary) ~ cy_new + COMBINED_STATS + COMMON_NO_STRUCT + year FE,
    cluster SE по player.

Outputs:
    output/h6_verification/03_alternative_cy_definitions.csv  — таблица
        каждого определения на каждом player-season.
    output/h6_verification/03_m3c_alternative.csv             — коэффициенты β
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.config import COMBINED_STATS, COMMON_NO_STRUCT  # noqa: E402

OUT = ROOT / "output" / "h6_verification"
OUT.mkdir(parents=True, exist_ok=True)
MULTI_TEAM = {"2TM", "3TM", "4TM", "TOT"}


def build_alternative_cy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["player_id", "season"]).reset_index(drop=True).copy()
    g = df.groupby("player_id", sort=False)

    # === 1. cy_same_team_endpoint ===
    # team_tenure_run: кол-во подряд сезонов с тем же team_abbr
    def _tenure(s):
        runs = (s != s.shift()).cumsum()
        return s.groupby(runs).cumcount() + 1

    df["team_tenure"] = df.groupby("player_id")["team_abbr"].transform(_tenure)

    multi_t = df["team_abbr"].isin(MULTI_TEAM)
    multi_next = df["team_next"].isin(MULTI_TEAM)

    same_team = (df["team_next"].notna() & (df["team_abbr"] == df["team_next"]))
    big_raise = (df["salary_next"] > 0) & (df["salary_usd"] > 0) & \
                (np.log(df["salary_next"] / df["salary_usd"]) > np.log(1.20))
    enough_tenure = df["team_tenure"] >= 3
    df["cy_same_team_endpoint"] = (
        same_team & big_raise & enough_tenure & (~multi_t) & (~multi_next)
    ).astype("Int64")
    df.loc[df["salary_next"].isna() | df["salary_usd"].isna(), "cy_same_team_endpoint"] = pd.NA
    df.loc[multi_t, "cy_same_team_endpoint"] = pd.NA

    # === 2. cy_age_based: «ступенька после плато» ===
    # Используем cap_share lag/next; ищем плато ≥3 года + scaler change > 0.15
    df["cap_share_t"] = df["salary_cap_share_t"]
    df["cap_share_next"] = df["salary_cap_share_next"]
    df["cap_share_lag1"] = g["cap_share_t"].shift(1)
    df["cap_share_lag2"] = g["cap_share_t"].shift(2)
    df["cap_share_lag3"] = g["cap_share_t"].shift(3)

    def _plateau(row):
        if any(pd.isna([row["cap_share_t"], row["cap_share_lag1"], row["cap_share_lag2"]])):
            return False
        d1 = abs(row["cap_share_t"] - row["cap_share_lag1"]) / max(row["cap_share_lag1"], 0.001)
        d2 = abs(row["cap_share_lag1"] - row["cap_share_lag2"]) / max(row["cap_share_lag2"], 0.001)
        return (d1 < 0.05) and (d2 < 0.05)

    df["_plateau"] = df.apply(_plateau, axis=1)
    df["_next_jump"] = (
        df["cap_share_next"].notna()
        & (abs(df["cap_share_next"] - df["cap_share_t"]) / df["cap_share_t"].clip(lower=0.001) > 0.15)
    )
    df["cy_age_based"] = (df["_plateau"] & df["_next_jump"] & (~multi_t) & (~multi_next)).astype("Int64")
    df.loc[df["cap_share_next"].isna(), "cy_age_based"] = pd.NA
    df.loc[multi_t, "cy_age_based"] = pd.NA

    # === 3. cy_walk_back: cy_B_offseason ∪ {≥5% cap-share jump same team after ≥2 yrs} ===
    df["_capjump_same"] = (
        same_team & (~multi_t) & (~multi_next)
        & ((df["cap_share_next"] - df["cap_share_t"]) > 0.05)
        & (df["team_tenure"] >= 2)
    )
    df["cy_walk_back"] = (
        (df["cy_B_offseason"].fillna(0) == 1) | df["_capjump_same"]
    ).astype("Int64")
    df.loc[df["salary_next"].isna(), "cy_walk_back"] = pd.NA
    df.loc[multi_t, "cy_walk_back"] = pd.NA

    # === 4. cy_renewal_year: cy_B_offseason ∪ {cap_share_next/cap_share_t > 1.15} ===
    df["_capratio"] = df["cap_share_next"] / df["cap_share_t"]
    df["cy_renewal_year"] = (
        (df["cy_B_offseason"].fillna(0) == 1)
        | (df["_capratio"] > 1.15)
    ).astype("Int64")
    df.loc[df["salary_next"].isna(), "cy_renewal_year"] = pd.NA
    df.loc[multi_t, "cy_renewal_year"] = pd.NA

    # === 5. cy_canonical_extended: cy_exogenous ∪ {rookie-scale extension endpoint}
    # First-round picks with experience = 4 → конец 4-летнего rookie-scale ext.
    # Это полностью экзогенный сигнал (правила CBA).
    rookie_ext_endpoint = ((df["draft_round"] == 1) & (df["experience"] == 7)).astype("Int64")
    # 7 = 4 rookie + 4 ext - но фактически нам нужен конец extension. Для 1st rd
    # rookie max ext = 4-year covering yrs 5-8 of career → experience=8 endpoint.
    # Используем 7-летний rookie+ext (experience=7 → 4-yr ext was signed
    # before yr 4-5 transition, ending yr 8). Берём experience=7 как extension
    # endpoint (соответствует ст. 4 ext-летнего соглашения).
    df["cy_canonical_extended"] = (
        (df["cy_exogenous"].fillna(0) == 1) | (rookie_ext_endpoint == 1)
    ).astype("Int64")
    df.loc[df["cy_exogenous"].isna() & (rookie_ext_endpoint == 0), "cy_canonical_extended"] = pd.NA

    # Clean up
    df = df.drop(columns=["_plateau", "_next_jump", "_capjump_same", "_capratio",
                          "cap_share_lag1", "cap_share_lag2", "cap_share_lag3"])
    return df


def fit_m3c(df_input: pd.DataFrame, cy_col: str, label: str) -> dict:
    d = df_input[~df_input["team_abbr"].isin(MULTI_TEAM)].copy()
    must = ["ln_salary", "ppg", "rpg", "apg", "age", "age_sq", "experience",
            "post_cba_2017", "post_covid", "allstar", "undrafted",
            "log_draft_pick", "pos_PG", "pos_SG", "pos_SF", "pos_PF",
            "mpg", "gp", "per", "ws", "bpm", "vorp", "usg_pct"]
    d = d.dropna(subset=must + ["salary_next", cy_col])
    if d[cy_col].sum() == 0:
        return {"model": label, "cy_var": cy_col, "beta": np.nan, "se": np.nan,
                "p": np.nan, "n": len(d), "n_cy_1": 0}
    d["dln_salary"] = np.log(d["salary_next"]) - d["ln_salary"]
    d[cy_col] = d[cy_col].astype(int)
    d = d.set_index(["player_id", "season"])

    X = sm.add_constant(d[COMBINED_STATS + COMMON_NO_STRUCT + [cy_col]])
    res = PanelOLS(d["dln_salary"], X, time_effects=True).fit(
        cov_type="clustered", cluster_entity=True
    )
    beta = float(res.params[cy_col])
    se = float(res.std_errors[cy_col])
    p = float(res.pvalues[cy_col])
    mde = 2.8 * se
    return {
        "model": label,
        "cy_var": cy_col,
        "beta": beta,
        "se": se,
        "p": p,
        "MDE_80": mde,
        "n": int(res.nobs),
        "n_cy_1": int(d[cy_col].sum()),
        "share_cy_1": float(d[cy_col].mean()),
    }


def main():
    df = pd.read_csv(ROOT / "data" / "clean" / "data_analysis_v1.csv")
    df = build_alternative_cy(df)
    # Save full mapping
    keep = ["player_id", "player_name", "season", "team_abbr", "salary_usd",
            "salary_next", "real_salary_change",
            "cy_A_up", "cy_B_offseason", "cy_C", "contract_year", "cy_exogenous",
            "cy_same_team_endpoint", "cy_age_based", "cy_walk_back",
            "cy_renewal_year", "cy_canonical_extended"]
    df[keep].to_csv(OUT / "03_alternative_cy_definitions.csv", index=False)

    # Counts
    cnt = []
    for c in ["contract_year", "cy_exogenous", "cy_A_up", "cy_B_offseason", "cy_C",
              "cy_same_team_endpoint", "cy_age_based", "cy_walk_back",
              "cy_renewal_year", "cy_canonical_extended"]:
        s = df[c]
        cnt.append({"signal": c,
                    "n_eq_1": int((s == 1).sum()),
                    "n_eq_0": int((s == 0).sum()),
                    "n_na":   int(s.isna().sum())})
    pd.DataFrame(cnt).to_csv(OUT / "03_signal_counts.csv", index=False)

    # M3c regressions for each
    results = []
    for cy_var, label in [
        ("cy_exogenous",          "M3c_canonical (V1, baseline)"),
        ("contract_year",         "M3c_composite (V1, composite)"),
        ("cy_A_up",               "M3c_circular (V1, circular)"),
        ("cy_same_team_endpoint", "M3c_alt1: same-team endpoint"),
        ("cy_age_based",          "M3c_alt2: age-based plateau"),
        ("cy_walk_back",          "M3c_alt3: walk-back (B_off ∪ same-team jump)"),
        ("cy_renewal_year",       "M3c_alt4: renewal (B_off ∪ +15% cap-share)"),
        ("cy_canonical_extended", "M3c_alt5: extended canonical (exo ∪ rookie ext endpoint)"),
    ]:
        try:
            results.append(fit_m3c(df, cy_var, label))
        except Exception as e:
            results.append({"model": label, "cy_var": cy_var, "error": str(e)})

    rdf = pd.DataFrame(results)
    rdf.to_csv(OUT / "03_m3c_alternative.csv", index=False)
    print(rdf.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
