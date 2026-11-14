"""Loads settings from a .env file so keys never sit in your code."""
import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_ID = os.getenv("EXCHANGE_ID", "kraken")
API_KEY = os.getenv("API_KEY", "")
API_SECRET = os.getenv("API_SECRET", "")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", 0.01))
MAX_POSITION_PCT = float(os.getenv("MAX_POSITION_PCT", 0.25))
