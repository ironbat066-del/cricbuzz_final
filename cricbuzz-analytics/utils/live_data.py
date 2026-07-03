"""Fetch live cricket data from RapidAPI with MySQL fallback."""

from __future__ import annotations

from typing import Any

import pandas as pd

from scraper.api_client import CricbuzzClient
from utils.helpers import read_sql


def fetch_live_from_api() -> tuple[list[dict[str, Any]], str | None]:
    try:
        client = CricbuzzClient()
        live = client.live_matches()
        recent = client.recent_matches()
        rows: list[dict[str, Any]] = []

        def extract(payload: Any, source: str) -> None:
            if isinstance(payload, dict):
                for key in ("typeMatches", "matches", "matchList"):
                    if key in payload and isinstance(payload[key], list):
                        for block in payload[key]:
                            if isinstance(block, dict) and "seriesMatches" in block:
                                for sm in block.get("seriesMatches", []):
                                    for m in sm.get("seriesAdWrapper", {}).get("matches", []):
                                        if isinstance(m, dict):
                                            info = m.get("matchInfo", m)
                                            rows.append(_normalize_match(info, source))
                            elif "matchInfo" in block:
                                rows.append(_normalize_match(block["matchInfo"], source))
                for v in payload.values():
                    extract(v, source)
            elif isinstance(payload, list):
                for item in payload:
                    extract(item, source)

        extract(live, "Live")
        extract(recent, "Recent")
        if not rows:
            return [], "API returned no matches."
        return rows, None
    except Exception as exc:
        return [], str(exc)


def _normalize_match(info: dict[str, Any], source: str) -> dict[str, Any]:
    t1 = (info.get("team1") or {}).get("teamName", "")
    t2 = (info.get("team2") or {}).get("teamName", "")
    venue = info.get("venueInfo") or {}
    return {
        "source": source,
        "match_id": info.get("matchId"),
        "match_description": info.get("matchDesc") or f"{t1} vs {t2}",
        "team1": t1,
        "team2": t2,
        "status": info.get("status") or info.get("state"),
        "format": info.get("matchFormat"),
        "venue": venue.get("ground") or venue.get("name"),
        "city": venue.get("city"),
    }


def live_matches_from_db() -> pd.DataFrame:
    return read_sql(
        """
        SELECT match_id, match_description, team1_name, team2_name,
               venue_name, city, match_date, format, winner, result_margin, result_type
        FROM matches
        WHERE match_date >= CURDATE() - INTERVAL 14 DAY
        ORDER BY match_date DESC
        """
    )


def scorecard_for_match(match_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    batting = read_sql(
        """
        SELECT player_name, batting_position, runs, balls_faced, strike_rate
        FROM batting_scorecard
        WHERE match_id = %s
        ORDER BY innings_id, batting_position
        """,
        (match_id,),
    )
    bowling = read_sql(
        """
        SELECT player_name, overs, economy, wickets
        FROM bowling_scorecard
        WHERE match_id = %s
        ORDER BY innings_id
        """,
        (match_id,),
    )
    return batting, bowling


def team_details_for_match(match_id: int) -> pd.DataFrame:
    return read_sql(
        """
        SELECT m.match_description, m.team1_name, m.team2_name, m.format,
               m.toss_winner, m.toss_decision, m.winner, m.result_margin, m.result_type,
               v.venue_name, v.city, v.country, t1.country AS team1_country, t2.country AS team2_country
        FROM matches m
        LEFT JOIN venue_country_map v ON m.venue_id = v.venue_id
        LEFT JOIN team_country_map t1 ON m.team1_name = t1.team_name
        LEFT JOIN team_country_map t2 ON m.team2_name = t2.team_name
        WHERE m.match_id = %s
        """,
        (match_id,),
    )
