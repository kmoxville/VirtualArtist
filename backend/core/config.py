import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

APP_PORT = int(os.getenv("APP_PORT", 8000))
DATABASE_URL = os.getenv("DATABASE_URL")