"""
SkillRadar Backend Configuration
Loads environment variables and provides centralized config.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    PORT = int(os.getenv("FLASK_PORT", 5000))

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///skillradar.db")

    # API Keys
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
    JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY", "")

    # Cache
    CACHE_DIR = os.getenv("CACHE_DIR", "./cache")
    CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", 6))

    # API endpoints
    ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"
    REMOTIVE_BASE_URL = "https://remotive.com/api/remote-jobs"
    JSEARCH_BASE_URL = "https://jsearch.p.rapidapi.com/search"

    # Sensible defaults
    DEFAULT_RESULTS_PER_PAGE = 20
    MAX_RESULTS_PER_QUERY = 100


config = Config()
