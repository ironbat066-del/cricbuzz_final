import streamlit as st

from utils.helpers import execute_sql, read_sql

st.title("CRUD Operations")

st.write("Add update delete records in database")
st.write("(C=create R=read U=update D=delete)")

table = st.selectbox("select table", ["players", "matches", "venues"])

if table == "players":
    st.write("All players:")
    df = read_sql("SELECT * FROM players")
    st.dataframe(df)

    st.write("---")
    st.write("ADD new player")
    name = st.text_input("name")
    country = st.text_input("country")
    role = st.text_input("role (Batsman/Bowler/All-rounder/Wicket-keeper)")
    if st.button("add player"):
        execute_sql(
            "INSERT INTO players (full_name, country, playing_role) VALUES (%s,%s,%s)",
            (name, country, role),
        )
        st.write("done! refresh page to see")
        st.rerun()

    st.write("---")
    st.write("UPDATE player")
    pid = st.text_input("player id to update")
    new_name = st.text_input("new name")
    if st.button("update player"):
        execute_sql("UPDATE players SET full_name=%s WHERE player_id=%s", (new_name, pid))
        st.write("updated")
        st.rerun()

    st.write("---")
    st.write("DELETE player")
    del_id = st.text_input("player id to delete")
    if st.button("delete player"):
        execute_sql("DELETE FROM players WHERE player_id=%s", (del_id,))
        st.write("deleted")
        st.rerun()

elif table == "matches":
    st.write("All matches:")
    df = read_sql("SELECT match_id, match_description, team1_name, team2_name, winner FROM matches")
    st.dataframe(df)

    st.write("---")
    st.write("ADD new match")
    desc = st.text_input("match description")
    t1 = st.text_input("team 1")
    t2 = st.text_input("team 2")
    if st.button("add match"):
        execute_sql(
            "INSERT INTO matches (match_description, team1_name, team2_name, match_date, format) VALUES (%s,%s,%s,NOW(),'ODI')",
            (desc, t1, t2),
        )
        st.write("added")
        st.rerun()

    st.write("---")
    st.write("UPDATE match winner")
    mid = st.text_input("match id")
    winner = st.text_input("winner team name")
    if st.button("update match"):
        execute_sql("UPDATE matches SET winner=%s WHERE match_id=%s", (winner, mid))
        st.write("updated")
        st.rerun()

    st.write("---")
    st.write("DELETE match")
    del_mid = st.text_input("match id to delete")
    if st.button("delete match"):
        execute_sql("DELETE FROM matches WHERE match_id=%s", (del_mid,))
        st.write("deleted")
        st.rerun()

else:
    st.write("All venues:")
    df = read_sql("SELECT * FROM venue_country_map")
    st.dataframe(df)

    st.write("---")
    st.write("ADD venue")
    vid = st.text_input("venue id")
    vname = st.text_input("venue name")
    city = st.text_input("city")
    country = st.text_input("country")
    cap = st.text_input("capacity")
    if st.button("add venue"):
        execute_sql(
            "INSERT INTO venue_country_map (venue_id, venue_name, city, country, capacity) VALUES (%s,%s,%s,%s,%s)",
            (vid, vname, city, country, cap),
        )
        st.write("added")
        st.rerun()

    st.write("---")
    st.write("DELETE venue")
    del_vid = st.text_input("venue id to delete")
    if st.button("delete venue"):
        execute_sql("DELETE FROM venue_country_map WHERE venue_id=%s", (del_vid,))
        st.write("deleted")
        st.rerun()
