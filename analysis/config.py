"""Paths and shared constants for the analysis pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_CLEAN = ROOT / "data" / "clean"
DATA_LOOKUPS = ROOT / "data" / "lookups"
OUT_TABLES = ROOT / "output" / "tables"
OUT_FIGURES = ROOT / "output" / "figures"

OUT_TABLES.mkdir(parents=True, exist_ok=True)
OUT_FIGURES.mkdir(parents=True, exist_ok=True)

# bbref → modern abbreviations (for tax lookup JOIN)
TEAM_ABBR_FIX = {"BRK": "BKN", "CHO": "CHA", "PHO": "PHX"}

# NBA salary cap (USD) — used to deflate salary changes for the contract_year heuristic.
CAP = {
    2016: 70.0e6,   2017: 94.1e6,   2018: 99.1e6,   2019: 101.9e6,
    2020: 109.1e6,  2021: 109.1e6,  2022: 112.4e6,  2023: 123.7e6,
    2024: 136.0e6,  2025: 140.6e6,  2026: 154.6e6,
}

# Regressor groups
BASIC_STATS = ["ppg", "rpg", "apg", "spg", "bpg", "mpg", "gp",
               "fg_pct", "fg3_pct", "ft_pct"]
COMBINED_STATS = ["ppg", "rpg", "apg", "mpg", "gp",
                  "per", "ws", "vorp", "usg_pct"]
COMMON_NO_STRUCT = ["age", "age_sq", "experience", "allstar", "undrafted",
                    "log_draft_pick",
                    "pos_PG", "pos_SG", "pos_SF", "pos_PF"]
COMMON_STRUCT = COMMON_NO_STRUCT + ["post_cba_2017", "post_covid"]
# In player+year FE: age = year - birth_year is mechanically absorbed
# (age-period-cohort collinearity). Position dummies are also typically
# time-invariant per player; we keep them defensively in case the heuristic
# flips position across seasons for a few players.
COMMON_WITHIN = ["experience", "allstar",
                 "pos_PG", "pos_SG", "pos_SF", "pos_PF"]
