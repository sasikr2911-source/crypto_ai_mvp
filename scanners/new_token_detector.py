MAJOR_COINS = {"BTC", "ETH", "BNB", "SOL"}


def detect_new_tokens(tokens):

    new_tokens = []
    seen = set()

    for token in tokens:

        symbol = token.get("symbol")
        price = token.get("price", 0)
        volume = token.get("volume", 0)
        liquidity = token.get("liquidity", 0)

        # basic validation
        if not symbol or price <= 0:
            continue

        # skip major market coins
        if symbol in MAJOR_COINS:
            continue

        # avoid duplicates
        if symbol in seen:
            continue

        seen.add(symbol)

        # early-stage opportunity filter
        if volume > 50000 and liquidity > 20000:

            new_token = token.copy()
            new_token["new_token"] = True

            new_tokens.append(new_token)

    return new_tokens