def detect_momentum(tokens):

    momentum_tokens = []

    for token in tokens:

        price = token.get("price", 0)
        volume = token.get("volume", 0)

        momentum_score = 0

        # Volume spike
        if volume > 1000000:
            momentum_score += 40

        elif volume > 300000:
            momentum_score += 20

        # Price strength
        if price > 1:
            momentum_score += 20

        elif price > 0.01:
            momentum_score += 10

        if momentum_score >= 30:

            new_token = token.copy()
            new_token["momentum_score"] = momentum_score

            momentum_tokens.append(new_token)

    return momentum_tokens