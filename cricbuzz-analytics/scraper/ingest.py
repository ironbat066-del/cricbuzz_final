"""
Ingest Cricbuzz API data into MySQL.

Run when your RapidAPI quota is available:
    python -m scraper.ingest
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from database.connection import get_connection
from scraper.api_client import CricbuzzClient


def _walk(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _walk(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk(item)


def _parse_match_blocks(payload: Any) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for node in _walk(payload):
        if not isinstance(node, dict):
            continue
        if "matchId" in node and ("team1" in node or "matchInfo" in node):
            matches.append(node)
    return matches


def _upsert_team(cur, name: str, country: str | None = None) -> None:
    cur.execute(
        """
        INSERT INTO team_country_map (team_name, country)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE country = COALESCE(VALUES(country), country)
        """,
        (name, country or name),
    )


def _insert_match(cur, block: dict[str, Any]) -> None:
    match_id = block.get("matchId")
    if not match_id:
        return

    team1 = block.get("team1") or {}
    team2 = block.get("team2") or {}
    t1_name = team1.get("teamName") or team1.get("name") or "Team 1"
    t2_name = team2.get("teamName") or team2.get("name") or "Team 2"
    _upsert_team(cur, t1_name)
    _upsert_team(cur, t2_name)

    venue = block.get("venueInfo") or block.get("venue") or {}
    venue_id = venue.get("id") or venue.get("venueId")
    venue_name = venue.get("ground") or venue.get("name") or "Unknown Venue"
    city = venue.get("city") or ""
    country = venue.get("country") or ""

    if venue_id:
        cur.execute(
            """
            INSERT INTO venue_country_map (venue_id, venue_name, city, country, capacity)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE venue_name = VALUES(venue_name), city = VALUES(city),
                                    country = VALUES(country)
            """,
            (venue_id, venue_name, city, country, venue.get("capacity")),
        )

    match_desc = block.get("matchDesc") or block.get("seriesName") or f"{t1_name} vs {t2_name}"
    fmt = block.get("matchFormat") or block.get("format") or "ODI"
    status = block.get("status") or block.get("state") or ""
    start = block.get("startDate") or block.get("matchStartTimestamp")
    if isinstance(start, (int, float)):
        match_date = datetime.fromtimestamp(start / 1000)
    else:
        match_date = datetime.now()

    cur.execute(
        """
        INSERT INTO matches
        (match_id, match_description, team1_name, team2_name, venue_id, venue_name, city,
         match_date, format, winner, result_margin, result_type, toss_winner, toss_decision)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE match_description = VALUES(match_description),
                                winner = VALUES(winner),
                                result_margin = VALUES(result_margin),
                                result_type = VALUES(result_type)
        """,
        (
            match_id,
            match_desc,
            t1_name,
            t2_name,
            venue_id,
            venue_name,
            city,
            match_date,
            fmt,
            block.get("winner"),
            block.get("margin"),
            block.get("marginType") or block.get("resultType"),
            block.get("tossWinner"),
            block.get("tossDecision"),
        ),
    )


def ingest_recent_and_live() -> int:
    client = CricbuzzClient()
    conn = get_connection()
    cur = conn.cursor()
    count = 0

    for fetch in (client.recent_matches, client.live_matches):
        payload = fetch()
        for block in _parse_match_blocks(payload):
            _insert_match(cur, block)
            count += 1

    conn.commit()
    cur.close()
    conn.close()
    return count


def run_ingestion() -> None:
    try:
        inserted = ingest_recent_and_live()
        print(f"Ingestion complete. Processed {inserted} match blocks.")
    except RuntimeError as exc:
        print(exc)
        print("Using seed data instead: python -m database.init_db")


if __name__ == "__main__":
    run_ingestion()
