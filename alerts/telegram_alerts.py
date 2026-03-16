import requests

# Paste your real values here
TELEGRAM_BOT_TOKEN = "8618043465:AAEZ4-ryXQJMHly1esOZQJfFVKVNdJnfZn8"
TELEGRAM_CHAT_ID = "1091600611"


def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram alert error:", e)