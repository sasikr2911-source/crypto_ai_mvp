from fastapi import APIRouter
from database.db_manager import get_signal_history

router = APIRouter()


@router.get("/signals/history")
def signal_history():

    history = get_signal_history()

    return {
        "status": "success",
        "count": len(history),
        "signals": history
    }