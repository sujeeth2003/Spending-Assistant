from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
from io import StringIO
import os

from utils import preprocess_csv

load_dotenv()
client = Groq()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/finance/insights")
async def finance_insights(
    file: UploadFile,
    question: str = Form(...)
):
    content = await file.read()
    _, summary = preprocess_csv(StringIO(content.decode()))

    summary_text = "\n".join([f"{k}: ${v:.2f}" for k, v in summary.items()])

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
My spending summary:
{summary_text}

Question:
{question}

Answer in max 4 short lines. Give actionable advice.
"""
            }
        ],
        temperature=0.7,
        max_completion_tokens=300,
    )

    answer = completion.choices[0].message.content

    return {
        "summary": summary,
        "answer": answer
    }
