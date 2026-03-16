def detect_hundred_x(tokens):

    hundred_x_tokens = []

    for token in tokens:

        price = token.get("price", 0)
        volume = token.get("volume", 0)
        liquidity = token.get("liquidity", 0)
        alpha_score = token.get("alpha_score", 0)

        score = 0

        # Ignore large tokens (price too high)
        if price > 5:
            continue

        # Low price (early stage)
        if price < 0.01:
            score += 30

        # Strong volume
        if volume > 500000:
            score += 30

        # Healthy liquidity
        if liquidity > 100000:
            score += 20

        # Strong AI alpha score
        if alpha_score > 60:
            score += 40

        # Additional safety filter
        if liquidity > volume * 5:
            continue

        if score >= 70:

            new_token = token.copy()
            new_token["hundred_x_score"] = score

            hundred_x_tokens.append(new_token)

    return hundred_x_tokens