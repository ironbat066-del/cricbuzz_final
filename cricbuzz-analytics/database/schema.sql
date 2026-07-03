CREATE DATABASE IF NOT EXISTS cricbuzz;
USE cricbuzz;

DROP TABLE IF EXISTS partnerships;
DROP TABLE IF EXISTS fielding_stats;
DROP TABLE IF EXISTS bowling_scorecard;
DROP TABLE IF EXISTS batting_scorecard;
DROP TABLE IF EXISTS player_format_stats;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS venue_country_map;
DROP TABLE IF EXISTS team_country_map;

CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(128) NOT NULL,
    playing_role VARCHAR(64) NOT NULL,
    batting_style VARCHAR(64),
    bowling_style VARCHAR(64)
);

CREATE TABLE venue_country_map (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city VARCHAR(128),
    country VARCHAR(128) NOT NULL,
    capacity INT
);

CREATE TABLE team_country_map (
    team_name VARCHAR(128) PRIMARY KEY,
    country VARCHAR(128) NOT NULL
);

CREATE TABLE series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(255) NOT NULL,
    host_country VARCHAR(128),
    match_type VARCHAR(32),
    start_date DATE,
    total_matches_planned INT
);

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
    series_id INT,
    FOREIGN KEY (venue_id) REFERENCES venue_country_map(venue_id),
    FOREIGN KEY (series_id) REFERENCES series(series_id)
);

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
    economy_rate DECIMAL(5, 2),
    UNIQUE KEY uq_player_format (player_name, format)
);

CREATE TABLE batting_scorecard (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    format VARCHAR(16) NOT NULL,
    batting_position TINYINT,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    strike_rate DECIMAL(6, 2),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE bowling_scorecard (
    bowl_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    overs DECIMAL(5, 1) DEFAULT 0,
    economy DECIMAL(5, 2),
    wickets INT DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE partnerships (
    partnership_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_id INT NOT NULL,
    batter1_name VARCHAR(255) NOT NULL,
    batter2_name VARCHAR(255) NOT NULL,
    batter1_position TINYINT,
    batter2_position TINYINT,
    partnership_runs INT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE fielding_stats (
    player_name VARCHAR(255) PRIMARY KEY,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    run_outs INT DEFAULT 0
);

CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_format ON matches(format);
CREATE INDEX idx_batting_player ON batting_scorecard(player_name);
CREATE INDEX idx_batting_match ON batting_scorecard(match_id);
CREATE INDEX idx_bowling_player ON bowling_scorecard(player_name);
