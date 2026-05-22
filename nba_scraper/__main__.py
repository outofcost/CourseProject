from __future__ import annotations

import argparse
import logging
import sys

from .allstar import consolidate_allstar, scrape_allstar
from .bbref import scrape_advanced, scrape_per_game
from .config import SEASONS, URLS
from .draft import DEFAULT_DRAFT_FROM, DEFAULT_DRAFT_TO, consolidate_draft, scrape_draft
from .hoopshype import scrape_salaries
from .merge import build_dataset
from .http_client import fetch
from .logging_setup import setup_logging
from .names import canonicalize_name, ensure_alias_template

log = logging.getLogger("nba_scraper.cli")


def cmd_selftest(args: argparse.Namespace) -> int:
    setup_logging()
    log.info("=== selftest start ===")

    samples = [
        ("Luka Dončić", "luka doncic"),
        ("P.J. Tucker", "pj tucker"),
        ("Kelly Oubre Jr.", "kelly oubre"),
        ("Karl-Anthony Towns", "karl anthony towns"),
        ("Glenn Robinson III", "glenn robinson"),
        ("D'Angelo Russell", "dangelo russell"),
    ]
    failures = 0
    for raw, want in samples:
        got = canonicalize_name(raw)
        status = "OK " if got == want else "FAIL"
        if got != want:
            failures += 1
        log.info("canon %s %r -> %r (want %r)", status, raw, got, want)

    ensure_alias_template()

    test_year = args.season or 2024
    markers = {
        "bbref_per_game": ('id="per_game_stats"', "<table"),
        "bbref_advanced": ('id="advanced"', "<table"),
        "hoopshype_salaries": ('"seasons"', '"salary"'),
    }
    url_to_key = {
        URLS["bbref_per_game"].format(year=test_year): "bbref_per_game",
        URLS["bbref_advanced"].format(year=test_year): "bbref_advanced",
        URLS["hoopshype_salaries"].format(start=test_year - 1, end=test_year): "hoopshype_salaries",
    }

    for url, key in url_to_key.items():
        try:
            resp = fetch(url)
            body = resp.text
            wanted = markers[key]
            ok = all(m.lower() in body.lower() for m in wanted)
            log.info(
                "fetched %s (%d chars, cache=%s) markers %s -> %s",
                url,
                len(body),
                resp.from_cache,
                wanted,
                "OK" if ok else "MISS",
            )
            if not ok:
                failures += 1
                log.error("expected markers %s not all present in %s", wanted, url)
        except Exception as exc:
            failures += 1
            log.error("fetch failed for %s: %s", url, exc)

    log.info("=== selftest done: %d failures ===", failures)
    return 0 if failures == 0 else 1


def cmd_stub(args: argparse.Namespace) -> int:
    setup_logging()
    log.error("subcommand %r not implemented yet (coming in next iteration)", args.cmd)
    return 2


def cmd_bbref(args: argparse.Namespace) -> int:
    setup_logging()
    seasons = [args.season] if args.season else list(SEASONS)
    log.info("=== bbref start: %d season(s) %s ===", len(seasons), seasons)
    failures = 0
    for season in seasons:
        try:
            pg = scrape_per_game(season)
            adv = scrape_advanced(season)
            log.info("season %d: per_game=%d rows, advanced=%d rows", season, len(pg), len(adv))
        except Exception as exc:
            failures += 1
            log.exception("season %d failed: %s", season, exc)
    log.info("=== bbref done: %d failures ===", failures)
    return 0 if failures == 0 else 1


def cmd_salaries(args: argparse.Namespace) -> int:
    setup_logging()
    seasons = [args.season] if args.season else list(SEASONS)
    log.info("=== hoopshype salaries start: %d season(s) %s ===", len(seasons), seasons)
    failures = 0
    for season in seasons:
        try:
            df = scrape_salaries(season)
            log.info("season %d: salaries=%d rows", season, len(df))
        except Exception as exc:
            failures += 1
            log.exception("season %d failed: %s", season, exc)
    log.info("=== hoopshype salaries done: %d failures ===", failures)
    return 0 if failures == 0 else 1


