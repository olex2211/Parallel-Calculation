from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import router
from app.core.cache import close_cache, init_cache
from app.core.config import settings
from app.core.database import engine
from app.core.error_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_cache()
    yield
    await close_cache()
    await engine.dispose()


app = FastAPI(
    title=settings.SERVICE_NAME,
    lifespan=lifespan,
    docs_url="/docs/patients",
    openapi_url="/openapi/patients.json",
    redoc_url="/redoc/patients",
)

register_exception_handlers(app)
app.include_router(router)


@app.get("/health", tags=["System"])
async def health_check():
    health = {
        "status": "ok",
        "service": settings.SERVICE_NAME,
        "database": "ok",
        "cache": "ok",
    }
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        health["database"] = "unavailable"
    try:
        from app.core.cache import redis_client

        if redis_client:
            await redis_client.ping()
        else:
            health["cache"] = "unavailable"
    except Exception:
        health["cache"] = "unavailable"
    return health
