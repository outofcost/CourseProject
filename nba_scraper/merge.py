from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from .config import CLEAN_DIR, LOGS_DIR, MIN_GP, MIN_SALARY, RAW_DIR, SEASONS

log = logging.getLogger("nba_scraper.merge")

PER_GAME_PATTERN = "per_game_{season}.csv"
ADVANCED_PATTERN = "advanced_{season}.csv"
SALARIES_PATTERN = "salaries_{season}.csv"

POST_CBA_SEASON = 2018
POST_COVID_SEASON = 2021
UNMATCHED_WARN_THRESHOLD = 0.10


def _load_concat(pattern: str, seasons: list[int]) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    missing: list[int] = []
    for s in seasons:
        p = RAW_DIR / pattern.format(season=s)
        if not p.exists():
            missing.append(s)
            continue
        parts.append(pd.read_csv(p))
    if missing:
        log.warning("missing %d files for pattern %s: %s", len(missing), pattern, missing)
    if not parts:
        raise RuntimeError(f"no CSVs found for {pattern}")
    return pd.concat(parts, ignore_index=True)


def _log_unmatched(
    label: str,
    df: pd.DataFrame,
    total_left: int,
    expected_by_design: bool = False,
) -> None:
    if df.empty:
        log.info("[%s] all rows matched", label)
        return
    pct = len(df) / total_left if total_left else 0.0
    level = logging.WARNING if (pct >= UNMATCHED_WARN_THRESHOLD and not expected_by_design) else logging.INFO
    log.log(
        level,
        "[%s] %d unmatched rows (%.1f%% of %d)%s — saved sample to logs/",
        label, len(df), 100 * pct, total_left,
        " [by design]" if expected_by_design else "",
    )
    sample = df.head(200)
    out = LOGS_DIR / f"unmatched_{label}.csv"
    sample.to_csv(out, index=False)


