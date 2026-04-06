from fastapi import APIRouter, Depends, Query, status
from fastapi_cache.decorator import cache

from app.api.dependencies import get_visit_service
from app.core.cache import invalidate_visit
from app.core.config import settings
from app.schemas.visit import VisitCreate, VisitResponse
from app.services.visit_service import VisitService

router = APIRouter()


@router.get("/", response_model=list[VisitResponse])
async def get_all_visits(
    patient_id: int | None = None,
    doctor_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: VisitService = Depends(get_visit_service),
):
    if patient_id:
        return await service.get_by_patient(patient_id)
    if doctor_id:
        return await service.get_by_doctor(doctor_id)
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=VisitResponse)
@cache(expire=settings.CACHE_TTL, namespace="get_visit")
async def get_visit(id: int, service: VisitService = Depends(get_visit_service)):
    return await service.get_by_id(id)


@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    data: VisitCreate, service: VisitService = Depends(get_visit_service)
):
    return await service.create(data)


@router.patch("/{id}/complete", response_model=VisitResponse)
async def complete_visit(id: int, service: VisitService = Depends(get_visit_service)):
    result = await service.complete(id)
    await invalidate_visit(id)
    return result


@router.patch("/{id}/cancel", response_model=VisitResponse)
async def cancel_visit(id: int, service: VisitService = Depends(get_visit_service)):
    result = await service.cancel(id)
    await invalidate_visit(id)
    return result
