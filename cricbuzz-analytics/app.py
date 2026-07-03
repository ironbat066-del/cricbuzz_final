import streamlit as st

from utils.helpers import db_counts

st.set_page_config(page_title="CricPulse")

st.title("CricPulse 🏏")
st.write("This is my cricket project for college.")
st.write("Data comes from cricbuzz api and mysql database.")

st.write("---")

try:
    counts = db_counts()
    st.write("Total matches in db:", counts.get("matches", 0))
    st.write("Total players:", counts.get("players", 0))
    st.write("Total venues:", counts.get("venue_country_map", 0))
except Exception as e:
    st.write("Error connecting to database:", e)
    st.write("Run this first: python -m database.init_db")

st.write("---")

st.write("How to use this app:")
st.write("1. Click Live Matches in sidebar for match data")
st.write("2. Click SQL Analytics for 25 questions")
st.write("3. Click Top Player Stats for player rankings")
st.write("4. Click CRUD Operations to add delete update records")

st.write("---")
st.write("Made by me using python streamlit and mysql")
