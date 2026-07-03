# Step 4 (optional): Check database using pandas
# Command: python check_database_with_pandas.py

import mysql.connector
import pandas as pd

HOST = "localhost"
USER = "root"
PASSWORD = "Ironbat2529"
DATABASE = "cricbuzz"

conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

print("---- PLAYERS ----")
df1 = pd.read_sql("SELECT * FROM players LIMIT 5", conn)
print(df1)

print("\n---- MATCHES ----")
df2 = pd.read_sql("SELECT match_id, match_description, team1_name, team2_name, winner FROM matches LIMIT 5", conn)
print(df2)

print("\n---- VENUES ----")
df3 = pd.read_sql("SELECT * FROM venue_country_map LIMIT 5", conn)
print(df3)

conn.close()
print("\nDatabase check done.")
