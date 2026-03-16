MAJOR_COINS = {"BTC", "ETH", "BNB", "SOL", "XRP", "ADA"}


def detect_market_sentiment(tokens, previous_state):

    # protect against None
    if previous_state is None:
        previous_state = {}

    if not tokens:
        return None, previous_state

    major_tokens = [t for t in tokens if t.get("symbol") in MAJOR_COINS]

    if not major_tokens:
        return None, previous_state

    sentiment = None
    up_count = 0
    down_count = 0

    new_state = {}

    for token in major_tokens:

        symbol = token.get("symbol")
        price = token.get("price", 0)

        # ignore invalid prices
        if not price:
            continue

        if symbol in previous_state:

            old_price = previous_state.get(symbol, 0)

            if old_price > 0:

                change = ((price - old_price) / old_price) * 100

                if change > 0.5:
                    up_count += 1

                elif change < -0.5:
                    down_count += 1

        new_state[symbol] = price

    # market sentiment logic
    if up_count >= 4:
        sentiment = "PUMP"

    elif down_count >= 4:
        sentiment = "CRASH"

    return sentiment, new_state