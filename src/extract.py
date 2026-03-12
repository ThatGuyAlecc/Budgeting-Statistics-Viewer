import csv
import sqlite3
import pandas as pd
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

def read_data():
    with open(DATA_DIR / "export.csv", "r", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
    return data

def read_user_params():
    try:
        with open(DATA_DIR / "user_params.yaml", "r") as file:
            data = yaml.safe_load(file)
        
        if data is None:
            print("Warning: user_params.yaml is empty")
            return pd.DataFrame(columns=['Category', 'Budget'])
        
        # Get budgets from the YAML file
        if isinstance(data, dict) and "budgets" in data:
            budget_dict = data["budgets"]
        elif isinstance(data, dict):
            # If the YAML file is just a flat dictionary of budgets
            budget_dict = data
        else:
            print("Warning: Invalid YAML structure")
            return pd.DataFrame(columns=['Category', 'Budget'])
        
        if budget_dict:
            budget_df = pd.DataFrame(list(budget_dict.items()), columns=['Category', 'Budget'])
            return budget_df
        else:
            return pd.DataFrame(columns=['Category', 'Budget'])
            
    except FileNotFoundError:
        print(f"Warning: {DATA_DIR / 'user_params.yaml'} not found")
        return pd.DataFrame(columns=['Category', 'Budget'])
    except Exception as e:
        print(f"Error reading budgets: {e}")
        return pd.DataFrame(columns=['Category', 'Budget'])

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
    stats = cursor.fetchone()
    return [stats]