import pandas as pd

categories = {
    "Food": ["restaurant", "cafe", "coffee", "dining", "mcdonalds", "burger", "pizza"],
    "Groceries": ["supermarket", "grocery", "walmart", "target"],
    "Transport": ["uber", "lyft", "metro", "bus", "taxi", "fuel", "gas"],
    "Entertainment": ["netflix", "spotify", "movie", "cinema", "amc"],
    "Shopping": ["amazon", "mall", "clothes", "nike", "adidas"],
    "Bills": ["electric", "water", "internet", "phone", "rent"]
}

def categorize(row):
    text = f"{row['Merchant']} {row.get('Description','')}".lower()
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in text:
                return cat
    return "Other"

