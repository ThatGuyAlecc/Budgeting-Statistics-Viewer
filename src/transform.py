import pandas as pd
import numpy as np
from extract import read_data


def transform_data():
    data = read_data()
    df = pd.DataFrame(data[1:], columns=data[0])
    df['Summa'] = df['Summa'].str.replace(',', '.').astype(float)
    df['category'] = df.apply(categorize_transaction, axis=1)
    return df

def categorize_transaction(row):
    categories = {
    'Food & Necessities': ['juvenes', 'sale', 'lidl', 'k-supermarket', 'k-market', 's-market', 'prisma', 'citymarket', 'kauppa', 'k-citymarket', 'campusravita', 'sokos', 'stockmann', 'alko', 'r-kioski', 'apteekki', 'pharmacy'],
    'Clothing': ['h&m', 'zara', 'gina tricot', 'lindex', 'cubus', 'dressmann', 'veromoda', 'only', 'jack & jones'],
    'Entertainment': ['spotify', 'netflix', 'hulu', 'disney+', 'amazon prime', 'apple music', 'youtube', 'twitch', 'steam', 'google', 'play', 'nintendo', 'xbox', 'playstation', 'finnkino', 'theater', 'concert', 'event', 'crunchroll', 'hoyoverse'],
    'Transportation': ['vr', 'hsl', 'taxi', 'uber', 'bolt', 'lyft', 'bus', 'train', 'metro', 'tram', 'nysse'],
    'Sports & Fitness': ['gym', 'kuntosali', 'kiipeily', 'uima', 'uimahalli', 'deltarec'],
}
    for category, keywords in categories.items():
        if any(keyword in row["Saajan nimi"].lower() for keyword in keywords):
            return category
    return 'Other'

def calculate_budget(df, budgets):
    category_sums = df.groupby('category')['Summa'].sum()
    budget_comparison = {category: {'total': category_sums.get(category, 0), 'budget': budgets.get(category, 0)} for category in budgets}
    return budget_comparison

def compare_budgets_with_spending(budgets, spending):
    comparison = {}
    for category in budgets:
        budget = float(budgets[category])
        spent = spending.get(category, 0)
        comparison[category] = {
            'budget': budget,
            'spent': spent,
            'difference': budget - spent
        }
    return comparison