from fastapi import APIRouter
from app.core.config import settings

from app.api.routes import diagnoses, prescriptions, treatment_history

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(diagnoses.router, prefix="/diagnoses", tags=["Diagnoses"])
router.include_router(
    prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"]
)
router.include_router(
    treatment_history.router, prefix="/treatment-history", tags=["Treatment History"]
)
