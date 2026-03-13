import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# Primary Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Load fallback keys if provided (e.g., GROQ_FALLBACK_KEYS='["key1", "key2"]')
try:
    fallback_keys_raw = os.getenv("GROQ_FALLBACK_KEYS", "[]")
    GROQ_FALLBACK_KEYS = json.loads(fallback_keys_raw)
except json.JSONDecodeError:
    GROQ_FALLBACK_KEYS = []

MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_TEMPERATURE = 0.3

DB_PATH = BASE_DIR / "candidates_data.json"
