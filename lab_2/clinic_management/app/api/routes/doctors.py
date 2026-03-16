from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.api.dependencies import get_doctor_service
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from app.services.doctor_service import DoctorService

router = APIRouter()


@router.get("/", response_model=list[DoctorResponse])
def get_all_doctors(
    specialization: str | None = None,
    service: DoctorService = Depends(get_doctor_service),
):
    if specialization:
        return service.get_by_specialization(specialization)
    return service.get_all()


@router.get("/{id}", response_model=DoctorResponse)
def get_doctor(id: int, service: DoctorService = Depends(get_doctor_service)):
    return service.get_by_id(id)


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    data: DoctorCreate, service: DoctorService = Depends(get_doctor_service)
):
    return service.create(data)


@router.put("/{id}", response_model=DoctorResponse)
def update_doctor(
    id: int,
    data: DoctorUpdate,
    service: DoctorService = Depends(get_doctor_service),
):
    return service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(id: int, service: DoctorService = Depends(get_doctor_service)):
    service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
