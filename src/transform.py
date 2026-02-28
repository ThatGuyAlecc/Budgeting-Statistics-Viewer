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
    'Entertainment': ['spotify', 'netflix', 'hulu', 'disney+', 'amazon prime', 'apple music', 'youtube', 'twitch', 'steam', 'google', 'play', 'nintendo', 'xbox', 'playstation', 'finnkino', 'theater', 'concert', 'event', 'crunchroll'],
    'Transportation': ['vr', 'hsl', 'taxi', 'uber', 'bolt', 'lyft', 'bus', 'train', 'metro', 'tram', 'nysse'],
}
    for category, keywords in categories.items():
        if any(keyword in row["Saajan nimi"].lower() for keyword in keywords):
            return category
    return 'Other'