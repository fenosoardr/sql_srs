# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise_selected = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise_selected)

    try:
        exercise_name = exercise_selected.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql") as f:
            answer = f.read()
        exercise_answer = con.execute(answer).df()
    except KeyError as e:
        st.write("no data for this exercise")


st.header("enter your code :")
query = st.text_area("votre Code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solutions"])

with tab2:
    try:
        exercise_tables = exercise_selected.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)
    except KeyError as e:
        st.write("no data for this exercise")

with tab3:
    try:
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()
        st.write(answer)
        st.write(exercise_answer)
    except NameError as e:
        st.write("no data for this exercise")
