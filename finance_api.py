from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from groq import Groq
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- Models ----------
class Expense(BaseModel):
    category: str
    amount: float

class InsightRequest(BaseModel):
    expenses: List[Expense]
    question: str


# ---------- Health Check ----------
@app.get("/")
def root():
    return {"status": "Finance Assistant API running"}


# ---------- Manual Insights ----------
@app.post("/finance/manual-insights")
async def manual_insights(req: InsightRequest):
    # Aggregate spending by category
    summary = {}

    for e in data.expenses:
        merchant = e["merchant"].lower()
        amount = e["amount"]

        category = "Other"
        for k, v in categories.items():
            if any(word in merchant for word in v):
                category = k

        summary[category] = summary.get(category, 0) + amount

    summary_text = "\n".join(
        f"{k}: ${v:.2f}" for k, v in summary.items()
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"My spending:\n{summary_text}\n\n{data.question}"
        }],
        max_completion_tokens=150
    )

    return {
        "summary": summary,
        "answer": response.choices[0].message.content
    }
