import pandas as pd
from database_handler import get_connection

# Connect to Railway DB
conn = get_connection()

# Show all tables
tables = pd.read_sql("SHOW TABLES;", conn)
print("Tables in DB:\n", tables)

# Show row counts for key tables
for table in ["Categories", "Competitions", "Venues", "Competitors", "Competitor_Rankings"]:
    try:
        df = pd.read_sql(f"SELECT COUNT(*) AS cnt FROM {table};", conn)
        print(f"{table}: {df['cnt'][0]} rows")
    except Exception as e:
        print(f"{table}: not found ({e})")

conn.close()
