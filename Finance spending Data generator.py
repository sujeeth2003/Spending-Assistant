import pandas as pd

# Sample transaction CSV
data = {
    "Date": ["2025-10-01", "2025-10-02", "2025-10-05", "2025-10-07", "2025-10-09"],
    "Merchant": ["Walmart", "Starbucks", "Amazon", "Uber", "Whole Foods"],
    "Description": ["Groceries", "Coffee", "", "Ride", ""],
    "Amount": [120.5, 5.75, 45.0, 18.0, 80.0]
}

df = pd.DataFrame(data)
df.to_csv("transactions.csv", index=False)
df
