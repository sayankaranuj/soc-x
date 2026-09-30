from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

try:
    from app.database import engine
    from app.routes.logs import router as logs_router
    from app.routes.alerts import router as alerts_router
    from app.routes.dashboard import router as dashboard_router
except ModuleNotFoundError:
    from backend.app.database import engine
    from backend.app.routes.logs import router as logs_router
    from backend.app.routes.alerts import router as alerts_router
    from backend.app.routes.dashboard import router as dashboard_router


app = FastAPI(
    title="SOC-X",
    description="Security Operations Center Monitoring Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8001",
        "http://localhost:8001",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(logs_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "SOC-X backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "soc-x-backend"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "MySQL"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }