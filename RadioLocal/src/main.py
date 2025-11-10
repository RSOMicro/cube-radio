import uvicorn
from fastapi import FastAPI
from routes import station_routes
from health import HealthService
from config import settings

from fastapi.openapi.utils import get_openapi

app = FastAPI(title="RadioLocal Service", version="1.0.0")
app.include_router(prefix="/api/radio", router=station_routes.router)
app.include_router(prefix="/api/radio/health", router=HealthService.router)



@app.get("/")
def health_check():
    return {"status": "RadioLocal is running"}

#Add OpenAPI/Swagget Authenticate button
# Add security schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="RadioLocal microservice for managing radio stations.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.service_port, reload=True)