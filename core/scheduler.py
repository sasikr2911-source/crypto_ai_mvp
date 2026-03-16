import time

from collectors.market_collector import collect_market_data
from scanners.new_token_detector import detect_new_tokens

from engines.main_market_engine import detect_market_leaders
from engines.market_sentiment_engine import detect_market_sentiment
from engines.alpha_score_engine import calculate_alpha
from engines.hundred_x_detector import detect_hundred_x

from alerts.telegram_alerts import send_telegram_alert
from database.db_manager import save_signal
from core.config import SCAN_INTERVAL


# memory
sent_tokens = set()
last_prices = {}
market_state = {}

def format_units(value):

    try:
        value = float(value)

        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        elif value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        elif value >= 1_000:
            return f"{value/1_000:.2f}K"

        else:
            return f"{value:.2f}"

    except:
        return value

def run_pipeline():

    print("Starting Blaz Intelligence scanner...")

    global market_state

    while True:

        try:

            print("Scanning market...")

            # ------------------------------------------------
            # 1 COLLECT MARKET DATA
            # ------------------------------------------------
            tokens = collect_market_data()

            # ------------------------------------------------
            # 2 MARKET SNAPSHOT (MAJOR COINS)
            # ------------------------------------------------
            leaders = detect_market_leaders(tokens)

            snapshot = "📊 *CRYPTO MARKET SNAPSHOT*\n\n"

            for coin in leaders:
                snapshot += f"""
{coin['symbol']}
Price: ${coin['price']}
Volume: ${format_units(coin['volume'])}
Liquidity: ${format_units(coin['liquidity'])}
"""

            send_telegram_alert(snapshot)

            # ------------------------------------------------
            # 3 MARKET SENTIMENT (PUMP / CRASH)
            # ------------------------------------------------
            sentiment, market_state = detect_market_sentiment(tokens, market_state)

            if sentiment == "PUMP":

                send_telegram_alert(
                    "🚀 *CRYPTO MARKET PUMP DETECTED*\nMajor coins rising together."
                )

            elif sentiment == "CRASH":

                send_telegram_alert(
                    "⚠️ *CRYPTO MARKET CRASH SIGNAL*\nMajor coins falling together."
                )

            # ------------------------------------------------
            # 4 MARKET MOVE ALERT (>1%)
            # ------------------------------------------------
            for coin in leaders:

                symbol = coin["symbol"]
                price = coin["price"]

                if symbol not in last_prices:
                    last_prices[symbol] = price
                    continue

                old_price = last_prices[symbol]

                if old_price <= 0:
                    continue

                change = ((price - old_price) / old_price) * 100

                last_prices[symbol] = price

                if abs(change) < 1:
                    continue

                direction = "📈 UP" if change > 0 else "📉 DOWN"

                message = f"""
📊 *MARKET MOVE*

Coin: {symbol}
Price: ${price}

Change: {change:.2f}% {direction}
"""

                send_telegram_alert(message)

            # ------------------------------------------------
            # 5 ALPHA TOKEN DETECTOR
            # ------------------------------------------------
            new_tokens = detect_new_tokens(tokens)
            alpha_tokens = calculate_alpha(new_tokens)
            signals = detect_hundred_x(alpha_tokens)

            print("Signals detected:", len(signals))

            for token in signals:

                symbol = token["symbol"]

                if symbol in sent_tokens:
                    continue

                sent_tokens.add(symbol)

                save_signal(token)

                message = f"""
🚨 *BLAZ SIGNAL*

Token: {symbol}
Price: ${token['price']}

Volume: ${format_units(token['volume'])}
Liquidity: ${format_units(token['liquidity'])}

Alpha Score: {token.get('alpha_score')}
100x Score: {token.get('hundred_x_score')}
"""

                send_telegram_alert(message)

        except Exception as e:

            print("Pipeline error:", e)

        time.sleep(SCAN_INTERVAL)