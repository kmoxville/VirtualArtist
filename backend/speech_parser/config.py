import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

# core
MAIN_LANG=os.getenv("MAIN_LANG")