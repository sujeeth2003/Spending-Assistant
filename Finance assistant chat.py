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

