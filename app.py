# pylint: disable=missing-module-docstring

import os
import logging
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


with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme :
        st.write(f"You selected:", theme)
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else :
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
