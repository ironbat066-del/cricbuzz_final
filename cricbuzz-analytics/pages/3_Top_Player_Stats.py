import streamlit as st

from utils.helpers import read_sql

st.title("Top Player Stats")

st.write("Some player stats from the database")

stat_type = st.selectbox(
    "choose stats type",
    [
        "top odi run scorers",
        "top wicket takers",
        "best batting average",
        "all rounders",
        "fielding stats",
        "player ranking",
    ],
)

if stat_type == "top odi run scorers":
    st.write("Top ODI run scorers")
    df = read_sql(
        """
        SELECT player_name, runs, centuries, batting_average
        FROM player_format_stats
        WHERE format = 'ODI'
        ORDER BY runs DESC
        LIMIT 10
        """
    )
    st.dataframe(df)

elif stat_type == "top wicket takers":
    st.write("Top wicket takers")
    df = read_sql(
        """
        SELECT player_name, format, wickets, economy_rate
        FROM player_format_stats
        WHERE wickets > 0
        ORDER BY wickets DESC
        LIMIT 10
        """
    )
    st.dataframe(df)

elif stat_type == "best batting average":
    fmt = st.selectbox("format", ["Test", "ODI", "T20I"])
    st.write("Best batting average in", fmt)
    df = read_sql(
        """
        SELECT player_name, batting_average, runs, matches_played
        FROM player_format_stats
        WHERE format = %s
        ORDER BY batting_average DESC
        LIMIT 10
        """,
        (fmt,),
    )
    st.dataframe(df)

elif stat_type == "all rounders":
    st.write("All rounder players")
    df = read_sql(
        """
        SELECT p.full_name, pfs.format, pfs.runs, pfs.wickets
        FROM player_format_stats pfs
        JOIN players p ON p.full_name = pfs.player_name
        WHERE p.playing_role = 'All-rounder'
        """
    )
    st.dataframe(df)

elif stat_type == "fielding stats":
    st.write("Fielding stats")
    df = read_sql("SELECT * FROM fielding_stats ORDER BY catches DESC")
    st.dataframe(df)

else:
    st.write("Player ranking score")
    df = read_sql(
        """
        SELECT pf.player_name, pf.format,
               (pf.runs * 0.01 + pf.batting_average * 0.5 + pf.wickets * 2) AS score
        FROM player_format_stats pf
        ORDER BY score DESC
        LIMIT 15
        """
    )
    st.dataframe(df)
