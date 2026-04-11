import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

model_name = os.getenv("model_name", "gpt-4o-mini")  # default model gpt 4o mini
key = os.getenv("OPENAI_API_KEY")
