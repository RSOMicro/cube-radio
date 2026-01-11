from fastapi import FastAPI, APIRouter, Depends
from fastapi_health import health
from database import get_database
from remote_logger import setup_logging

logger = setup_logging()

router = APIRouter(tags=["health"])

# Example health conditions
def service_ready():
    return {"service": "online"}


def get_session():
    return True


def is_database_online():
    """
    Readiness check:
    - Returns True if DB is reachable
    - Returns False if connection/query fails
    """
    try:
        conn = get_database()
        db = conn.cursor()

        # SQLAlchemy session or engine
        db.execute("SELECT 1")

        return True
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        return False

# Attach the /health endpoint to this router
router.add_api_route("/liveness", health([service_ready]))
router.add_api_route("/readiness", health([is_database_online]))