from fastapi import APIRouter
from app.core.config import settings

from app.api.routes import visits

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(visits.router, prefix="/visits", tags=["Visits"])
