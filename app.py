# pylint: disable=missing-module-docstring

import os
import logging
from datetime import timedelta

import duckdb
import streamlit as st
from pathlib import Path

# Configurer les logs
logging.basicConfig(level=logging.INFO)


# Définir les chemins
data_folder = Path("data")
db_file = data_folder / "exercises_sql_tables.duckdb"

# 1. Créer le dossier s'il n'existe pas
if not data_folder.exists():
    logging.info("Dossier 'data' non trouvé, création...")
    data_folder.mkdir(parents=True, exist_ok=True)

# 2. Créer le fichier s'il n'existe pas
if not db_file.exists():
    logging.info("Fichier DB non trouvé, exécution de init_db.py...")
    try:
        exec(open("init_db.py").read())
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution de init_db.py : {e}")
        raise

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

def check_users_solution(user_query:str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checkig the volutmes 
    :param user_query: a string containing the SQL query inserted by the user
    """
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solutions_df.columns]
        compare_df = result.compare(solutions_df)
        if compare_df.shape == (0,0):
            st.write ("Correct !")
            st.balloons()
    except KeyError as e:
        st.dataframe(compare_df)
        st.write("Some columns are missing")

    n_lines_differences = result.shape[0] - solutions_df.shape[0]
    if n_lines_differences != 0:
        st.write(
            f"result has a {n_lines_differences} lines difference with the solution"
        )

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write(f"You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    exercise_selected = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise_selected)

    try:
        exercise_name = exercise_selected.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql") as f:
            answer = f.read()
        solutions_df = con.execute(answer).df()
    except KeyError as e:
        st.write("no data for this exercise")


st.header("enter your code :")
query = st.text_area("votre Code SQL ici", key="user_input")

if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'")
        st.rerun()

if st.button('Reset'):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01' WHERE exercise_name = '{exercise_name}'")
    st.rerun()

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
        st.write(solutions_df)
    except NameError as e:
        st.write("no data for this exercise")
