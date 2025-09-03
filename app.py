import streamlit as st
import pandas as pd
from queries import (
    list_competitions_with_category,
    top_ranked_competitors,
    run_query
)

st.set_page_config(page_title="🎾 Tennis Data Explorer", layout="wide")

st.title("🎾 Tennis Data Explorer (MySQL + Streamlit)")

page = st.sidebar.selectbox(
    "Choose a page",
    [
        "Competitions",
        "Top Competitors",
        "Venues & Complexes",
        "Country Analysis",
        "Leaderboards"
    ]
)

# Page 1 - Competitions
if page == "Competitions":
    st.subheader("📊 Competitions & Categories")
    df = list_competitions_with_category()
    st.dataframe(df)

# Page 2 - Top Competitors
elif page == "Top Competitors":
    st.subheader("🏆 Top Ranked Competitors")
    df = top_ranked_competitors(limit=10)
    st.dataframe(df)

# Page 3 - Venues & Complexes
elif page == "Venues & Complexes":
    st.subheader("🏟️ Venues with Complexes")
    df = run_query("""
        SELECT v.venue_name, v.city_name, v.country_name, v.timezone, c.complex_name
        FROM Venues v
        JOIN Complexes c ON v.complex_id = c.complex_id
    """)
    st.dataframe(df)

    st.subheader("📌 Venues per Country")
    df2 = run_query("""
        SELECT country_name, COUNT(*) as venue_count
        FROM Venues
        GROUP BY country_name
        ORDER BY venue_count DESC
    """)
    st.bar_chart(df2.set_index("country_name"))

# Page 4 - Country Analysis
elif page == "Country Analysis":
    st.subheader("🌍 Competitors by Country")
    df = run_query("""
        SELECT country, COUNT(*) as competitors, AVG(r.points) as avg_points
        FROM Competitors comp
        JOIN Competitor_Rankings r ON comp.competitor_id = r.competitor_id
        GROUP BY country
        ORDER BY competitors DESC
    """)
    st.dataframe(df)
    st.bar_chart(df.set_index("country")["competitors"])

# Page 5 - Leaderboards
elif page == "Leaderboards":
    st.subheader("🥇 Top Competitors by Points")
    df = run_query("""
        SELECT comp.name, comp.country, r.points
        FROM Competitors comp
        JOIN Competitor_Rankings r ON comp.competitor_id = r.competitor_id
        ORDER BY r.points DESC LIMIT 10
    """)
    st.table(df)