import sqlite3
from contextlib import closing

DB_NAME = "crawler_results.db"

def initialize_database():
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    type TEXT,
                    content TEXT,
                    url TEXT,
                    root_url TEXT
                )
            """)

def save_results(emails, phone_numbers, root_url):
    initialize_database()
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            for email, url in emails.items():
                conn.execute("INSERT INTO results (type, content, url, root_url) VALUES (?, ?, ?, ?)", ("EMAIL", email, url, root_url))
            for phone, url in phone_numbers.items():
                conn.execute("INSERT INTO results (type, content, url, root_url) VALUES (?, ?, ?, ?)", ("PHONE NUMBER", phone, url, root_url))

def search_results_db(keyword):
    initialize_database()
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with conn:
            cursor = conn.execute("""
                SELECT type, content, url, root_url
                FROM results
                WHERE type LIKE ? OR content LIKE ? OR url LIKE ? OR root_url LIKE ?
                ORDER BY id DESC
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
