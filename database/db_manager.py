import sqlite3
from datetime import datetime

DB_NAME = "crypto_ai.db"


# Initialize database
def init_db():

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            volume REAL,
            liquidity REAL,
            alpha_score REAL,
            hundred_x_score REAL,
            timestamp TEXT
        )
        """)

        # index for faster searches
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_symbol
        ON signals(symbol)
        """)

        conn.commit()


# Save signal
def save_signal(token):

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO signals
        (symbol, price, volume, liquidity, alpha_score, hundred_x_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            token["symbol"],
            token["price"],
            token["volume"],
            token["liquidity"],
            token.get("alpha_score"),
            token.get("hundred_x_score"),
            datetime.utcnow().isoformat()
        ))

        conn.commit()


# Get latest signals
def get_signal_history(limit=50):

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT symbol, price, volume, liquidity, alpha_score, hundred_x_score, timestamp
        FROM signals
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({
            "symbol": row[0],
            "price": row[1],
            "volume": row[2],
            "liquidity": row[3],
            "alpha_score": row[4],
            "hundred_x_score": row[5],
            "timestamp": row[6]
        })

    return results


# Get latest single signal
def get_latest_signal():

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute("""
        SELECT symbol, price, volume, liquidity, alpha_score, hundred_x_score, timestamp
        FROM signals
        ORDER BY id DESC
        LIMIT 1
        """)

        row = cursor.fetchone()

    if not row:
        return None

    return {
        "symbol": row[0],
        "price": row[1],
        "volume": row[2],
        "liquidity": row[3],
        "alpha_score": row[4],
        "hundred_x_score": row[5],
        "timestamp": row[6]
    }