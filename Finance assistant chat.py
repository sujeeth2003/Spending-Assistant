# ===== Step 1: Install required packages =====
#!pip install pandas matplotlib groq

# ===== Step 2: Set your Groq API Key =====
import os
from dotenv import load_dotenv
#from google.colab import userdata
load_dotenv()
Key = os.getenv("GROQ_API_KEY")

# ===== Step 3: Import libraries =====
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# ===== Step 4: Load your CSV file =====
# Make sure your CSV has columns: Date, Merchant, Amount, Description (optional)
df = pd.read_csv("transactions.csv")
df['Date'] = pd.to_datetime(df['Date'])

# ===== Step 5: Categorize spending =====
# Simple rule-based categorization first
categories = {
    "Food": ["restaurant", "cafe", "coffee", "dining", "mcdonalds", "burger", "pizza"],
    "Groceries": ["supermarket", "grocery", "walmart", "target"],
    "Transport": ["uber", "lyft", "metro", "bus", "taxi", "fuel", "gas"],
    "Entertainment": ["netflix", "spotify", "movie", "cinema", "amc"],
    "Shopping": ["amazon", "mall", "clothes", "nike", "adidas"],
    "Bills": ["electric", "water", "internet", "phone", "rent"],
    "Coffee": []
}

def categorize(row):
    text = f"{row['Merchant']} {row.get('Description','')}".lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in text:
                return cat
    return "Other"

df['Category'] = df.apply(categorize, axis=1)

# ===== Step 6: Plot monthly spending chart =====
monthly = df.groupby([df['Date'].dt.to_period('M'), 'Category'])['Amount'].sum().unstack(fill_value=0)
monthly.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title("Monthly Spending by Category")
plt.ylabel("Amount ($)")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.show()

