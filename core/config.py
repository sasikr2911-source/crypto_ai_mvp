import os
from dotenv import load_dotenv

# Load environment variables from .env (optional)
load_dotenv()

# API Sources
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Scanner interval (seconds)
SCAN_INTERVAL = 300

# Telegram Bot Configuration
# Replace with your real bot token and chat ID

TELEGRAM_BOT_TOKEN = "8618043465:AAEZ4-ryXQJMHly1esOZQJfFVKVNdJnfZn8"
TELEGRAM_CHAT_ID = "1091600611"
