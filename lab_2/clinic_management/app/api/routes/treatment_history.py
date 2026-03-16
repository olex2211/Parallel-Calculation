from fastapi import APIRouter, Depends

from app.api.dependencies import get_treatment_history_service
from app.schemas.treatment_history import TreatmentHistoryResponse
from app.services.treatment_history_service import TreatmentHistoryService

router = APIRouter()


@router.get("/{patient_id}", response_model=TreatmentHistoryResponse)
def get_treatment_history(
    patient_id: int,
    service: TreatmentHistoryService = Depends(get_treatment_history_service),
):
    return service.get_by_patient(patient_id)
