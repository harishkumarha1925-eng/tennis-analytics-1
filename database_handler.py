import mysql.connector

# MySQL connection settings (XAMPP default)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         # change if you set another user
    "password": "",         # enter password if set in XAMPP
    "database": "tennis_db" # we’ll create this
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS tennis_db")
    conn.commit()
    conn.close()

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Categories
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    )
    """)

    # Competitions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(100) NOT NULL,
        parent_id VARCHAR(50),
        type VARCHAR(20) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        category_id VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )
    """)

    # Complexes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(100) NOT NULL
    )
    """)

    # Venues
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        city_name VARCHAR(100) NOT NULL,
        country_name VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        timezone VARCHAR(100) NOT NULL,
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
    )
    """)

    # Competitors
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(10) NOT NULL
    )
    """)

    # Competitor Rankings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Competitor_Rankings (
        rank_id INT AUTO_INCREMENT PRIMARY KEY,
        rank INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
    )
    """)

    conn.commit()
    conn.close()