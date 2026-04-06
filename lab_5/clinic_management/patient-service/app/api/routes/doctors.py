from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response

from app.api.dependencies import get_doctor_service
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from app.services.doctor_service import DoctorService

router = APIRouter()


@router.get("/", response_model=list[DoctorResponse])
async def get_all_doctors(
    specialization: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: DoctorService = Depends(get_doctor_service),
):
    if specialization:
        return await service.get_by_specialization(specialization)
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=DoctorResponse)
async def get_doctor(id: int, service: DoctorService = Depends(get_doctor_service)):
    return await service.get_by_id(id)


@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    data: DoctorCreate, service: DoctorService = Depends(get_doctor_service)
):
    return await service.create(data)


@router.put("/{id}", response_model=DoctorResponse)
async def update_doctor(
    id: int,
    data: DoctorUpdate,
    service: DoctorService = Depends(get_doctor_service),
):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(
    id: int, service: DoctorService = Depends(get_doctor_service)
):
    await service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
