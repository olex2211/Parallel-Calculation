from fastapi import APIRouter

from app.api.routes import (
    diagnoses,
    doctors,
    patients,
    payments,
    prescriptions,
    treatment_history,
    visits,
)

router = APIRouter(prefix="/api")

router.include_router(patients.router, prefix="/patients", tags=["Patients"])
router.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
router.include_router(visits.router, prefix="/visits", tags=["Visits"])
router.include_router(diagnoses.router, prefix="/diagnoses", tags=["Diagnoses"])
router.include_router(
    prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"]
)
router.include_router(
    treatment_history.router, prefix="/treatment-history", tags=["Treatment History"]
)
router.include_router(payments.router, prefix="/payments", tags=["Payments"])
