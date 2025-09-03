from database_handler import get_engine
import pandas as pd

def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)

def list_competitions_with_category():
    return run_query("""
        SELECT c.competition_name,
               IFNULL(cat.category_name, 'Unknown') AS category_name
        FROM Competitions c
        LEFT JOIN Categories cat ON c.category_id = cat.category_id
    """)




def top_ranked_competitors(limit=5):
    return run_query(f"""
        SELECT comp.name, r.rank, r.points
        FROM Competitors comp
        JOIN Competitor_Rankings r ON comp.competitor_id = r.competitor_id
        ORDER BY r.rank ASC LIMIT {limit}
    """)
