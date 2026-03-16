from engines.trend_engine import detect_trend
from engines.momentum_engine import detect_momentum
from engines.liquidity_engine import analyze_liquidity


def calculate_alpha(tokens):

    tokens = detect_trend(tokens)
    tokens = detect_momentum(tokens)
    tokens = analyze_liquidity(tokens)

    alpha_tokens = []

    for token in tokens:

        trend = token.get("trend_score", 0)
        momentum = token.get("momentum_score", 0)
        liquidity = token.get("liquidity_score", 0)

        alpha_score = trend + momentum + liquidity

        if alpha_score >= 70:

            new_token = token.copy()
            new_token["alpha_score"] = alpha_score

            alpha_tokens.append(new_token)

    return alpha_tokens