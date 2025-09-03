from database_handler import get_engine
import pandas as pd

def run_query(query):
    """Run a SQL query safely with Pandas + SQLAlchemy engine"""
    engine = get_engine()
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        import streamlit as st
        st.error(f"SQL error: {str(e)}")
        return pd.DataFrame()

# ---------------------------
# Competitions + Categories
# ---------------------------
def list_competitions_with_category():
    return run_query("""
        SELECT c.competition_name,
               IFNULL(cat.category_name, 'Unknown') AS category_name,
               c.`type`,
               c.gender
        FROM Competitions c
        LEFT JOIN Categories cat ON c.category_id = cat.category_id
    """)

def count_competitions_per_category():
    return run_query("""
        SELECT cat.category_name,
               COUNT(c.competition_id) AS total_competitions
        FROM Competitions c
        LEFT JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name
    """)

def list_doubles_competitions():
    return run_query("""
        SELECT competition_id, competition_name
        FROM Competitions
        WHERE `type` = 'doubles'
    """)

def competitions_by_category(category_name):
    return run_query(f"""
        SELECT competition_id, competition_name, `type`, gender
        FROM Competitions
        LEFT JOIN Categories cat ON Competitions.category_id = cat.category_id
        WHERE cat.category_name = '{category_name}'
    """)

def parent_and_sub_competitions():
    return run_query("""
        SELECT parent.competition_name AS parent_name,
               child.competition_name AS sub_name
        FROM Competitions child
        JOIN Competitions parent ON child.parent_id = parent.competition_id
    """)

def distribution_of_competition_types():
    return run_query("""
        SELECT cat.category_name, c.`type`, COUNT(*) AS total
        FROM Competitions c
        LEFT JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name, c.`type`
    """)

def list_top_level_competitions():
    return run_query("""
        SELECT competition_id, competition_name
        FROM Competitions
        WHERE parent_id IS NULL
    """)

# ---------------------------
# Complexes + Venues
# ---------------------------
def venues_with_complex_name():
    return run_query("""
        SELECT v.venue_name, v.city_name, v.country_name, v.timezone,
               c.complex_name
        FROM Venues v
        LEFT JOIN Complexes c ON v.complex_id = c.complex_id
    """)

def count_venues_per_complex():
    return run_query("""
        SELECT c.complex_name, COUNT(v.venue_id) AS total_venues
        FROM Complexes c
        LEFT JOIN Venues v ON c.complex_id = v.complex_id
        GROUP BY c.complex_name
    """)

def venues_in_country(country):
    return run_query(f"""
        SELECT venue_name, city_name, country_name, timezone
        FROM Venues
        WHERE country_name = '{country}'
    """)

def venues_with_timezones():
    return run_query("""
        SELECT venue_name, timezone
        FROM Venues
    """)

def complexes_with_multiple_venues():
    return run_query("""
        SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
        FROM Complexes c
        LEFT JOIN Venues v ON c.complex_id = v.complex_id
        GROUP BY c.complex_name
        HAVING COUNT(v.venue_id) > 1
    """)

def venues_grouped_by_country():
    return run_query("""
        SELECT country_name, COUNT(*) AS total_venues
        FROM Venues
        GROUP BY country_name
    """)

def venues_for_complex(complex_name):
    return run_query(f"""
        SELECT v.venue_name, v.city_name, v.country_name
        FROM Venues v
        LEFT JOIN Complexes c ON v.complex_id = c.complex_id
        WHERE c.complex_name = '{complex_name}'
    """)

# ---------------------------
# Competitors + Rankings
# ---------------------------
def all_competitors_with_rank_points():
    return run_query("""
        SELECT comp.name, cr.`rank`, cr.points
        FROM Competitors comp
        LEFT JOIN Competitor_Rankings cr ON comp.competitor_id = cr.competitor_id
    """)

def top_5_competitors():
    return run_query("""
        SELECT comp.name, cr.`rank`, cr.points
        FROM Competitors comp
        LEFT JOIN Competitor_Rankings cr ON comp.competitor_id = cr.competitor_id
        WHERE cr.`rank` <= 5
        ORDER BY cr.`rank`
    """)

def stable_rank_competitors():
    return run_query("""
        SELECT comp.name, cr.`rank`
        FROM Competitors comp
        LEFT JOIN Competitor_Rankings cr ON comp.competitor_id = cr.competitor_id
        WHERE cr.movement = 0
    """)

def total_points_by_country(country):
    return run_query(f"""
        SELECT comp.country, SUM(cr.points) AS total_points
        FROM Competitors comp
        LEFT JOIN Competitor_Rankings cr ON comp.competitor_id = cr.competitor_id
        WHERE comp.country = '{country}'
        GROUP BY comp.country
    """)

def competitors_per_country():
    return run_query("""
        SELECT country, COUNT(*) AS total_competitors
        FROM Competitors
        GROUP BY country
    """)

def highest_points_competitors():
    return run_query("""
        SELECT comp.name, cr.points
        FROM Competitors comp
        LEFT JOIN Competitor_Rankings cr ON comp.competitor_id = cr.competitor_id
        ORDER BY cr.points DESC
        LIMIT 1
    """)