def build_dataset(seasons: list[int] | None = None) -> pd.DataFrame:
    seasons = seasons or list(SEASONS)
    log.info("=== build_dataset: seasons %s ===", seasons)

    pg = _load_concat(PER_GAME_PATTERN, seasons)
    adv = _load_concat(ADVANCED_PATTERN, seasons)
    sal = _load_concat(SALARIES_PATTERN, seasons)
    log.info("loaded: per_game=%d, advanced=%d, salaries=%d", len(pg), len(adv), len(sal))

    adv_for_merge = adv.drop(
        columns=[c for c in ["player_name", "player_clean", "team_abbr", "position", "age", "gp"]
                 if c in adv.columns]
    )
    stats = pg.merge(
        adv_for_merge,
        on=["player_id", "season"],
        how="left",
        indicator=True,
    )
    only_pg = stats[stats["_merge"] == "left_only"]
    _log_unmatched("per_game_without_advanced", only_pg[["player_id", "player_clean", "player_name", "season"]], len(pg))
    stats = stats.drop(columns=["_merge"])

    pg_keys = pg.set_index(["player_id", "season"]).index
    adv_keys = adv.set_index(["player_id", "season"]).index
    only_adv_mask = ~adv_keys.isin(pg_keys)
    if only_adv_mask.any():
        only_adv_df = adv.loc[only_adv_mask, ["player_id", "player_clean", "player_name", "season"]]
        _log_unmatched("advanced_without_per_game", only_adv_df, len(adv), expected_by_design=True)

    stats_out = CLEAN_DIR / "stats_all.csv"
    stats.to_csv(stats_out, index=False)
    log.info("wrote %s (%d rows)", stats_out, len(stats))

    sal_for_merge = sal.drop(
        columns=[c for c in ["player_name", "player_slug_hh"] if c in sal.columns]
    )
    merged = stats.merge(
        sal_for_merge,
        on=["player_clean", "season"],
        how="left",
        indicator=True,
    )
    no_salary = merged[merged["_merge"] == "left_only"]
    _log_unmatched(
        "stats_without_salary",
        no_salary[["player_id", "player_clean", "player_name", "season", "team_abbr", "gp"]],
        len(stats),
    )
    merged = merged.drop(columns=["_merge"])

    stats_keys = stats.set_index(["player_clean", "season"]).index
    sal_keys = sal.set_index(["player_clean", "season"]).index
    salary_orphans_mask = ~sal_keys.isin(stats_keys)
    if salary_orphans_mask.any():
        salary_orphans = sal.loc[salary_orphans_mask, ["player_clean", "player_name", "season", "salary_usd"]]
        _log_unmatched("salary_without_stats", salary_orphans, len(sal), expected_by_design=True)

    sal_out = CLEAN_DIR / "salaries_all.csv"
    sal.to_csv(sal_out, index=False)
    log.info("wrote %s (%d rows)", sal_out, len(sal))

    draft_path = CLEAN_DIR / "draft_picks.csv"
    if draft_path.exists():
        draft = pd.read_csv(draft_path)
        draft_for_merge = draft[["player_id", "draft_year", "draft_round", "draft_pick", "draft_team", "college"]]
        merged = merged.merge(draft_for_merge, on="player_id", how="left")
        log.info("joined draft: %d rows, %d with draft_pick", len(merged), merged["draft_pick"].notna().sum())
        merged["undrafted"] = merged["draft_pick"].isna().astype(int)
    else:
        log.warning("draft_picks.csv missing — skipping draft join")
        merged["undrafted"] = np.nan

    allstar_path = CLEAN_DIR / "allstar_all.csv"
    if allstar_path.exists():
        allstar = pd.read_csv(allstar_path)
        allstar_for_merge = allstar[["player_id", "season", "allstar"]].drop_duplicates(
            subset=["player_id", "season"]
        )
        merged = merged.merge(allstar_for_merge, on=["player_id", "season"], how="left")
        merged["allstar"] = merged["allstar"].fillna(0).astype(int)
        log.info("joined allstar: %d AS player-seasons matched", int(merged["allstar"].sum()))
    else:
        log.warning("allstar_all.csv missing — skipping allstar join")
        merged["allstar"] = 0

    before = len(merged)
    merged = merged.dropna(subset=["salary_usd"]).copy()
    merged = merged[(merged["gp"] >= MIN_GP) & (merged["salary_usd"] > MIN_SALARY)].copy()
    log.info("filter GP>=%d AND salary_usd>%d: %d -> %d", MIN_GP, MIN_SALARY, before, len(merged))

    merged["ln_salary"] = np.log(merged["salary_usd"])
    merged["age_sq"] = merged["age"] ** 2
    merged["post_cba_2017"] = (merged["season"] >= POST_CBA_SEASON).astype(int)
    merged["post_covid"] = (merged["season"] >= POST_COVID_SEASON).astype(int)
    merged["experience"] = merged["season"] - merged["draft_year"]

    merged = merged.sort_values(["season", "salary_usd"], ascending=[True, False]).reset_index(drop=True)

    out_path = CLEAN_DIR / "data_merged.csv"
    merged.to_csv(out_path, index=False)
    log.info("wrote %s (%d rows, %d cols)", out_path, len(merged), merged.shape[1])

    _print_summary(merged)
    return merged


def _print_summary(df: pd.DataFrame) -> None:
    log.info("--- summary by season ---")
    grp = df.groupby("season").agg(
        n=("player_id", "size"),
        salary_median=("salary_usd", "median"),
        salary_max=("salary_usd", "max"),
        allstars=("allstar", "sum"),
    )
    for season, row in grp.iterrows():
        log.info(
            "  %d: n=%d, salary median=$%s, max=$%s, AS=%d",
            int(season), int(row["n"]),
            f"{row['salary_median']:,.0f}", f"{row['salary_max']:,.0f}",
            int(row["allstars"]),
        )
    log.info("total rows: %d", len(df))
