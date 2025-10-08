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

