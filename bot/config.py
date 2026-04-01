# bot/config.py
# One single place that reads environment variables and every other module can import from here.

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def _require(key:str) -> str:
    """"Read an environment variable and raise error if it is missing."""
    value = os.getenv(key)
    if not value: 
        raise RuntimeError(
            f"Required environment variable '{key}' is not set. "
            f"Check your .env file against .env.example"
        )
    return value

class Config:
    """"Central configuration class that reads environment variables once and provides them as attributes (instead of os.getenv)
    )."""""
    TELEGRAM_BOT_TOKEN = _require("TELEGRAM_BOT_TOKEN")
    OPENROUTE_API_KEY = _require("OPENROUTE_API_KEY")
    HF_ACCESS_TOKEN = _require("HF_ACCESS_TOKEN")
    OPEN_METEO_URL = _require("OPEN_METEO_URL")