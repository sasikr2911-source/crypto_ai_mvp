from fastapi import APIRouter
from collectors.market_collector import collect_market_data
import time

router = APIRouter()


@router.get("/market/trending")
def get_trending():

    try:

        data = collect_market_data()[:20]

        return {
            "status": "success",
            "timestamp": int(time.time()),
            "tokens": data
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }