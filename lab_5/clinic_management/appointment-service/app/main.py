from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from sqlalchemy import text

from app.api.router import router
from app.core.config import settings
from app.core.database import engine
from app.core.error_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(5.0),
        follow_redirects=True,
    )
    yield
    await app.state.http_client.aclose()
    await engine.dispose()


app = FastAPI(
    title=settings.SERVICE_NAME,
    lifespan=lifespan,
    docs_url="/docs/appointments",
    openapi_url="/openapi/appointments.json",
    redoc_url="/redoc/appointments",
)

register_exception_handlers(app)
app.include_router(router)


@app.get("/health", tags=["System"])
async def health_check():
    health = {"status": "ok", "service": settings.SERVICE_NAME, "database": "ok"}
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        health["database"] = "unavailable"
    return health
