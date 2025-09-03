import streamlit as st
from queries import debug_query

st.title("🎾 Tennis DB Raw Debug")

st.subheader("Raw debug query (direct cursor):")
rows = debug_query()
st.write(rows)

