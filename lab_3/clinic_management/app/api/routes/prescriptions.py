from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response

from app.api.dependencies import get_prescription_service
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse
from app.services.prescription_service import PrescriptionService

router = APIRouter()

#NOTE Comment on route like 
# GET api/prescriptions/ -> 200 OK

@router.get("/", response_model=list[PrescriptionResponse])
async def get_all_prescriptions(
    diagnosis_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: PrescriptionService = Depends(get_prescription_service),
):
    if diagnosis_id:
        return await service.get_by_diagnosis(diagnosis_id)
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=PrescriptionResponse)
async def get_prescription(
    id: int, service: PrescriptionService = Depends(get_prescription_service)
):
    return await service.get_by_id(id)


@router.post(
    "/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED
)
async def create_prescription(
    data: PrescriptionCreate,
    service: PrescriptionService = Depends(get_prescription_service),
):
    return await service.create(data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prescription(
    id: int, service: PrescriptionService = Depends(get_prescription_service)
):
    await service.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
