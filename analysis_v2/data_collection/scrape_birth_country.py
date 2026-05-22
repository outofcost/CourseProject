"""Scrape basketball-reference player pages for birth country / city / date.

Source: https://www.basketball-reference.com/players/{letter}/{player_id}.html
Uses the project's existing http_client (curl_cffi impersonate=chrome, cached).

Output: data/clean/birth_country.csv with columns
  player_id, birth_date_bbref, birth_city, birth_country_code, birth_country, is_international.

Run:
    python3 -m analysis_v2.data_collection.scrape_birth_country
"""
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from nba_scraper.config import CLEAN_DIR  # noqa: E402
from nba_scraper.http_client import fetch  # noqa: E402

log = logging.getLogger("analysis_v2.birth_country")
LOGS_DIR = ROOT / "analysis_v2" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

PLAYER_URL = "https://www.basketball-reference.com/players/{letter}/{pid}.html"

# ISO 3166-1 alpha-2 → country name (covers all NBA-relevant countries 2015–2024).
# Source: ISO official list. Manually compiled for the subset bbref returns.
ISO_COUNTRY = {
    "us": "USA",
    "ca": "Canada",
    "fr": "France",
    "de": "Germany",
    "es": "Spain",
    "it": "Italy",
    "rs": "Serbia",
    "si": "Slovenia",
    "hr": "Croatia",
    "ba": "Bosnia and Herzegovina",
    "mk": "North Macedonia",
    "me": "Montenegro",
    "lt": "Lithuania",
    "lv": "Latvia",
    "ee": "Estonia",
    "ru": "Russia",
    "ua": "Ukraine",
    "tr": "Turkey",
    "gr": "Greece",
    "il": "Israel",
    "ch": "Switzerland",
    "at": "Austria",
    "be": "Belgium",
    "nl": "Netherlands",
    "se": "Sweden",
    "no": "Norway",
    "fi": "Finland",
    "dk": "Denmark",
    "ie": "Ireland",
    "gb": "United Kingdom",
    "uk": "United Kingdom",
    "cz": "Czech Republic",
    "pl": "Poland",
    "ro": "Romania",
    "bg": "Bulgaria",
    "hu": "Hungary",
    "br": "Brazil",
    "ar": "Argentina",
    "mx": "Mexico",
    "do": "Dominican Republic",
    "vi": "US Virgin Islands",
    "pr": "Puerto Rico",
    "ht": "Haiti",
    "cu": "Cuba",
    "jm": "Jamaica",
    "bs": "Bahamas",
    "tt": "Trinidad and Tobago",
    "ve": "Venezuela",
    "co": "Colombia",
    "cl": "Chile",
    "pe": "Peru",
    "uy": "Uruguay",
    "ng": "Nigeria",
    "cm": "Cameroon",
    "sn": "Senegal",
    "cg": "Republic of the Congo",
    "cd": "Democratic Republic of the Congo",
    "ml": "Mali",
    "tn": "Tunisia",
    "eg": "Egypt",
    "za": "South Africa",
    "sd": "Sudan",
    "ss": "South Sudan",
    "gh": "Ghana",
    "au": "Australia",
    "nz": "New Zealand",
    "jp": "Japan",
    "cn": "China",
    "tw": "Taiwan",
    "kr": "South Korea",
    "ph": "Philippines",
    "ir": "Iran",
    "lb": "Lebanon",
    "ge": "Georgia",
    "by": "Belarus",
    "ao": "Angola",
    "lc": "Saint Lucia",
    "gn": "Guinea",
    "gf": "French Guiana",
    "ag": "Antigua and Barbuda",
    "pt": "Portugal",
    "ga": "Gabon",
    "cy": "Cyprus",
    "uz": "Uzbekistan",
    "rw": "Rwanda",
    "et": "Ethiopia",
}


def _player_url(player_id: str) -> str:
    letter = player_id[0].lower()
    return PLAYER_URL.format(letter=letter, pid=player_id)


_CITY_RE = re.compile(r"in\s+([^,]+?)\s*,", re.IGNORECASE)


def _extract_country_code_from_href(href: str) -> str | None:
    """Pull `country=XX` from /friv/birthplaces.fcgi?country=XX&state=YY."""
    parsed = urlparse(href)
    qs = parse_qs(parsed.query)
    country = qs.get("country", [None])[0]
    return country.lower() if country else None


