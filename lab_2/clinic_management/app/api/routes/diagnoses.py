from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_diagnosis_service
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisResponse
from app.services.diagnosis_service import DiagnosisService

router = APIRouter()


@router.get("/", response_model=list[DiagnosisResponse])
def get_all_diagnoses(
    visit_id: int | None = None,
    service: DiagnosisService = Depends(get_diagnosis_service),
):
    if visit_id:
        return service.get_by_visit(visit_id)
    return service.get_all()


@router.get("/{id}", response_model=DiagnosisResponse)
def get_diagnosis(id: int, service: DiagnosisService = Depends(get_diagnosis_service)):
    return service.get_by_id(id)


@router.post(
    "/", response_model=DiagnosisResponse, status_code=status.HTTP_201_CREATED
)
def create_diagnosis(
    data: DiagnosisCreate,
    service: DiagnosisService = Depends(get_diagnosis_service),
):
    return service.create(data)
