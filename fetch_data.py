import requests
from database_handler import create_tables, get_connection

# ---------------------------
# API ENDPOINTS (replace YOUR_API_KEY)
# ---------------------------
COMPETITIONS_URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key=Cg5QnQ4hGxac0zOPBxyZkVzuVkoEHSuAmoQ0dLiU"
COMPLEXES_URL = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key=Cg5QnQ4hGxac0zOPBxyZkVzuVkoEHSuAmoQ0dLiU"
RANKINGS_URL = "https://api.sportradar.com/tennis/trial/v3/en/rankings/doubles.json?api_key=Cg5QnQ4hGxac0zOPBxyZkVzuVkoEHSuAmoQ0dLiU"


# ---------------------------
# FETCH COMPETITIONS + CATEGORIES
# ---------------------------
def fetch_competitions():
    conn = get_connection()
    cur = conn.cursor()

    data = requests.get(COMPETITIONS_URL).json()

    for item in data.get("competitions", []):
        comp_id = item.get("id")
        comp_name = item.get("name")
        parent_id = item.get("parent_id")
        comp_type = item.get("type")
        gender = item.get("gender")

        category = item.get("category", {})
        category_id = category.get("id")
        category_name = category.get("name")

        # Insert category
        cur.execute("""
            INSERT IGNORE INTO Categories (category_id, category_name)
            VALUES (%s, %s)
        """, (category_id, category_name))

        # Insert competition
        cur.execute("""
            INSERT IGNORE INTO Competitions (competition_id, competition_name, parent_id, type, gender, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (comp_id, comp_name, parent_id, comp_type, gender, category_id))

    conn.commit()
    conn.close()
    print("Competitions & Categories inserted.")


# ---------------------------
# FETCH COMPLEXES + VENUES
# ---------------------------
def fetch_complexes():
    conn = get_connection()
    cur = conn.cursor()

    data = requests.get(COMPLEXES_URL).json()

    for complex_item in data.get("complexes", []):
        complex_id = complex_item.get("id")
        complex_name = complex_item.get("name")

        # Insert complex
        cur.execute("""
            INSERT IGNORE INTO Complexes (complex_id, complex_name)
            VALUES (%s, %s)
        """, (complex_id, complex_name))

        # Insert venues
        for venue in complex_item.get("venues", []):
            cur.execute("""
                INSERT IGNORE INTO Venues (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                venue.get("id"),
                venue.get("name"),
                venue.get("city_name"),
                venue.get("country_name"),
                venue.get("country_code"),
                venue.get("timezone"),
                complex_id
            ))

    conn.commit()
    conn.close()
    print("Complexes & Venues inserted.")


# ---------------------------
# FETCH COMPETITORS + RANKINGS
# ---------------------------
def fetch_competitor_rankings():
    conn = get_connection()
    cur = conn.cursor()

    data = requests.get(RANKINGS_URL).json()

    for ranking in data.get("rankings", []):
        competitor = ranking.get("competitor", {})
        competitor_id = competitor.get("id")

        # Insert competitor
        cur.execute("""
            INSERT IGNORE INTO Competitors (competitor_id, name, country, country_code, abbreviation)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            competitor_id,
            competitor.get("name"),
            competitor.get("country"),
            competitor.get("country_code"),
            competitor.get("abbreviation"),
        ))

        # Insert ranking
        cur.execute("""
            INSERT INTO Competitor_Rankings (rank, movement, points, competitions_played, competitor_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            ranking.get("rank"),
            ranking.get("movement"),
            ranking.get("points"),
            ranking.get("competitions_played"),
            competitor_id
        ))

    conn.commit()
    conn.close()
    print("Competitors & Rankings inserted.")


# ---------------------------
# MASTER FUNCTION
# ---------------------------
def fetch_and_store():
    create_tables()
    fetch_competitions()
    fetch_complexes()
    fetch_competitor_rankings()
    print("All data fetched & stored successfully!")


if __name__ == "__main__":
    fetch_and_store()
