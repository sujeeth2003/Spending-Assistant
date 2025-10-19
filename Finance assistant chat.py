# ===== Step 1: Install required packages =====
#!pip install pandas matplotlib groq

# ===== Step 2: Set your Groq API Key =====
import os
from dotenv import load_dotenv
#from google.colab import userdata
#os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
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
    "Cofe": []
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

# ===== Step 7: Use Groq LLM for insights =====
client = Groq()

# Prepare a summary text for the LLM
summary_text = df.groupby("Category")['Amount'].sum().to_dict()
summary_text_str = "\n".join([f"{cat}: ${amt:.2f}" for cat, amt in summary_text.items()])

# Example query
query = "Which category did I spend the most on and how can I reduce it and compare the price of a specific item and recommend cheaper place to buy make it short like within 4 lines and if its necessary suggest which else can be reduced?"

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
      {
        "role": "user",
        "content": f"My spending summary:\n{summary_text_str}\n\nQuestion: {query}"
      }
    ],
    temperature=0.7,
    max_completion_tokens=512,
    top_p=1,
    stream=True,
    stop=None
)

# Stream the AI's response
print("AI Insight:")
for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
