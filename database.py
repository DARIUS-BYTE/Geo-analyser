import sqlite3
from datetime import datetime

DB_NAME = "seo_analytics.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            brand TEXT,
            rank INTEGER,
            ai_present BOOLEAN,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_ranking(keyword, brand, rank, ai_present):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO rankings (keyword, brand, rank, ai_present, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (keyword, brand, rank, ai_present, timestamp))
    conn.commit()
    conn.close()

def get_all_rankings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT keyword, brand, rank, ai_present, timestamp FROM rankings')
    data = cursor.fetchall()
    conn.close()
    return data