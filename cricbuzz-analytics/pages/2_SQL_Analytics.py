import streamlit as st

from questions.queries import QUESTIONS, run_query

st.title("SQL Analytics")

st.write("This page has 25 sql questions for the assignment.")
st.write("Select question and click run query button.")

question_list = [f"Question {i + 1}" for i in range(len(QUESTIONS))]
pick = st.selectbox("pick question number", range(len(QUESTIONS)), format_func=lambda i: question_list[i])

question_text, sql = QUESTIONS[pick]

st.write("Question:")
st.write(question_text)

st.write("SQL query used:")
st.code(sql.strip())

if st.button("run query"):
    try:
        result = run_query(sql)
        st.write("Result:")
        st.dataframe(result)
        st.write("Total rows:", len(result))
    except Exception as e:
        st.write("Query failed:", e)
