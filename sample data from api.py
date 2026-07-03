"""Load sample cricket data into MySQL for development and demo queries."""

from __future__ import annotations

from datetime import datetime, timedelta

from database.connection import get_connection

TEAMS = [
    ("India", "India"),
    ("Australia", "Australia"),
    ("England", "England"),
    ("Pakistan", "Pakistan"),
    ("South Africa", "South Africa"),
    ("New Zealand", "New Zealand"),
]

VENUES = [
    (1, "Wankhede Stadium", "Mumbai", "India", 33108),
    (2, "Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    (3, "Lord's", "London", "England", 31100),
    (4, "Eden Gardens", "Kolkata", "India", 68000),
    (5, "The Oval", "London", "England", 25500),
    (6, "Sydney Cricket Ground", "Sydney", "Australia", 48000),
    (7, "Newlands", "Cape Town", "South Africa", 25000),
    (8, "Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    (9, "Basin Reserve", "Wellington", "New Zealand", 12000),
    (10, "Narendra Modi Stadium", "Ahmedabad", "India", 132000),
]

INDIA_PLAYERS = [
    ("Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium"),
    ("Rohit Sharma", "India", "Batsman", "Right-hand bat", None),
    ("Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
    ("Ravindra Jadeja", "India", "All-rounder", "Left-hand bat", "Left-arm orthodox"),
    ("KL Rahul", "India", "Wicket-keeper", "Right-hand bat", None),
    ("Hardik Pandya", "India", "All-rounder", "Right-hand bat", "Right-arm medium-fast"),
    ("Rishabh Pant", "India", "Wicket-keeper", "Left-hand bat", None),
    ("Mohammed Shami", "India", "Bowler", "Right-hand bat", "Right-arm fast-medium"),
]

OTHER_PLAYERS = [
    ("Steve Smith", "Australia", "Batsman", "Right-hand bat", "Right-arm legbreak"),
    ("Pat Cummins", "Australia", "All-rounder", "Right-hand bat", "Right-arm fast"),
    ("Joe Root", "England", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    ("Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
    ("Babar Azam", "Pakistan", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    ("Shaheen Afridi", "Pakistan", "Bowler", "Left-hand bat", "Left-arm fast"),
    ("Quinton de Kock", "South Africa", "Wicket-keeper", "Left-hand bat", None),
    ("Kagiso Rabada", "South Africa", "Bowler", "Left-hand bat", "Right-arm fast"),
    ("Kane Williamson", "New Zealand", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    ("Trent Boult", "New Zealand", "Bowler", "Right-hand bat", "Left-arm fast-medium"),
]

FORMAT_STATS = [
    ("Virat Kohli", "ODI", 13848, 4, 50, 295, 58.67, 93.25, 0, 0),
    ("Rohit Sharma", "ODI", 10866, 2, 31, 265, 49.17, 90.31, 0, 0),
    ("Joe Root", "Test", 12847, 0, 35, 147, 49.41, 55.20, 0, 0),
    ("Joe Root", "ODI", 6207, 0, 5, 170, 44.25, 87.50, 0, 0),
    ("Joe Root", "T20I", 893, 0, 0, 32, 27.90, 126.30, 0, 0),
    ("Steve Smith", "Test", 9685, 0, 32, 116, 56.75, 54.10, 0, 0),
    ("Steve Smith", "ODI", 4939, 0, 12, 155, 44.50, 87.20, 0, 0),
    ("Steve Smith", "T20I", 590, 0, 0, 28, 29.50, 127.00, 0, 0),
    ("Ravindra Jadeja", "Test", 2800, 280, 2, 72, 35.50, 52.00, 32.50, 2.45),
    ("Ravindra Jadeja", "ODI", 2756, 220, 0, 198, 32.10, 87.80, 36.20, 4.65),
    ("Ben Stokes", "Test", 6368, 197, 12, 105, 36.40, 58.90, 31.80, 3.20),
    ("Ben Stokes", "ODI", 3200, 74, 3, 120, 38.50, 93.40, 42.10, 5.10),
    ("Pat Cummins", "Test", 1200, 250, 0, 65, 22.00, 45.00, 22.50, 3.10),
    ("Pat Cummins", "ODI", 450, 120, 0, 95, 18.50, 72.00, 28.40, 5.20),
    ("Jasprit Bumrah", "ODI", 89, 145, 0, 89, 12.50, 65.00, 24.30, 4.65),
    ("Jasprit Bumrah", "T20I", 12, 78, 0, 70, 8.00, 80.00, 18.50, 6.50),
    ("Hardik Pandya", "ODI", 1774, 89, 1, 92, 33.20, 112.50, 38.90, 5.45),
    ("Hardik Pandya", "T20I", 967, 42, 0, 68, 28.40, 145.20, 35.00, 8.10),
    ("Babar Azam", "ODI", 5729, 0, 19, 118, 56.72, 89.40, 0, 0),
    ("Babar Azam", "T20I", 4222, 0, 9, 128, 41.80, 129.20, 0, 0),
    ("Kane Williamson", "Test", 8732, 0, 32, 101, 54.90, 51.80, 0, 0),
    ("Kane Williamson", "ODI", 6173, 0, 13, 161, 47.50, 81.60, 0, 0),
    ("Kane Williamson", "T20I", 2465, 0, 0, 87, 33.20, 123.40, 0, 0),
]

FIELDING = [
    ("Ravindra Jadeja", 160, 0, 45),
    ("Virat Kohli", 175, 0, 12),
    ("KL Rahul", 85, 0, 8),
    ("Rishabh Pant", 45, 120, 15),
    ("Quinton de Kock", 220, 0, 18),
    ("Joe Root", 195, 0, 22),
    ("Ben Stokes", 110, 0, 35),
]


def _recent(days_ago: int) -> datetime:
    return datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) - timedelta(
        days=days_ago
    )


MATCHES = [
    ("India vs Australia, 3rd ODI", "India", "Australia", 4, "Eden Gardens", "Kolkata", _recent(1), "ODI", "India", "6", "wickets", "India", "bat", "India tour of Australia ODI Series 2026"),
    ("England vs Pakistan, 2nd T20I", "England", "Pakistan", 3, "Lord's", "London", _recent(2), "T20I", "England", "24", "runs", "England", "field", "England vs Pakistan T20 Series 2026"),
    ("South Africa vs New Zealand, 1st Test", "South Africa", "New Zealand", 7, "Newlands", "Cape Town", _recent(3), "Test", "South Africa", "156", "runs", "South Africa", "bat", "South Africa vs New Zealand Test Series 2026"),
    ("India vs England, 1st ODI", "India", "England", 10, "Narendra Modi Stadium", "Ahmedabad", _recent(4), "ODI", "India", "43", "runs", "India", "field", "India tour of Australia ODI Series 2026"),
    ("Australia vs Pakistan, 2nd Test", "Australia", "Pakistan", 2, "Melbourne Cricket Ground", "Melbourne", _recent(5), "Test", "Australia", "3", "wickets", "Australia", "bat", "Border-Gavaskar Trophy 2024"),
    ("India vs New Zealand, 3rd T20I", "India", "New Zealand", 1, "Wankhede Stadium", "Mumbai", _recent(6), "T20I", "India", "8", "wickets", "New Zealand", "field", "South Africa vs New Zealand Test Series 2026"),
    ("England vs Australia, 5th Test", "England", "Australia", 5, "The Oval", "London", _recent(45), "Test", "Australia", "49", "runs", "England", "bat", "Border-Gavaskar Trophy 2024"),
    ("India vs Pakistan, Asia Cup Final", "India", "Pakistan", 8, "Gaddafi Stadium", "Lahore", _recent(60), "ODI", "India", "4", "wickets", "Pakistan", "field", "India in England ODI Series 2023"),
    ("India vs Australia, 1st Test 2024", "India", "Australia", 10, "Narendra Modi Stadium", "Ahmedabad", datetime(2024, 3, 10, 9, 30), "Test", "India", "280", "runs", "India", "bat", "Border-Gavaskar Trophy 2024"),
    ("India vs Australia, 2nd Test 2024", "India", "Australia", 4, "Eden Gardens", "Kolkata", datetime(2024, 3, 18, 9, 30), "Test", "Australia", "6", "wickets", "Australia", "field", "Border-Gavaskar Trophy 2024"),
    ("India vs Australia, 3rd Test 2024", "India", "Australia", 1, "Wankhede Stadium", "Mumbai", datetime(2024, 3, 25, 9, 30), "Test", "India", "120", "runs", "India", "bat", "Border-Gavaskar Trophy 2024"),
    ("India vs Australia, 4th Test 2024", "India", "Australia", 10, "Narendra Modi Stadium", "Ahmedabad", datetime(2024, 4, 2, 9, 30), "Test", "Australia", "3", "wickets", "Australia", "field", "Border-Gavaskar Trophy 2024"),
    ("India vs Australia, 5th Test 2024", "India", "Australia", 4, "Eden Gardens", "Kolkata", datetime(2024, 4, 10, 9, 30), "Test", "India", "35", "runs", "India", "bat", "Border-Gavaskar Trophy 2024"),
    ("England vs India, 1st ODI 2023", "England", "India", 3, "Lord's", "London", datetime(2023, 7, 12, 10, 30), "ODI", "India", "2", "wickets", "England", "bat", "India in England ODI Series 2023"),
    ("England vs India, 2nd ODI 2023", "England", "India", 5, "The Oval", "London", datetime(2023, 7, 15, 10, 30), "ODI", "England", "18", "runs", "India", "field", "India in England ODI Series 2023"),
    ("England vs India, 3rd ODI 2023", "England", "India", 3, "Lord's", "London", datetime(2023, 7, 19, 10, 30), "ODI", "India", "5", "wickets", "England", "bat", "India in England ODI Series 2023"),
    ("India vs Australia, 1st ODI 2023", "India", "Australia", 1, "Wankhede Stadium", "Mumbai", datetime(2023, 9, 22, 14, 0), "ODI", "Australia", "66", "runs", "India", "field", "India vs Australia ODI Series 2023"),
    ("India vs Australia, 2nd ODI 2023", "India", "Australia", 4, "Eden Gardens", "Kolkata", datetime(2023, 9, 25, 14, 0), "ODI", "India", "99", "runs", "Australia", "bat", "India vs Australia ODI Series 2023"),
    ("India vs Australia, 3rd ODI 2023", "India", "Australia", 10, "Narendra Modi Stadium", "Ahmedabad", datetime(2023, 9, 28, 14, 0), "ODI", "India", "7", "wickets", "India", "field", "India vs Australia ODI Series 2023"),
    ("India vs Australia, 1st T20I 2024", "India", "Australia", 6, "Sydney Cricket Ground", "Sydney", datetime(2024, 11, 20, 19, 0), "T20I", "India", "11", "runs", "Australia", "field", "India vs Australia T20 Series 2024"),
    ("India vs Australia, 2nd T20I 2024", "India", "Australia", 2, "Melbourne Cricket Ground", "Melbourne", datetime(2024, 11, 23, 19, 0), "T20I", "Australia", "4", "wickets", "India", "bat", "India vs Australia T20 Series 2024"),
    ("India vs Australia, 3rd T20I 2024", "India", "Australia", 6, "Sydney Cricket Ground", "Sydney", datetime(2024, 11, 26, 19, 0), "T20I", "India", "3", "wickets", "India", "field", "India vs Australia T20 Series 2024"),
    ("India vs Australia, 4th T20I 2024", "India", "Australia", 2, "Melbourne Cricket Ground", "Melbourne", datetime(2024, 11, 29, 19, 0), "T20I", "Australia", "6", "wickets", "Australia", "bat", "India vs Australia T20 Series 2024"),
    ("India vs Australia, 5th T20I 2024", "India", "Australia", 1, "Wankhede Stadium", "Mumbai", datetime(2024, 12, 3, 19, 0), "T20I", "India", "15", "runs", "India", "field", "India vs Australia T20 Series 2024"),
    ("South Africa vs England, 1st ODI", "South Africa", "England", 7, "Newlands", "Cape Town", datetime(2025, 1, 15, 13, 0), "ODI", "South Africa", "45", "runs", "England", "bat", "South Africa vs England ODI Series 2025"),
    ("South Africa vs England, 2nd ODI", "South Africa", "England", 7, "Newlands", "Cape Town", datetime(2025, 1, 18, 13, 0), "ODI", "England", "3", "wickets", "South Africa", "field", "South Africa vs England ODI Series 2025"),
]

SERIES = [
    ("India tour of Australia ODI Series 2026", "Australia", "ODI", datetime(2026, 6, 20).date(), 3),
    ("England vs Pakistan T20 Series 2026", "England", "T20I", datetime(2026, 6, 18).date(), 3),
    ("South Africa vs New Zealand Test Series 2026", "South Africa", "Test", datetime(2026, 6, 15).date(), 2),
    ("Border-Gavaskar Trophy 2024", "India", "Test", datetime(2024, 3, 1).date(), 5),
    ("India in England ODI Series 2023", "England", "ODI", datetime(2023, 7, 1).date(), 3),
    ("India vs Australia ODI Series 2023", "India", "ODI", datetime(2023, 9, 1).date(), 3),
    ("India vs Australia T20 Series 2024", "India", "T20I", datetime(2024, 11, 15).date(), 5),
    ("South Africa vs England ODI Series 2025", "South Africa", "ODI", datetime(2025, 1, 10).date(), 3),
]


def seed() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in (
        "partnerships",
        "fielding_stats",
        "bowling_scorecard",
        "batting_scorecard",
        "player_format_stats",
        "matches",
        "series",
        "players",
        "venue_country_map",
        "team_country_map",
    ):
        cur.execute(f"TRUNCATE TABLE {table}")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")

    cur.executemany(
        "INSERT INTO team_country_map (team_name, country) VALUES (%s, %s)", TEAMS
    )
    cur.executemany(
        "INSERT INTO venue_country_map (venue_id, venue_name, city, country, capacity) VALUES (%s,%s,%s,%s,%s)",
        VENUES,
    )
    cur.executemany(
        "INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style) VALUES (%s,%s,%s,%s,%s)",
        INDIA_PLAYERS + OTHER_PLAYERS,
    )
    cur.executemany(
        "INSERT INTO series (series_name, host_country, match_type, start_date, total_matches_planned) VALUES (%s,%s,%s,%s,%s)",
        SERIES,
    )

    series_ids = {}
    cur.execute("SELECT series_id, series_name FROM series")
    for sid, name in cur.fetchall():
        series_ids[name] = sid

    match_rows = []
    for m in MATCHES:
        desc, t1, t2, vid, vname, city, dt, fmt, winner, margin, rtype, toss_w, toss_d, sname = m
        match_rows.append(
            (desc, t1, t2, vid, vname, city, dt, fmt, winner, margin, rtype, toss_w, toss_d, series_ids[sname])
        )

    cur.executemany(
        """INSERT INTO matches
        (match_description, team1_name, team2_name, venue_id, venue_name, city, match_date,
         format, winner, result_margin, result_type, toss_winner, toss_decision, series_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        match_rows,
    )

    cur.executemany(
        """INSERT INTO player_format_stats
        (player_name, format, runs, wickets, centuries, matches_played, batting_average, strike_rate, bowling_average, economy_rate)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        FORMAT_STATS,
    )

    cur.executemany(
        "INSERT INTO fielding_stats (player_name, catches, stumpings, run_outs) VALUES (%s,%s,%s,%s)",
        FIELDING,
    )

    cur.execute("SELECT match_id, format FROM matches ORDER BY match_id")
    match_meta = cur.fetchall()

    batting_rows = []
    bowling_rows = []
    partnership_rows = []

    score_templates = [
        ("Virat Kohli", 1, 78, 62, 125.80),
        ("Rohit Sharma", 2, 65, 48, 135.40),
        ("Ravindra Jadeja", 7, 45, 38, 118.40),
        ("Steve Smith", 3, 92, 110, 83.60),
        ("Joe Root", 4, 55, 72, 76.30),
        ("Ben Stokes", 5, 88, 76, 115.80),
        ("Babar Azam", 2, 72, 58, 124.10),
        ("Kane Williamson", 3, 48, 52, 92.30),
        ("Jasprit Bumrah", 11, 8, 12, 66.70),
        ("Pat Cummins", 10, 22, 18, 122.20),
    ]

    for idx, (mid, fmt) in enumerate(match_meta):
        innings = 1 + (idx % 2)
        for pos, (pname, bpos, runs, balls, sr) in enumerate(score_templates, start=1):
            batting_rows.append((mid, innings, pname, fmt, bpos, runs + (idx % 5) * 3, balls, sr))

        for pname, overs, econ, wkts in [
            ("Jasprit Bumrah", 10.0, 4.25, 3),
            ("Pat Cummins", 9.0, 5.10, 2),
            ("Ravindra Jadeja", 8.0, 4.85, 1),
            ("Shaheen Afridi", 10.0, 5.45, 2),
            ("Kagiso Rabada", 9.5, 4.95, 2),
        ]:
            bowling_rows.append((mid, innings, pname, overs, econ, wkts))

        partnership_rows.append(
            ("Virat Kohli", "Rohit Sharma", 1, 2, 105 + (idx % 20))
        )
        partnership_rows.append(
            ("Joe Root", "Ben Stokes", 4, 5, 62 + (idx % 15))
        )
        if idx % 3 == 0:
            partnership_rows.append(
                ("Steve Smith", "Pat Cummins", 3, 4, 118 + idx)
            )

    cur.executemany(
        """INSERT INTO batting_scorecard
        (match_id, innings_id, player_name, format, batting_position, runs, balls_faced, strike_rate)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        batting_rows,
    )
    cur.executemany(
        """INSERT INTO bowling_scorecard
        (match_id, innings_id, player_name, overs, economy, wickets)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        bowling_rows,
    )

    full_partnerships = [
        (mid, 1, b1, b2, p1, p2, pr)
        for mid, _ in match_meta
        for b1, b2, p1, p2, pr in partnership_rows[:3]
    ]
    cur.executemany(
        """INSERT INTO partnerships
        (match_id, innings_id, batter1_name, batter2_name, batter1_position, batter2_position, partnership_runs)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        full_partnerships,
    )

    extra_batting = []
    extra_bowling = []
    key_players = ["Virat Kohli", "Joe Root", "Steve Smith", "Ravindra Jadeja", "Jasprit Bumrah"]
    for i, (mid, fmt) in enumerate(match_meta):
        dt_row = MATCHES[i][6]
        for j, pname in enumerate(key_players):
            extra_batting.append(
                (mid, 1, pname, fmt, j + 1, 30 + (i * 3) + j, 40 + j, 90.0 + j)
            )
            if pname in ("Jasprit Bumrah", "Ravindra Jadeja"):
                extra_bowling.append((mid, 1, pname, 5.0 + (j % 3), 4.5 + (j * 0.1), 1 + (i % 3)))

    cur.executemany(
        """INSERT INTO batting_scorecard
        (match_id, innings_id, player_name, format, batting_position, runs, balls_faced, strike_rate)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        extra_batting,
    )
    if extra_bowling:
        cur.executemany(
            """INSERT INTO bowling_scorecard
            (match_id, innings_id, player_name, overs, economy, wickets)
            VALUES (%s,%s,%s,%s,%s,%s)""",
            extra_bowling,
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Seeded {len(match_rows)} matches, {len(INDIA_PLAYERS + OTHER_PLAYERS)} players.")


if __name__ == "__main__":
    seed()
