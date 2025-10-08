from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from groq import Groq
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/finance/insights")
async def finance_insights(
    file: UploadFile,
    question: str = Form(...)
):
    df = pd.read_csv(file.file)

    categories = {
        "Food": ["restaurant", "cafe", "coffee", "pizza"],
        "Groceries": ["walmart", "grocery"],
        "Transport": ["uber", "fuel"],
        "Entertainment": ["netflix", "spotify"],
        "Bills": ["rent", "electric"],
    }

    def categorize(row):
        text = str(row.get("Merchant", "")).lower()
        for cat, keys in categories.items():
            if any(k in text for k in keys):
                return cat
        return "Other"

    df["Category"] = df.apply(categorize, axis=1)
    summary = df.groupby("Category")["Amount"].sum().to_dict()

    summary_text = "\n".join(
        f"{k}: ${v:.2f}" for k, v in summary.items()
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"My spending:\n{summary_text}\n\n{question}"
            }
        ],
        max_completion_tokens=150,
    )

    return {
        "summary": summary,
        "answer": response.choices[0].message.content
    }
