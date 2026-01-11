from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import get_all_cors_headers
import uvicorn
import os

import config
from config import settings
from routes import auth_routes
from health import HealthService
from remote_logger import setup_logging

app = FastAPI(
    title="User Service",
    version="1.0.0",
    redirect_slashes=False
)

# SuperTokens middleware
app.add_middleware(get_middleware())

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

# Routers
app.include_router(auth_routes.router, prefix="/api/user")
app.include_router(HealthService.router, prefix="/api/user/health")

logger = setup_logging()

if __name__ == "__main__":
    logger.info("Service has started")
    IN_DOCKER = os.environ.get("IN_DOCKER") == "1"

    if IN_DOCKER:
        uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
    else:
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=settings.service_port,
            reload=True
        )