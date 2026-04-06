from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response

from app.api.dependencies import get_patient_service
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import PatientService

router = APIRouter()


@router.get("/", response_model=list[PatientResponse])
async def get_all_patients(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: PatientService = Depends(get_patient_service),
):
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=PatientResponse)
async def get_patient(id: int, service: PatientService = Depends(get_patient_service)):
    return await service.get_by_id(id)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    data: PatientCreate, service: PatientService = Depends(get_patient_service)
):
    return await service.create(data)


@router.put("/{id}", response_model=PatientResponse)
async def update_patient(
    id: int,
    data: PatientUpdate,
    service: PatientService = Depends(get_patient_service),
):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    id: int, service: PatientService = Depends(get_patient_service)
):
    await service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
