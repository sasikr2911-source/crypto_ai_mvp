import os
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

# API Sources
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Scanner interval (seconds)
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", 300))

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
