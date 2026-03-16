import requests
import time
from core.config import DEXSCREENER_API


COINS = ["BTC", "ETH", "BNB", "SOL"]


def get_trending_pairs():

    pairs = []
    seen = set()

    for coin in COINS:

        url = f"{DEXSCREENER_API}/search?q={coin}"

        try:

            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                continue

            data = response.json()

            for pair in data.get("pairs", [])[:25]:

                symbol = pair.get("baseToken", {}).get("symbol")

                if not symbol or symbol in seen:
                    continue

                seen.add(symbol)

                pairs.append({
                    "token": symbol,
                    "price": float(pair.get("priceUsd", 0)),
                    "volume_24h": float(pair.get("volume", {}).get("h24", 0)),
                    "liquidity": float(pair.get("liquidity", {}).get("usd", 0)),
                    "pair_address": pair.get("pairAddress"),
                    "chain": pair.get("chainId")
                })

            time.sleep(0.2)

        except Exception:
            continue

    return pairs