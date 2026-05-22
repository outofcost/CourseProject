"""Подключение альтернативных cy-сигналов из Этапа 3 в текущий датасет.

Использует уже посчитанные `03_alternative_cy_definitions.csv`. Если файл
отсутствует — пересчитывает.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

ALT_CSV = ROOT / "output" / "h6_verification" / "03_alternative_cy_definitions.csv"
ALT_COLS = ["cy_same_team_endpoint", "cy_age_based", "cy_walk_back",
            "cy_renewal_year", "cy_canonical_extended"]


def attach_alt_cy(df: pd.DataFrame) -> pd.DataFrame:
    if not ALT_CSV.exists():
        from analysis_v1.h6_verification import build_alternative_cy
        alt = build_alternative_cy(df.copy())
    else:
        alt = pd.read_csv(ALT_CSV)
    keep = ["player_id", "season"] + ALT_COLS
    alt = alt[keep]
    out = df.merge(alt, on=["player_id", "season"], how="left")
    return out