def parse_player_meta(html: str) -> dict:
    """Return {birth_date_bbref, birth_city, birth_country_code}.

    bbref 2024+ markup (post itemprop removal):
        <strong>Born: </strong>
        <span id="necro-birth" data-birth="YYYY-MM-DD">…</span>
        <span>
          in&nbsp;{City},&nbsp;<a href='/friv/birthplaces.fcgi?country=XX&state=ZZ'>…</a>
        </span>
        <span class="f-i f-xx">xx</span>
    """
    soup = BeautifulSoup(html, "lxml")
    meta = soup.find(id="meta")
    if meta is None:
        return {"birth_date_bbref": None, "birth_city": None, "birth_country_code": None}

    birth_date = None
    bd_span = meta.find("span", id="necro-birth")
    if bd_span is not None:
        birth_date = bd_span.get("data-birth") or None

    # Country: first <a> in #meta with href pointing to birthplaces.fcgi?country=XX.
    country_code = None
    for a in meta.find_all("a", href=True):
        if "/friv/birthplaces.fcgi" in a["href"] and "country=" in a["href"]:
            country_code = _extract_country_code_from_href(a["href"])
            if country_code:
                break

    # City: parse "in {City}, {Country/State}" text immediately following necro-birth.
    city = None
    if bd_span is not None:
        # The birthplace span is a sibling after the date span. Collect text within the
        # parent <p> from the end of bd_span onward.
        parent = bd_span.parent
        if parent is not None:
            tail_text = ""
            after = False
            for child in parent.children:
                if child is bd_span:
                    after = True
                    continue
                if not after:
                    continue
                tail_text += child.get_text(" ", strip=False) if hasattr(child, "get_text") else str(child)
            tail_text = re.sub(r"\xa0", " ", tail_text)
            tail_text = re.sub(r"\s+", " ", tail_text).strip()
            m = _CITY_RE.search(tail_text)
            if m:
                city = m.group(1).strip() or None

    return {
        "birth_date_bbref": birth_date,
        "birth_city": city,
        "birth_country_code": country_code,
    }


def scrape_one(player_id: str) -> dict:
    url = _player_url(player_id)
    try:
        resp = fetch(url)
    except Exception as exc:
        log.warning("FETCH FAIL %s: %s", player_id, exc)
        return {"player_id": player_id, "fetch_error": str(exc)}

    meta = parse_player_meta(resp.text)
    meta["player_id"] = player_id
    meta["fetch_error"] = None
    return meta


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    panel_path = CLEAN_DIR / "data_analysis_v1.csv"
    if not panel_path.exists():
        log.error("panel not found: %s", panel_path)
        return 1
    panel = pd.read_csv(panel_path, usecols=["player_id", "player_name"])
    players = (
        panel.dropna(subset=["player_id"])
        .drop_duplicates(subset=["player_id"])
        .sort_values("player_id")
        .reset_index(drop=True)
    )
    log.info("unique players to scrape: %d", len(players))

    rows: list[dict] = []
    for i, r in players.iterrows():
        if i % 50 == 0:
            log.info("progress: %d / %d", i, len(players))
        info = scrape_one(r["player_id"])
        info["player_name"] = r["player_name"]
        rows.append(info)

    df = pd.DataFrame(rows)
    df["birth_country"] = df["birth_country_code"].map(ISO_COUNTRY)
    df["is_international"] = (df["birth_country_code"] != "us").astype("Int64")
    df.loc[df["birth_country_code"].isna(), "is_international"] = pd.NA

    out = CLEAN_DIR / "birth_country.csv"
    df.to_csv(out, index=False)
    log.info("wrote %s (%d rows)", out, len(df))

    unmatched = df[df["birth_country_code"].isna()]
    if len(unmatched) > 0:
        upath = LOGS_DIR / "unmatched_birth_country.csv"
        unmatched.to_csv(upath, index=False)
        log.warning("unmatched: %d → %s", len(unmatched), upath)

    unknown_codes = df.loc[
        df["birth_country_code"].notna() & df["birth_country"].isna(),
        ["player_id", "player_name", "birth_country_code"],
    ]
    if len(unknown_codes) > 0:
        upath = LOGS_DIR / "unknown_country_codes.csv"
        unknown_codes.to_csv(upath, index=False)
        log.warning(
            "unknown ISO codes (extend ISO_COUNTRY map): %d → %s",
            len(unknown_codes),
            upath,
        )

    # Summary
    total = len(df)
    covered = int(df["birth_country_code"].notna().sum())
    intl = int((df["is_international"] == 1).sum())
    log.info(
        "coverage: %d/%d (%.1f%%); international: %d (%.1f%%)",
        covered,
        total,
        100 * covered / total,
        intl,
        100 * intl / total,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
