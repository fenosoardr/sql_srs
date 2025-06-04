import pip
import streamlit as st
import pandas as pd
import duckdb
import io


csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages CROSS JOIN food_items
"""
solution = duckdb.sql(answer).df()

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

st.header("enter your code :")
query = st.text_area("votre Code SQL ici",  key = 'user_input')
if query :
    result = duckdb.sql(query).df()
    st.dataframe(result)

with st.sidebar :
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Window Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write('You selected:', option)

tab2, tab3 = st.tabs([ "Tables", "Solutions"])



with tab2:
    st.write("table : bereages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("expected :")
    st.dataframe(solution)

with tab3:
    st.write(answer)
