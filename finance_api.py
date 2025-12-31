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
    for e in req.expenses:
        summary[e.category] = summary.get(e.category, 0) + e.amount

    summary_text = "\n".join(
        f"{cat}: ${amt:.2f}" for cat, amt in summary.items()
    )

    prompt = f"""
You are a financial assistant.
Here is the user's spending breakdown:

{summary_text}

Question:
{req.question}

Give practical, concise advice.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=200,
    )

    return {
        "summary": summary,
        "answer": response.choices[0].message.content.strip()
    }
