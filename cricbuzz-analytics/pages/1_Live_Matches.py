import streamlit as st
import pandas as pd

from utils.helpers import read_sql
from utils.live_data import (
    fetch_live_from_api,
    live_matches_from_db,
    scorecard_for_match,
    team_details_for_match,
)

st.title("Live Matches")

st.write("Here you can see live and recent cricket matches.")

show = st.radio("what do you want to see?", ["from api", "from database"])

if show == "from api":
    st.write("Click button to get data from cricbuzz api")
    if st.button("get live matches"):
        rows, err = fetch_live_from_api()
        if err:
            st.write("Error:", err)
            st.write("maybe api limit is over try database option")
        else:
            st.write("got these matches:")
            st.dataframe(pd.DataFrame(rows))

else:
    st.write("Matches stored in mysql:")
    try:
        live_df = live_matches_from_db()
        st.dataframe(live_df)

        if len(live_df) > 0:
            st.write("Pick a match id to see scorecard:")
            match_id = st.selectbox("match id", live_df["match_id"].tolist())

            st.write("Batting scorecard")
            batting, bowling = scorecard_for_match(match_id)
            st.dataframe(batting)

            st.write("Bowling scorecard")
            st.dataframe(bowling)

            st.write("Team details")
            teams = team_details_for_match(match_id)
            st.dataframe(teams)
    except Exception as e:
        st.write("Something went wrong:", e)
