import sqlite3
from urllib import response
import requests
import io
import pandas as pd 
from extract import insert_transaction, read_user_params
from transform import compare_budgets_with_spending


def load_data(df, conn):
    for _, row in df.iterrows():
        recipient = row['Saajan nimi']
        amount = row['Summa']
        category = row['category']
        insert_transaction(conn, recipient, amount, category)
    conn.commit()
    print(f"Loaded {len(df)} transactions into database.")


def create_output_file(stats_per_category, total_stats):
    # Get budget data
    budget_df = read_user_params()
    budgets = dict(zip(budget_df['Category'], budget_df['Budget']))
    
    spending = {category: abs(amount) for category, amount in stats_per_category}
    comparison = compare_budgets_with_spending(budgets, spending)

    # Write to text file
    with open('output.txt', 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("BUDGET vs SPENDING COMPARISON\n")
        f.write("=" * 60 + "\n\n")
        
        if not comparison:
            f.write("No budget data available for comparison.\n")
            f.write("Please ensure user_params.yaml contains budget information.\n\n")
        
        for category, data in comparison.items():
            f.write(f"Category: {category}\n")
            f.write(f"  Budget:     ${data['budget']:.2f}\n")
            f.write(f"  Spent:      ${data['spent']:.2f}\n")
            f.write(f"  Difference: ${data['difference']:.2f}")
            if data['difference'] < 0:
                f.write(" (OVER BUDGET!)\n")
            else:
                f.write(" (Under budget)\n")
            f.write("-" * 60 + "\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("TOTAL STATISTICS\n")
        f.write("=" * 60 + "\n")
        total_expenses, total_income = total_stats[0]
        f.write(f"Total Expenses: ${abs(total_expenses):.2f}\n")
        f.write(f"Total Income:   ${total_income:.2f}\n")
        f.write(f"Net:            ${(total_income + total_expenses):.2f}\n")
    
    print("Output saved to output.txt")

