# src/config.py
"""Configuration file for the booking agent."""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta, datetime

# Load Environment Variables

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / '.env', override=True)

# App
PROJECT_NAME = os.environ.get("PROJECT_NAME", "MeetingRoomBookingAgent")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

# LLM Configuration
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.0"))
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "llama3-70b-8192")

OLLAMA_MODEL_NAME = os.environ.get("OLLAMA_MODEL_NAME", "")
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "")

GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# LangSmith Configuration
LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY", "")

# File Paths
ROOMS_FILE = PROJECT_DIR / "data/rooms.json"
BOOKINGS_FILE = PROJECT_DIR / "data/bookings.json"
MSG_JSON_FILE = PROJECT_DIR / "data/clarification_messages.json"
LOGS_DIR = PROJECT_DIR / "logs"


# Logging Configuration
recursion_limit = 50
DELAY = timedelta(hours=0.5)

# Ensure logs directory exists (skip silently on read-only filesystems like Vercel)
try:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    current_time = datetime.now().strftime('%Y-%m-%d_%H')
    log_file_path = LOGS_DIR / f"{current_time}.log"
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )
except OSError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

logger = logging.getLogger(__name__)


class FlaskConfig:
    """Flask application configuration."""
    FLASK_APP = os.getenv('FLASK_APP', 'src.app')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    PORT = os.getenv('PORT', '5000')
    HOST = os.getenv('HOST', '127.0.0.1')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)