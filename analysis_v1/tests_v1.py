"""§4.7 — минимальные тесты pipeline V1.

Запуск:
    pytest analysis_v1/tests_v1.py -v

Snapshot M1a (#5) добавляется после прогонки m1_v1 (§3 плана).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis.config import DATA_CLEAN  # noqa: E402

DATA_PATH = DATA_CLEAN / "data_analysis_v1.csv"


@pytest.fixture(scope="module")
def df():
    assert DATA_PATH.exists(), f"{DATA_PATH} не существует — прогоните prep_v1 + contract_year_v1"
    return pd.read_csv(DATA_PATH)


def test_vanvleet_experience(df):
    """A2 fix: VanVleet (undrafted) имеет experience 1..8 за 2017-2024."""
    vv = df[df["player_name"].str.contains("VanVleet", na=False)].sort_values("season")
    assert len(vv) == 8, f"VanVleet rows: {len(vv)}, ожидаем 8"
    assert vv["experience"].tolist() == [1, 2, 3, 4, 5, 6, 7, 8]


def test_undrafted_experience_positive(df):
    """A2 fix: ни один undrafted не имеет experience = 0."""
    und = df[df["undrafted"] == 1]
    assert (und["experience"] >= 1).all(), \
        f"{(und['experience'] == 0).sum()} undrafted всё ещё с experience=0"


def test_toronto_state_tax(df):
    """A3 fix: TOR имеет state_tax_rate ~ 0.49–0.54 для всех 107 наблюдений."""
    tor = df[df["team_abbr"] == "TOR"]
    assert len(tor) > 0, "TOR rows отсутствуют"
    assert tor["state_tax_rate"].notna().all()
    assert tor["state_tax_rate"].between(0.45, 0.56).all()
    # is_canada флаг
    assert (tor["is_canada"] == 1).all()
    assert (df.loc[df["team_abbr"] != "TOR", "is_canada"] == 0).all()


def test_cy_A_up_down_disjoint(df):
    """A1 fix: cy_A_up и cy_A_down ни на одном наблюдении одновременно ≠ 0."""
    both = ((df["cy_A_up"] == 1) & (df["cy_A_down"] == 1)).sum()
    assert both == 0, f"cy_A_up & cy_A_down пересекаются на {both} строках"


def test_contract_year_distribution(df):
    """A1 fix: contract_year=1 доля в разумных рамках (40–60%)."""
    share = (df["contract_year"] == 1).sum() / df["contract_year"].notna().sum()
    assert 0.40 <= share <= 0.60, f"contract_year=1 share = {share:.3f} вне (0.40, 0.60)"


def test_cy_exogenous_not_circular(df):
    """A1 fix: cy_exogenous слабо коррелирует с Δlog_salary (нет circularity)."""
    sub = df.dropna(subset=["salary_next", "cy_exogenous", "salary_usd"]).copy()
    sub = sub[sub["salary_usd"] > 0]
    dlog = np.log(sub["salary_next"] / sub["salary_usd"])
    corr = np.corrcoef(sub["cy_exogenous"].astype(float), dlog)[0, 1]
    assert abs(corr) < 0.30, f"corr(cy_exogenous, Δlog_salary) = {corr:.3f} ≥ 0.30"


def test_shooting_pct_flags(df):
    """C13 fix: для каждого NaN в shooting % создан no_<col>_attempts флаг."""
    flag_cols = [c for c in df.columns if c.startswith("no_") and c.endswith("_attempts")]
    assert len(flag_cols) >= 3  # минимум no_fg3_*, no_fg2_*, no_ft_*
    # 3-pt: 128 в V0, должно остаться 128.
    assert df["no_fg3_attempts"].sum() == 128


def test_data_row_count(df):
    """Sanity: после prep_v1 + contract_year_v1 ровно 3660 строк."""
    assert len(df) == 3660
