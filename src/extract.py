import csv
import sqlite3
import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

def read_data():
    with open(DATA_DIR / "export.csv", "r", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    return data

def init_db():
    print("Initializing database...")
    try:
        conn = sqlite3.connect(str(DATA_DIR / "database.db"))
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS transactions;')
        cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("Database initialized successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def insert_transaction(conn, recipient, amount, category):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (recipient, amount, category)
            VALUES (?, ?, ?)
        ''', (recipient, amount, category))
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_stats_per_category(conn):
    cursor = conn.cursor()
    cursor.execute('''
            SELECT category, SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS total_amount FROM transactions GROUP BY category
            ''')
    stats = cursor.fetchall()
    return stats

def get_total_stats(conn):
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT sum(CASE WHEN amount <= 0 THEN amount ELSE 0 END) AS total_expenses,
                   sum(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS total_income
                   FROM transactions
                   ''')
    stats = cursor.fetchall()
    return stats