# Step 1: Create database and all MySQL tables
# Run this file first:  python create_database_and_tables.py

import mysql.connector

# -------- CHANGE THESE IF NEEDED --------
HOST = "localhost"
USER = "root"
PASSWORD = "Ironbat2529"   # your mysql password
DATABASE = "cricbuzz"
# ----------------------------------------

print("Connecting to MySQL...")
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)
cursor = conn.cursor()

# Create database
print("Creating database...")
cursor.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE)
cursor.execute("USE " + DATABASE)

# Drop old tables if they exist (so we can run file again)
print("Dropping old tables if any...")
tables_to_drop = [
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
]
for table in tables_to_drop:
    cursor.execute("DROP TABLE IF EXISTS " + table)

# Table 1: players
print("Creating players table...")
cursor.execute("""
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    country VARCHAR(128) NOT NULL,
    playing_role VARCHAR(64) NOT NULL,
    batting_style VARCHAR(64),
    bowling_style VARCHAR(64)
)
""")

# Table 2: venues
print("Creating venue_country_map table...")
cursor.execute("""
CREATE TABLE venue_country_map (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city VARCHAR(128),
    country VARCHAR(128) NOT NULL,
    capacity INT
)
""")

# Table 3: teams
print("Creating team_country_map table...")
cursor.execute("""
CREATE TABLE team_country_map (
    team_name VARCHAR(128) PRIMARY KEY,
    country VARCHAR(128) NOT NULL
)
""")

# Table 4: series
print("Creating series table...")
cursor.execute("""
CREATE TABLE series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(255) NOT NULL,
    host_country VARCHAR(128),
    match_type VARCHAR(32),
    start_date DATE,
    total_matches_planned INT
)
""")

# Table 5: matches
print("Creating matches table...")
cursor.execute("""
CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_description VARCHAR(512) NOT NULL,
    team1_name VARCHAR(128) NOT NULL,
    team2_name VARCHAR(128) NOT NULL,
    venue_id INT,
    venue_name VARCHAR(255),
    city VARCHAR(128),
    match_date DATETIME NOT NULL,
    format VARCHAR(16) NOT NULL,
    winner VARCHAR(128),
    result_margin VARCHAR(32),
    result_type VARCHAR(32),
    toss_winner VARCHAR(128),
    toss_decision VARCHAR(32),
    series_id INT
)
""")

# Table 6: player stats by format
print("Creating player_format_stats table...")
cursor.execute("""
CREATE TABLE player_format_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    format VARCHAR(16) NOT NULL,
    runs INT DEFAULT 0,
    wickets INT DEFAULT 0,
    centuries INT DEFAULT 0,
    matches_played INT DEFAULT 0,
    batting_average DECIMAL(6, 2),
    strike_rate DECIMAL(6, 2),
    bowling_average DECIMAL(6, 2),
    economy_rate DECIMAL(5, 2)
)
""")

# Table 7: batting scorecard
print("Creating batting_scorecard table...")
cursor.execute("""
CREATE TABLE batting_scorecard (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    format VARCHAR(16) NOT NULL,
    batting_position TINYINT,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    strike_rate DECIMAL(6, 2)
)
""")

# Table 8: bowling scorecard
print("Creating bowling_scorecard table...")
cursor.execute("""
CREATE TABLE bowling_scorecard (
    bowl_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    overs DECIMAL(5, 1) DEFAULT 0,
    economy DECIMAL(5, 2),
    wickets INT DEFAULT 0
)
""")

# Table 9: partnerships
print("Creating partnerships table...")
cursor.execute("""
CREATE TABLE partnerships (
    partnership_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    batter1_name VARCHAR(255) NOT NULL,
    batter2_name VARCHAR(255) NOT NULL,
    batter1_position TINYINT,
    batter2_position TINYINT,
    partnership_runs INT NOT NULL
)
""")

# Table 10: fielding stats
print("Creating fielding_stats table...")
cursor.execute("""
CREATE TABLE fielding_stats (
    player_name VARCHAR(255) PRIMARY KEY,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    run_outs INT DEFAULT 0
)
""")

conn.commit()
cursor.close()
conn.close()

print("Done! Database and all tables created successfully.")
