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

