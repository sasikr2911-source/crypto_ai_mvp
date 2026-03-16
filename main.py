from fastapi import FastAPI
import threading
import logging

from api.routes_market import router as market_router
from api.routes_signals import router as signals_router

from database.db_manager import init_db
from core.scheduler import run_pipeline


# ---------------------------------------------------
# Logging configuration
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("blaz-intelligence")


# ---------------------------------------------------
# Initialize database
# ---------------------------------------------------
init_db()


# ---------------------------------------------------
# FastAPI app
# ---------------------------------------------------
app = FastAPI(
    title="Blaz Intelligence",
    description="AI Crypto Market Intelligence Engine",
    version="1.0"
)


# ---------------------------------------------------
# API routes
# ---------------------------------------------------
app.include_router(market_router)
app.include_router(signals_router)


# ---------------------------------------------------
# Root endpoint (health check)
# ---------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Blaz Intelligence",
        "version": "1.0"
    }


# ---------------------------------------------------
# Background scanner thread
# ---------------------------------------------------
def start_scanner():

    logger.info("Starting Blaz Intelligence scanner thread...")

    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Scanner crashed: {e}")


# ---------------------------------------------------
# Startup event
# ---------------------------------------------------
@app.on_event("startup")
def startup_event():

    logger.info("Initializing Blaz Intelligence API")

    scanner_thread = threading.Thread(
        target=start_scanner,
        daemon=True
    )

    scanner_thread.start()

    logger.info("Scanner started successfully")