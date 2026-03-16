from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.api.dependencies import get_patient_service
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import PatientService

router = APIRouter()


@router.get("/", response_model=list[PatientResponse])
def get_all_patients(service: PatientService = Depends(get_patient_service)):
    return service.get_all()


@router.get("/{id}", response_model=PatientResponse)
def get_patient(id: int, service: PatientService = Depends(get_patient_service)):
    return service.get_by_id(id)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    data: PatientCreate, service: PatientService = Depends(get_patient_service)
):
    return service.create(data)


@router.put("/{id}", response_model=PatientResponse)
def update_patient(
    id: int,
    data: PatientUpdate,
    service: PatientService = Depends(get_patient_service),
):
    return service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, service: PatientService = Depends(get_patient_service)):
    service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
