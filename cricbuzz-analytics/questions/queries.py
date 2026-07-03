import sqlite3
import pandas as pd

# ----------------------------
# 1. DB connection
# ----------------------------
def get_db():
    return sqlite3.connect("cricbuzz.db")

# ----------------------------
# 2. 25 SQL questions
# ----------------------------
QUESTIONS = [
    (
        "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        """
        SELECT full_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country = 'India'
        ORDER BY full_name;
        """,
    ),
    (
        "Show all cricket matches played in the last few days. Include match description, both team names, venue name with city, and match date. Sort by most recent first.",
        """
        SELECT match_description, team1_name, team2_name,
               CONCAT(venue_name, ', ', city) AS venue_with_city,
               match_date
        FROM matches
        WHERE match_date >= CURDATE() - INTERVAL 7 DAY
        ORDER BY match_date DESC;
        """,
    ),
    (
        "List the top 10 highest run scorers in ODI cricket. Show player name, total runs, batting average, and centuries. Highest first.",
        """
        SELECT player_name, runs AS total_runs, batting_average, centuries
        FROM player_format_stats
        WHERE format = 'ODI'
        ORDER BY runs DESC
        LIMIT 10;
        """,
    ),
    (
        "Display venues with seating capacity over 25,000. Show venue name, city, country, and capacity. Largest first (top 10).",
        """
        SELECT venue_name, city, country, capacity
        FROM venue_country_map
        WHERE capacity > 25000
        ORDER BY capacity DESC
        LIMIT 10;
        """,
    ),
    (
        "Calculate how many matches each team has won. Show team name and total wins. Most wins first.",
        """
        SELECT winner AS team_name, COUNT(*) AS total_wins
        FROM matches
        WHERE winner IS NOT NULL
        GROUP BY winner
        ORDER BY total_wins DESC;
        """,
    ),
    (
        "Count players by playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
        """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        GROUP BY playing_role
        ORDER BY player_count DESC;
        """,
    ),
    (
        "Find the highest individual batting score in each format (Test, ODI, T20I).",
        """
        SELECT format, MAX(runs) AS highest_score
        FROM batting_scorecard
        WHERE format IN ('Test', 'ODI', 'T20I')
        GROUP BY format
        ORDER BY FIELD(format, 'Test', 'ODI', 'T20I');
        """,
    ),
    (
        "Show all cricket series that started in 2024. Include series name, host country, match type, start date, and total matches planned.",
        """
        SELECT series_name, host_country, match_type, start_date, total_matches_planned
        FROM series
        WHERE YEAR(start_date) = 2024
        ORDER BY start_date;
        """,
    ),
    (
        "Find all-rounders with more than 1000 runs AND more than 50 wickets in a format.",
        """
        SELECT p.full_name AS player_name, pfs.runs AS total_runs, pfs.wickets AS total_wickets, pfs.format
        FROM player_format_stats pfs
        JOIN players p ON p.full_name = pfs.player_name
        WHERE p.playing_role = 'All-rounder'
          AND pfs.runs > 1000
          AND pfs.wickets > 50
        ORDER BY pfs.runs DESC;
        """,
    ),
    (
        "Get details of the last 20 completed matches. Show description, teams, winner, margin, victory type, and venue.",
        """
        SELECT match_description, team1_name, team2_name,
               winner AS winning_team, result_margin AS victory_margin,
               result_type AS victory_type, venue_name
        FROM matches
        WHERE winner IS NOT NULL
        ORDER BY match_date DESC
        LIMIT 20;
        """,
    ),
    (
        "Compare player performance across formats for players with at least 2 formats.",
        """
        SELECT player_name,
               SUM(CASE WHEN format = 'Test' THEN runs ELSE 0 END) AS test_runs,
               SUM(CASE WHEN format = 'ODI' THEN runs ELSE 0 END) AS odi_runs,
               SUM(CASE WHEN format = 'T20I' THEN runs ELSE 0 END) AS t20i_runs,
               ROUND(AVG(batting_average), 2) AS overall_batting_average
        FROM player_format_stats
        GROUP BY player_name
        HAVING COUNT(DISTINCT format) >= 2
        ORDER BY overall_batting_average DESC;
        """,
    ),
    (
        "Home vs away win counts per team (home = venue country matches team country).",
        """
        WITH team_matches AS (
            SELECT m.team1_name AS team_name, m.winner, v.country AS venue_country, t.country AS team_country
            FROM matches m
            JOIN team_country_map t ON m.team1_name = t.team_name
            JOIN venue_country_map v ON m.venue_id = v.venue_id
            UNION ALL
            SELECT m.team2_name, m.winner, v.country, t.country
            FROM matches m
            JOIN team_country_map t ON m.team2_name = t.team_name
            JOIN venue_country_map v ON m.venue_id = v.venue_id
        )
        SELECT team_name,
               SUM(CASE WHEN venue_country = team_country AND winner = team_name THEN 1 ELSE 0 END) AS home_wins,
               SUM(CASE WHEN venue_country <> team_country AND winner = team_name THEN 1 ELSE 0 END) AS away_wins
        FROM team_matches
        GROUP BY team_name
        ORDER BY home_wins + away_wins DESC;
        """,
    ),
    (
        "Batting partnerships of 100+ runs between consecutive batting positions.",
        """
        SELECT p.batter1_name, p.batter2_name, p.partnership_runs,
               CONCAT('Innings ', p.innings_id, ' (Match ', p.match_id, ')') AS innings_context
        FROM partnerships p
        WHERE ABS(p.batter2_position - p.batter1_position) = 1
          AND p.partnership_runs >= 100
        ORDER BY p.partnership_runs DESC;
        """,
    ),
    (
        "Bowling economy and wickets at venues (min 3 matches, 4+ overs per match).",
        """
        SELECT b.player_name, v.venue_name,
               ROUND(AVG(b.economy), 2) AS avg_economy,
               SUM(b.wickets) AS total_wickets,
               COUNT(DISTINCT b.match_id) AS matches_at_venue
        FROM bowling_scorecard b
        JOIN matches m ON b.match_id = m.match_id
        JOIN venue_country_map v ON m.venue_id = v.venue_id
        WHERE b.overs >= 4
        GROUP BY b.player_name, v.venue_name
        HAVING COUNT(DISTINCT b.match_id) >= 3
        ORDER BY avg_economy ASC;
        """,
    ),
    (
        "Player performance in close matches (<50 runs or <5 wickets margin).",
        """
        SELECT b.player_name,
               ROUND(AVG(b.runs), 2) AS avg_runs_in_close_matches,
               COUNT(DISTINCT b.match_id) AS close_matches_played
        FROM batting_scorecard b
        JOIN matches m ON b.match_id = m.match_id
        WHERE (m.result_type = 'runs' AND CAST(m.result_margin AS UNSIGNED) < 50)
           OR (m.result_type = 'wickets' AND CAST(m.result_margin AS UNSIGNED) < 5)
        GROUP BY b.player_name
        ORDER BY avg_runs_in_close_matches DESC;
        """,
    ),
    (
        "Yearly batting averages and strike rates since 2020 (min 5 matches per year).",
        """
        SELECT b.player_name,
               YEAR(m.match_date) AS year,
               ROUND(AVG(b.runs), 2) AS avg_runs_per_match,
               ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate
        FROM batting_scorecard b
        JOIN matches m ON b.match_id = m.match_id
        WHERE YEAR(m.match_date) >= 2020
        GROUP BY b.player_name, YEAR(m.match_date)
        HAVING COUNT(*) >= 5
        ORDER BY year DESC, avg_runs_per_match DESC;
        """,
    ),
    (
        "Toss win percentage by toss decision (bat vs field).",
        """
        SELECT toss_decision,
               COUNT(*) AS total_matches,
               SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won,
               ROUND(100.0 * SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(*), 2) AS toss_win_percentage
        FROM matches
        WHERE toss_decision IS NOT NULL AND winner IS NOT NULL
        GROUP BY toss_decision;
        """,
    ),
    (
        "Most economical bowlers in ODI/T20I (10+ matches, 2+ overs avg per match).",
        """
        SELECT b.player_name,
               ROUND(AVG(b.economy), 2) AS overall_economy,
               SUM(b.wickets) AS total_wickets,
               COUNT(DISTINCT b.match_id) AS matches_bowled
        FROM bowling_scorecard b
        JOIN matches m ON b.match_id = m.match_id
        WHERE m.format IN ('ODI', 'T20I')
        GROUP BY b.player_name
        HAVING COUNT(DISTINCT b.match_id) >= 10
           AND AVG(b.overs) >= 2
        ORDER BY overall_economy ASC;
        """,
    ),
    (
        "Most consistent batsmen since 2022 (min 10 balls/innings). Lower stddev = more consistent.",
        """
        SELECT b.player_name,
               ROUND(AVG(b.runs), 2) AS avg_runs,
               ROUND(STDDEV(b.runs), 2) AS run_stddev
        FROM batting_scorecard b
        JOIN matches m ON b.match_id = m.match_id
        WHERE YEAR(m.match_date) >= 2022
        GROUP BY b.player_name
        HAVING AVG(b.balls_faced) >= 10
        ORDER BY run_stddev ASC;
        """,
    ),
    (
        "Match counts and batting averages by format (20+ total matches).",
        """
        SELECT player_name,
               SUM(CASE WHEN format = 'Test' THEN matches_played ELSE 0 END) AS test_matches,
               SUM(CASE WHEN format = 'ODI' THEN matches_played ELSE 0 END) AS odi_matches,
               SUM(CASE WHEN format = 'T20I' THEN matches_played ELSE 0 END) AS t20_matches,
               ROUND(AVG(batting_average), 2) AS batting_average
        FROM player_format_stats
        GROUP BY player_name
        HAVING SUM(matches_played) >= 20
        ORDER BY batting_average DESC;
        """,
    ),
    (
        "Comprehensive performance ranking by format using weighted batting, bowling, and fielding scores.",
        """
        SELECT pf.format,
               pf.player_name,
               ROUND((pf.runs * 0.01) + (pf.batting_average * 0.5) + (pf.strike_rate * 0.3)
                   + (pf.wickets * 2) + ((50 - pf.bowling_average) * 0.5) + ((6 - pf.economy_rate) * 2)
                   + COALESCE(fs.catches, 0) + COALESCE(fs.stumpings, 0) + COALESCE(fs.run_outs, 0),
                   2
               ) AS total_score
        FROM player_format_stats pf
        LEFT JOIN fielding_stats fs ON pf.player_name = fs.player_name
        ORDER BY pf.format, total_score DESC;
        """,
    ),
    (
        "Head-to-head analysis for teams with 5+ meetings in the last 3 years.",
        """
        WITH h2h AS (
            SELECT LEAST(team1_name, team2_name) AS team_a,
                   GREATEST(team1_name, team2_name) AS team_b,
                   team1_name, team2_name, winner, result_margin, result_type,
                   toss_decision, venue_id, match_date
            FROM matches
            WHERE match_date >= CURDATE() - INTERVAL 3 YEAR
        ),
        pairs AS (
            SELECT team_a, team_b,
                   COUNT(*) AS total_matches,
                   SUM(CASE WHEN winner = team_a THEN 1 ELSE 0 END) AS team_a_wins,
                   SUM(CASE WHEN winner = team_b THEN 1 ELSE 0 END) AS team_b_wins,
                   ROUND(AVG(CASE WHEN winner = team_a THEN CAST(result_margin AS UNSIGNED) END), 2) AS team_a_avg_margin,
                   ROUND(AVG(CASE WHEN winner = team_b THEN CAST(result_margin AS UNSIGNED) END), 2) AS team_b_avg_margin
            FROM h2h
            GROUP BY team_a, team_b
            HAVING COUNT(*) >= 5
        )
        SELECT team_a, team_b, total_matches, team_a_wins, team_b_wins,
               ROUND(100.0 * team_a_wins / total_matches, 2) AS team_a_win_pct,
               ROUND(100.0 * team_b_wins / total_matches, 2) AS team_b_win_pct,
               team_a_avg_margin, team_b_avg_margin
        FROM pairs
        ORDER BY total_matches DESC;
        """,
    ),
    (
        "Recent player form: last 10 innings with form category.",
        """
        WITH ranked AS (
            SELECT b.player_name, b.runs, b.strike_rate, m.match_date,
                   ROW_NUMBER() OVER (PARTITION BY b.player_name ORDER BY m.match_date DESC) AS rn
            FROM batting_scorecard b
            JOIN matches m ON b.match_id = m.match_id
        ),
        last10 AS (
            SELECT player_name, runs, strike_rate, rn FROM ranked WHERE rn <= 10
        ),
        summary AS (
            SELECT player_name,
                   ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 2) AS avg_last_5,
                   ROUND(AVG(runs), 2) AS avg_last_10,
                   ROUND(AVG(CASE WHEN rn <= 5 THEN strike_rate END), 2) AS sr_last_5,
                   ROUND(AVG(strike_rate), 2) AS sr_last_10,
                   SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) AS fifties_in_last_10,
                   ROUND(STDDEV(runs), 2) AS consistency_stddev
            FROM last10
            GROUP BY player_name
            HAVING COUNT(*) >= 5
        )
        SELECT player_name, avg_last_5, avg_last_10, sr_last_5, sr_last_10,
               fifties_in_last_10, consistency_stddev,
               CASE
                   WHEN avg_last_5 >= 60 AND fifties_in_last_10 >= 4 THEN 'Excellent Form'
                   WHEN avg_last_5 >= 40 AND fifties_in_last_10 >= 2 THEN 'Good Form'
                   WHEN avg_last_5 >= 25 THEN 'Average Form'
                   ELSE 'Poor Form'
               END AS form_category
        FROM summary
        ORDER BY avg_last_5 DESC;
        """,
    ),
    (
        "Best batting partnerships (consecutive positions, 5+ partnerships).",
        """
        SELECT batter1_name, batter2_name,
               ROUND(AVG(partnership_runs), 2) AS avg_partnership_runs,
               SUM(CASE WHEN partnership_runs > 50 THEN 1 ELSE 0 END) AS partnerships_over_50,
               MAX(partnership_runs) AS highest_partnership,
               ROUND(100.0 * SUM(CASE WHEN partnership_runs > 50 THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate_pct
        FROM partnerships
        WHERE ABS(batter2_position - batter1_position) = 1
        GROUP BY batter1_name, batter2_name
        HAVING COUNT(*) >= 5
        ORDER BY avg_partnership_runs DESC;
        """,
    ),
    (
        "Quarterly performance evolution and career phase (6+ quarters, 3+ matches/quarter).",
        """
        WITH quarterly AS (
            SELECT b.player_name,
                   YEAR(m.match_date) AS yr,
                   QUARTER(m.match_date) AS qtr,
                   ROUND(AVG(b.runs), 2) AS avg_runs,
                   ROUND(AVG(b.strike_rate), 2) AS avg_strike_rate,
                   COUNT(*) AS matches_in_quarter
            FROM batting_scorecard b
            JOIN matches m ON b.match_id = m.match_id
            GROUP BY b.player_name, YEAR(m.match_date), QUARTER(m.match_date)
            HAVING COUNT(*) >= 3
        ),
        with_lag AS (
            SELECT *,
                   LAG(avg_runs) OVER (PARTITION BY player_name ORDER BY yr, qtr) AS prev_avg_runs
            FROM quarterly
        ),
        trajectory AS (
            SELECT player_name,
                   COUNT(*) AS quarters_analyzed,
                   ROUND(AVG(avg_runs - COALESCE(prev_avg_runs, avg_runs)), 2) AS avg_quarterly_change
            FROM with_lag
            GROUP BY player_name
            HAVING COUNT(*) >= 4
        )
        SELECT player_name, quarters_analyzed, avg_quarterly_change,
               CASE
                   WHEN avg_quarterly_change > 5 THEN 'Career Ascending'
                   WHEN avg_quarterly_change < -5 THEN 'Career Declining'
                   ELSE 'Career Stable'
               END AS career_phase
        FROM trajectory
        ORDER BY avg_quarterly_change DESC;
        """,
    ),
]

# ----------------------------
# 3. run_query function
# ----------------------------
def run_query(sql: str):
    conn = get_db()
    try:
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        raise e