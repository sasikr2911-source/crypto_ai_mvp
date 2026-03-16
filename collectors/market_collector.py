from data_sources.dexscreener_api import get_trending_pairs
from data_sources.coingecko_api import get_major_coins


def collect_market_data():

    tokens = []
    seen = set()

    # 1️⃣ Major coins from CoinGecko
    major_coins = get_major_coins()

    for coin in major_coins:

        symbol = coin.get("symbol")

        if not symbol:
            continue

        seen.add(symbol)

        tokens.append({
            "symbol": symbol,
            "price": float(coin.get("price", 0)),
            "volume": float(coin.get("volume", 0)),
            "liquidity": float(coin.get("liquidity", 0)),
            "chain": coin.get("chain", "main_market")
        })

    # 2️⃣ DEX tokens from Dexscreener
    pairs = get_trending_pairs()

    for p in pairs:

        symbol = p.get("token")

        if not symbol or symbol in seen:
            continue

        volume = float(p.get("volume_24h", 0))

        if volume < 50000:
            continue

        seen.add(symbol)

        tokens.append({
            "symbol": symbol,
            "price": float(p.get("price", 0)),
            "volume": volume,
            "liquidity": float(p.get("liquidity", 0)),
            "chain": p.get("chain")
        })

    return tokens