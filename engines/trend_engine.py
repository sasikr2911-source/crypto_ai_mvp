def detect_trend(tokens):

    trending_tokens = []

    for token in tokens:

        volume = token.get("volume", 0)
        liquidity = token.get("liquidity", 0)

        trend_score = 0

        # Volume strength
        if volume > 500000:
            trend_score += 40

        elif volume > 100000:
            trend_score += 20

        # Liquidity strength
        if liquidity > 300000:
            trend_score += 40

        elif liquidity > 100000:
            trend_score += 20

        if trend_score >= 40:

            new_token = token.copy()
            new_token["trend_score"] = trend_score

            trending_tokens.append(new_token)

    return trending_tokens