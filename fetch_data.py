import requests
from database_handler import create_tables, get_connection


API_KEY = "Cg5QnQ4hGxac0zOPBxyZkVzuVkoEHSuAmoQ0dLiU"   # <-- put your real API key here
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"

def fetch_and_store():
    # REMOVE create_database() ❌
    create_tables()   # ✅ only create tables
    conn = get_connection()
    cur = conn.cursor()

    # 1. Competitions
    url = f"{BASE_URL}/competitions.json?api_key={API_KEY}"
    data = requests.get(url).json()
    for comp in data.get("competitions", []):
        cat = comp.get("category", {})
        cur.execute("INSERT IGNORE INTO Categories VALUES (%s,%s)",
                    (cat["id"], cat["name"]))
        cur.execute("""
            INSERT IGNORE INTO Competitions
            (competition_id, competition_name, parent_id, type, gender, category_id)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            comp["id"], comp["name"], comp.get("parent_id"),
            comp.get("type", ""), comp.get("gender", ""), cat["id"]
        ))

    # 2. Complexes
    url = f"{BASE_URL}/complexes.json?api_key={API_KEY}"
    data = requests.get(url).json()
    for complex_data in data.get("complexes", []):
        cur.execute("INSERT IGNORE INTO Complexes VALUES (%s,%s)",
                    (complex_data["id"], complex_data["name"]))
        for v in complex_data.get("venues", []):
            cur.execute("""
            INSERT IGNORE INTO Venues
            (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                v["id"], v["name"], v["city_name"], v["country_name"],
                v["country_code"], v["timezone"], complex_data["id"]
            ))

    # 3. Doubles Competitor Rankings (FIXED)
    url = f"{BASE_URL}/rankings/doubles.json?api_key={API_KEY}"
    data = requests.get(url).json()
    for ranking_group in data.get("rankings", []):
        for player in ranking_group.get("competitor_rankings", []):
            competitor = player["competitor"]

            # Insert competitor
            cur.execute("""
            INSERT IGNORE INTO Competitors VALUES (%s,%s,%s,%s,%s)
            """, (
                competitor["id"], competitor["name"], competitor["country"],
                competitor["country_code"], competitor["abbreviation"]
            ))

            # Insert ranking
            cur.execute("""
            INSERT INTO Competitor_Rankings
            (`rank`, movement, points, competitions_played, competitor_id)
            VALUES (%s,%s,%s,%s,%s)
            """, (
                player["rank"], player["movement"], player["points"],
                player["competitions_played"], competitor["id"]
            ))

    conn.commit()
    conn.close()
    print("Data fetched & stored in MySQL.")

if __name__ == "__main__":
    fetch_and_store()