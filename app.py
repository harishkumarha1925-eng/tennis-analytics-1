import streamlit as st
from queries import debug_query

st.title("🎾 Tennis DB Raw Debug")

rows = debug_query()
st.write("Raw output from DB (no pandas):")
st.write(rows)


