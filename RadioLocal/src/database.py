from pymongo import MongoClient, errors
from config import settings
from fastapi import HTTPException
from remote_logger import setup_logging

logger = setup_logging()

def get_database():
    """
    Safely connects to MongoDB and returns a database reference.
    If the database is unavailable, raises a handled exception
    instead of crashing the service.
    """
    try:
        # Build URI
        uri = settings.db_url

        # Initialize client with timeout (avoid hanging)
        client = MongoClient(uri, serverSelectionTimeoutMS=500)

        # Ping to verify connection
        client.admin.command("ping")

        return client.get_database("radiodb")

    except errors.ServerSelectionTimeoutError as e:
        logger.error(f"MongoDB connection timeout: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

    except errors.ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise HTTPException(status_code=503, detail="Database not available")