def cmd_draft(args: argparse.Namespace) -> int:
    setup_logging()
    year_from = args.year_from or DEFAULT_DRAFT_FROM
    year_to = args.year_to or DEFAULT_DRAFT_TO
    years = list(range(year_from, year_to + 1))
    log.info("=== draft start: years %d–%d (%d total) ===", year_from, year_to, len(years))
    failures = 0
    for y in years:
        try:
            df = scrape_draft(y)
            log.info("year %d: %d picks", y, len(df))
        except Exception as exc:
            failures += 1
            log.exception("year %d failed: %s", y, exc)
    try:
        consolidate_draft(year_from, year_to)
    except Exception as exc:
        log.exception("consolidate_draft failed: %s", exc)
        failures += 1
    log.info("=== draft done: %d failures ===", failures)
    return 0 if failures == 0 else 1


def cmd_allstar(args: argparse.Namespace) -> int:
    setup_logging()
    seasons = [args.season] if args.season else list(SEASONS)
    log.info("=== allstar start: %d season(s) %s ===", len(seasons), seasons)
    failures = 0
    for s in seasons:
        try:
            df = scrape_allstar(s)
            log.info("season %d: %d All-Stars", s, len(df))
        except Exception as exc:
            failures += 1
            log.exception("season %d failed: %s", s, exc)
    try:
        consolidate_allstar(seasons)
    except Exception as exc:
        log.exception("consolidate_allstar failed: %s", exc)
        failures += 1
    log.info("=== allstar done: %d failures ===", failures)
    return 0 if failures == 0 else 1


def cmd_merge(args: argparse.Namespace) -> int:
    setup_logging()
    try:
        build_dataset()
        return 0
    except Exception as exc:
        log.exception("build_dataset failed: %s", exc)
        return 1


def cmd_all(args: argparse.Namespace) -> int:
    setup_logging()
    log.info("=== run all stages ===")
    seasons = list(SEASONS)
    rc = 0

    for season in seasons:
        try:
            scrape_per_game(season)
            scrape_advanced(season)
        except Exception as exc:
            log.exception("bbref season=%d failed: %s", season, exc); rc = 1

    for season in seasons:
        try:
            scrape_salaries(season)
        except Exception as exc:
            log.exception("salaries season=%d failed: %s", season, exc); rc = 1

    for y in range(DEFAULT_DRAFT_FROM, DEFAULT_DRAFT_TO + 1):
        try:
            scrape_draft(y)
        except Exception as exc:
            log.exception("draft year=%d failed: %s", y, exc); rc = 1
    try:
        consolidate_draft(DEFAULT_DRAFT_FROM, DEFAULT_DRAFT_TO)
    except Exception as exc:
        log.exception("consolidate_draft failed: %s", exc); rc = 1

    for season in seasons:
        try:
            scrape_allstar(season)
        except Exception as exc:
            log.exception("allstar season=%d failed: %s", season, exc); rc = 1
    try:
        consolidate_allstar(seasons)
    except Exception as exc:
        log.exception("consolidate_allstar failed: %s", exc); rc = 1

    try:
        build_dataset()
    except Exception as exc:
        log.exception("build_dataset failed: %s", exc); rc = 1

    log.info("=== all stages done, rc=%d ===", rc)
    return rc


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="nba_scraper", description="NBA panel-data scraper")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("selftest", help="sanity-check HTTP client and name canonicalization")
    s.add_argument("--season", type=int, default=None, help="bbref season-end year (default 2024)")
    s.set_defaults(func=cmd_selftest)

    b = sub.add_parser("bbref", help="scrape per_game + advanced from basketball-reference")
    b.add_argument("--season", type=int, default=None, help="single season (year-end); default = all")
    b.set_defaults(func=cmd_bbref)

    sal = sub.add_parser("salaries", help="scrape salaries from hoopshype")
    sal.add_argument("--season", type=int, default=None, help="single season (year-end); default = all")
    sal.set_defaults(func=cmd_salaries)

    dr = sub.add_parser("draft", help="scrape draft picks from basketball-reference")
    dr.add_argument("--year-from", type=int, default=None, help=f"default {DEFAULT_DRAFT_FROM}")
    dr.add_argument("--year-to", type=int, default=None, help=f"default {DEFAULT_DRAFT_TO}")
    dr.set_defaults(func=cmd_draft)

    al = sub.add_parser("allstar", help="scrape all-star rosters from basketball-reference")
    al.add_argument("--season", type=int, default=None, help="single season (year-end); default = all")
    al.set_defaults(func=cmd_allstar)

    mg = sub.add_parser("merge", help="build merged panel dataset from data/raw/")
    mg.set_defaults(func=cmd_merge)

    al2 = sub.add_parser("all", help="run bbref + salaries + draft + allstar + merge end-to-end")
    al2.set_defaults(func=cmd_all)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
