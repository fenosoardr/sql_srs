import pip
import streamlit as st
import pandas as pd
#!pip install duckdb
import duckdb

st.write("hello world")
data = {'a':[1, 2, 3], "b":[4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label = "entrez votre input")
    result =  duckdb.query(sql_query).df()
    st.write(f"Vous avez rentré la query : {sql_query}")
    st.dataframe(result)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/images/dog.jpg", width=300)

with tab3:
    st.header("A owl")
    st.image("https://static.streamlit.io/images/owl.jpg", width=300)
