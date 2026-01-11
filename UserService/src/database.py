import time
import jwt

import mysql.connector
from mysql.connector import errors, pooling
from fastapi import HTTPException
from config import settings
from models.user_model import UserCreate
from remote_logger import setup_logging

logger = setup_logging()

# Create a connection pool at import time
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="radiodb_pool",
        pool_size=5,
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        connection_timeout=5,
    )
except Exception as e:
    logger.critical(f"Failed to create MySQL connection pool: {e}")
    db_pool = None


def get_database():
    """
    Safely gets a MySQL connection from the pool.
    If the database is unavailable, raises a handled exception
    instead of crashing the service.
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        conn = db_pool.get_connection()

        # MySQL "ping" equivalent
        conn.ping(reconnect=True, attempts=1, delay=0)

        return conn

    except errors.PoolError as e:
        logger.error(f"MySQL pool exhausted: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

    except errors.InterfaceError as e:
        logger.error(f"MySQL interface error: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

    except errors.OperationalError as e:
        logger.error(f"MySQL operational error: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise HTTPException(status_code=503, detail="Database not available")

def insert_user(user_id: str, user: UserCreate) -> None:
    """
    Inserts a user created by SuperTokens into the MySQL users table.
    """
    conn = get_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (user_id, email, name, lastname, company_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                user.email,
                user.name,
                user.lastname,
                user.company_id,
            )
        )
        conn.commit()

    except mysql.connector.IntegrityError as e:
        logger.warning(f"User already exists ({user_id}): {e}")

    except mysql.connector.Error as e:
        logger.error(f"Failed to insert user {user_id}: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

def get_current_user(_user_id: str, ACCESS_TOKEN_EXPIRE_SECONDS: int) -> str:
    """
    Fetches the user from the database and returns a SIGNED JWT.
    """
    conn = get_database()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT company_id, name, lastname
            FROM users
            WHERE user_id = %s
            """,
            (_user_id,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        payload = {
            "company_id": str(user["company_id"]),
            "user_id": _user_id,
            "name": str(user["name"]),
            "lastname": str(user["lastname"]),
            "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS,
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm="HS256",
        )

        # PyJWT >= 2.x returns str, <2.x returns bytes
        return token if isinstance(token, str) else token.decode("utf-8")


    except mysql.connector.Error as e:
        logger.error(f"Failed to fetch user {_user_id}: {e}")
        raise HTTPException(status_code=503, detail="Database error")

    finally:
        cursor.close()
        conn.close()

def create_tenant(name: str, size: int) -> int:
    conn = get_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO teenant (name, size)
            VALUES (%s, %s)
            """,
            (name, size)
        )
        conn.commit()
        return cursor.lastrowid

    except mysql.connector.IntegrityError as e:
        logger.warning(f"Tenant already exists: {name}")
        raise HTTPException(status_code=409, detail="Tenant already exists")

    except mysql.connector.Error as e:
        logger.error(f"Failed to create tenant {name}: {e}")
        raise HTTPException(status_code=503, detail="Database error")

    finally:
        cursor.close()
        conn.close()

def assign_user_to_tenant(user_id: str, tenant_id: int):
    conn = get_database()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET company_id = %s
            WHERE user_id = %s
            """,
            (tenant_id, user_id)
        )
        conn.commit()

    finally:
        cursor.close()
        conn.close()

def get_company_by_user_id(user_id: str) -> dict:
    """
    Returns the tenant (company) the user belongs to.
    """
    conn = get_database()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                t.teenant_id AS tenant_id,
                t.name       AS tenant_name,
                t.size       AS tenant_size
            FROM users u
            JOIN teenant t ON t.teenant_id = u.company_id
            WHERE u.user_id = %s
            """,
            (user_id,)
        )

        company = cursor.fetchone()

        if not company:
            raise HTTPException(
                status_code=404,
                detail="User does not belong to any tenant"
            )

        return company

    except mysql.connector.Error as e:
        logger.error(f"Failed to get company for user {user_id}: {e}")
        raise HTTPException(status_code=503, detail="Database error")

    finally:
        cursor.close()
        conn.close()