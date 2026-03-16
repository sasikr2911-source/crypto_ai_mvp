import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def get_major_coins():

    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,binancecoin,solana",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    try:

        response = requests.get(COINGECKO_URL, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        tokens = []

        for coin in data:

            tokens.append({
                "symbol": coin.get("symbol", "").upper(),
                "price": coin.get("current_price", 0),
                "volume": coin.get("total_volume", 0),
                "liquidity": coin.get("market_cap", 0),
                "chain": "main_market"
            })

        return tokens

    except Exception as e:

        print("CoinGecko error:", e)
        return []