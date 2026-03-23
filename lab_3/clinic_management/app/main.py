from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings
from app.core.database import engine
from app.core.error_handlers import register_exception_handlers



#  Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


#  App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Medical Clinic Management System — Lab Work #3",
    version="2.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(router)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}