from fastapi import APIRouter
from app.core.config import settings
from app.api.routes import payments

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(payments.router, prefix="/payments", tags=["Payments"])
