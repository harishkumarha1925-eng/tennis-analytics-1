import streamlit as st
from queries import debug_query, list_competitions_with_category

st.title("🎾 Tennis DB Debug")

st.subheader("Raw debug query (direct cursor):")
rows = debug_query()
st.write(rows)

st.subheader("Normal query (pandas.read_sql):")
df = list_competitions_with_category()
st.write(df.head())
