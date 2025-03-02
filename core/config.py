import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

# core
APP_PORT = int(os.getenv("APP_PORT", 8000))

# Database
DATABASE_URL = os.getenv("DATABASE_URL")