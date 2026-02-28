import sqlite3
from extract import insert_transaction

def load_data(df, conn):
    for _, row in df.iterrows():
        recipient = row['Saajan nimi']
        amount = row['Summa']
        category = row['category']
        insert_transaction(conn, recipient, amount, category)
    conn.commit()
    print(f"Loaded {len(df)} transactions into database.")

