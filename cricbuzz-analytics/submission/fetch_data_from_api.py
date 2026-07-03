# fetch data from cricbuzz api and save to mysql
# run: python fetch_data_from_api.py
# if api limit is over, run: python insert_sample_data.py

import requests
import mysql.connector as mysql
from datetime import datetime

DB_CON = {
    "host": "localhost",
    "database": "cricbuzz",
    "user": "root",
    "password": "Ironbat2529"
}

try:
    con = mysql.connect(**DB_CON)
    cursor = con.cursor()
    print("connected to mysql")
except Exception as e:
    print("database connection error:", e)
    exit()

# put your NEW key here (from RapidAPI account: drunkenlee066@gmail.com)
RAPIDAPI_KEY = "14f29ea30cmsh7bad2b98aedf2b7p104bdcjsn33eef1e8405b"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "Content-Type": "application/json"
}

if RAPIDAPI_KEY == "PASTE_NEW_KEY_HERE":
    print("ERROR: Paste your new RapidAPI key in RAPIDAPI_KEY at top of this file")
    exit()

match_count = 0
recent_count = 0
stats_count = 0

# -------- part 1: live matches --------
print("getting live matches from api...")
live_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
response = requests.get(live_url, headers=headers)
print("status code:", response.status_code)

live_data = response.json()

if response.status_code == 429:
    print("API limit is over!")
    print(live_data.get("message", ""))
elif "typeMatches" in live_data:
    for type_match in live_data["typeMatches"]:
        if "seriesMatches" not in type_match:
            continue
        for series_match in type_match["seriesMatches"]:
            if "seriesAdWrapper" not in series_match:
                continue
            matches_list = series_match["seriesAdWrapper"].get("matches", [])
            for match in matches_list:
                if "matchInfo" not in match:
                    continue
                info = match["matchInfo"]

                match_id = info.get("matchId")
                team1 = info.get("team1", {}).get("teamName", "Team 1")
                team2 = info.get("team2", {}).get("teamName", "Team 2")
                match_desc = info.get("matchDesc", team1 + " vs " + team2)
                match_format = info.get("matchFormat", "ODI")
                venue = info.get("venueInfo", {})
                venue_id = venue.get("id")
                venue_name = venue.get("ground", "Unknown")
                city = venue.get("city", "")
                status = info.get("status", "")
                match_date = datetime.now()

                try:
                    cursor.execute("""
                        INSERT INTO matches
                        (match_id, match_description, team1_name, team2_name,
                         venue_id, venue_name, city, match_date, format, winner)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE match_description = VALUES(match_description)
                    """, (match_id, match_desc, team1, team2, venue_id, venue_name, city, match_date, match_format, status))
                    match_count = match_count + 1
                except Exception as e:
                    print("error saving match:", e)
else:
    print("no match data found in live api response")

con.commit()
print("live matches saved:", match_count)

# -------- part 2: recent matches --------
print("getting recent matches from api...")
recent_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
response = requests.get(recent_url, headers=headers)
print("status code:", response.status_code)

recent_data = response.json()

if response.status_code == 429:
    print("API limit is over!")
    print(recent_data.get("message", ""))
elif "typeMatches" in recent_data:
    for type_match in recent_data["typeMatches"]:
        if "seriesMatches" not in type_match:
            continue
        for series_match in type_match["seriesMatches"]:
            if "seriesAdWrapper" not in series_match:
                continue
            matches_list = series_match["seriesAdWrapper"].get("matches", [])
            for match in matches_list:
                if "matchInfo" not in match:
                    continue
                info = match["matchInfo"]

                match_id = info.get("matchId")
                team1 = info.get("team1", {}).get("teamName", "Team 1")
                team2 = info.get("team2", {}).get("teamName", "Team 2")
                match_desc = info.get("matchDesc", team1 + " vs " + team2)
                match_format = info.get("matchFormat", "ODI")
                venue = info.get("venueInfo", {})
                venue_id = venue.get("id")
                venue_name = venue.get("ground", "Unknown")
                city = venue.get("city", "")
                status = info.get("status", "")
                match_date = datetime.now()

                try:
                    cursor.execute("""
                        INSERT INTO matches
                        (match_id, match_description, team1_name, team2_name,
                         venue_id, venue_name, city, match_date, format, winner)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE match_description = VALUES(match_description)
                    """, (match_id, match_desc, team1, team2, venue_id, venue_name, city, match_date, match_format, status))
                    recent_count = recent_count + 1
                except Exception as e:
                    print("error saving match:", e)
else:
    print("no match data found in recent api response")

con.commit()
print("recent matches saved:", recent_count)

# -------- part 3: top stats --------
print("getting top stats from api...")
stats_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats"
response = requests.get(stats_url, headers=headers)
print("status code:", response.status_code)

data = response.json()
players_stats = []

if response.status_code == 429:
    print("API limit is over!")
    print(data.get("message", ""))
elif "statsTypesList" in data:
    stats = data["statsTypesList"][0]
    players_stats = stats["types"]
else:
    print("no statsTypesList in api response")

for player in players_stats:
    try:
        category = player.get("valueType", "Unknown")
        header = player.get("header", "Unknown")
        value = player.get("value", 0)
        if value is None:
            value = 0
        value = int(value)

        cursor.execute("""
            INSERT INTO player_format_stats (player_name, format, runs, matches_played)
            VALUES (%s, %s, %s, %s)
        """, (header, category, value, 1))
        stats_count = stats_count + 1
    except Exception as e:
        print("error saving stat:", e)

con.commit()
print("stats saved:", stats_count)

con.close()
print("done! total live + recent matches:", match_count + recent_count)

if match_count + recent_count + stats_count == 0:
    print("")
    print("NOTE: 0 rows saved because API did not return data.")
    print("Most common reason: RapidAPI monthly limit is finished (status 429).")
    print("For submission/demo, run this instead:")
    print("   python insert_sample_data.py")
