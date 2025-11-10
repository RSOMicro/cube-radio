from fastapi import FastAPI, APIRouter, Depends
from fastapi_health import health
from database import get_database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

# Example health conditions
def service_ready():
    return {"service": "online"}


def get_session():
    return True


def is_database_online():
    """
    Health check condition to verify MongoDB connection.
    Returns True if the database is reachable, False otherwise.
    """
    try:
        db = get_database()
        # Optionally try a lightweight query or ping if needed
        db.command("ping")
        return True
    except Exception as e:
        # Log the exception but don’t crash the health endpoint
        logger.error(f"DB Health check failed: {e}")
        return False

# Attach the /health endpoint to this router
router.add_api_route("/liveness", health([service_ready]))
router.add_api_route("/readiness", health([is_database_online]))