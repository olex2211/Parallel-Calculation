from fastapi import APIRouter
from app.core.config import settings

from app.api.routes import doctors, patients

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(patients.router, prefix="/patients", tags=["Patients"])
router.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
