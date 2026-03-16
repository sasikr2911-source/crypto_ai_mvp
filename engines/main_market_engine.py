MAIN_COINS = {"BTC", "ETH", "BNB", "SOL"}


def detect_market_leaders(tokens):

    leaders = {}

    for token in tokens:

        symbol = token.get("symbol")
        liquidity = token.get("liquidity", 0)

        if symbol not in MAIN_COINS:
            continue

        # keep the pair with the highest liquidity
        if symbol not in leaders or liquidity > leaders[symbol]["liquidity"]:

            leaders[symbol] = {
                "symbol": symbol,
                "price": token.get("price"),
                "volume": token.get("volume"),
                "liquidity": liquidity
            }

    return list(leaders.values())