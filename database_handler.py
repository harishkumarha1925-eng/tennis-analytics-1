from sqlalchemy import create_engine
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    """Return an SQLAlchemy engine for Pandas queries"""
    if os.getenv("DB_HOST"):  # Local dev
        return create_engine(
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
    else:  # Streamlit Cloud
        return create_engine(
            f"mysql+pymysql://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"
        )

    if os.getenv("DB_HOST"):  # Local dev via .env
        return {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "database": os.getenv("DB_NAME"),
            "port": int(os.getenv("DB_PORT", 3306)),
        }
    else:  # Streamlit Cloud (uses st.secrets)
        return {
            "host": st.secrets["DB_HOST"],
            "user": st.secrets["DB_USER"],
            "password": st.secrets["DB_PASS"],
            "database": st.secrets["DB_NAME"],
            "port": int(st.secrets["DB_PORT"]),
        }

def get_connection():
    """Return a live MySQL connection"""
    return mysql.connector.connect(**get_config())

def create_tables():
    """Create all required tables if they don't exist"""
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
        `rank` INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully")

