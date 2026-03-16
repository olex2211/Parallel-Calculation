from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.api.dependencies import get_prescription_service
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.services.prescription_service import PrescriptionService

router = APIRouter()


@router.get("/", response_model=list[PrescriptionResponse])
def get_all_prescriptions(
    diagnosis_id: int | None = None,
    service: PrescriptionService = Depends(get_prescription_service),
):
    if diagnosis_id:
        return service.get_by_diagnosis(diagnosis_id)
    return service.get_all()


@router.get("/{id}", response_model=PrescriptionResponse)
def get_prescription(
    id: int, service: PrescriptionService = Depends(get_prescription_service)
):
    return service.get_by_id(id)


@router.post(
    "/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED
)
def create_prescription(
    data: PrescriptionCreate,
    service: PrescriptionService = Depends(get_prescription_service),
):
    return service.create(data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prescription(
    id: int, service: PrescriptionService = Depends(get_prescription_service)
):
    service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
