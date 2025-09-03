from database_handler import get_engine
import pandas as pd
import streamlit as st

def run_query(query):
    engine = get_engine()
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"❌ SQL error (pandas): {repr(e)}")
        return pd.DataFrame()

def list_competitions_with_category():
    return run_query("""
        SELECT c.competition_name,
               IFNULL(cat.category_name, 'Unknown') AS category_name,
               c.`type`,
               c.gender
        FROM Competitions c
        LEFT JOIN Categories cat ON c.category_id = cat.category_id
    """)

def debug_query():
    """Run same query with raw cursor to expose MySQL error."""
    engine = get_engine()
    conn = engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.competition_name,
                   IFNULL(cat.category_name, 'Unknown') AS category_name,
                   c.`type`,
                   c.gender
            FROM Competitions c
            LEFT JOIN Categories cat ON c.category_id = cat.category_id
            LIMIT 5
        """)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        st.error(f"❌ RAW SQL error: {repr(e)}")
        return []
    finally:
        cur.close()
        conn.close()



