def analyze_liquidity(tokens):

    safe_tokens = []

    for token in tokens:

        liquidity = token.get("liquidity", 0)
        volume = token.get("volume", 0)

        liquidity_score = 0

        # Liquidity strength
        if liquidity > 500000:
            liquidity_score += 40

        elif liquidity > 200000:
            liquidity_score += 25

        elif liquidity > 100000:
            liquidity_score += 15

        # Liquidity vs volume health
        if volume > 0 and liquidity > volume * 0.3:
            liquidity_score += 30

        if liquidity_score >= 30:

            new_token = token.copy()
            new_token["liquidity_score"] = liquidity_score

            safe_tokens.append(new_token)

    return safe_tokens