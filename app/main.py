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

