from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_diagnosis_service
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisResponse
from app.services.diagnosis_service import DiagnosisService

router = APIRouter()


@router.get("/", response_model=list[DiagnosisResponse])
async def get_all_diagnoses(
    visit_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: DiagnosisService = Depends(get_diagnosis_service),
):
    if visit_id:
        return await service.get_by_visit(visit_id)
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=DiagnosisResponse)
async def get_diagnosis(
    id: int, service: DiagnosisService = Depends(get_diagnosis_service)
):
    return await service.get_by_id(id)


@router.post(
    "/", response_model=DiagnosisResponse, status_code=status.HTTP_201_CREATED
)
async def create_diagnosis(
    data: DiagnosisCreate,
    service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await service.create(data)
