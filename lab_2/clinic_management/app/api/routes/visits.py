from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_visit_service
from app.schemas.visit import VisitCreate, VisitResponse
from app.services.visit_service import VisitService

router = APIRouter()


@router.get("/", response_model=list[VisitResponse])
def get_all_visits(
    patient_id: int | None = None,
    doctor_id: int | None = None,
    service: VisitService = Depends(get_visit_service),
):
    if patient_id:
        return service.get_by_patient(patient_id)
    if doctor_id:
        return service.get_by_doctor(doctor_id)
    return service.get_all()


@router.get("/{id}", response_model=VisitResponse)
def get_visit(id: int, service: VisitService = Depends(get_visit_service)):
    return service.get_by_id(id)


@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
def create_visit(
    data: VisitCreate, service: VisitService = Depends(get_visit_service)
):
    return service.create(data)


@router.patch("/{id}/complete", response_model=VisitResponse)
def complete_visit(id: int, service: VisitService = Depends(get_visit_service)):
    return service.complete(id)


@router.patch("/{id}/cancel", response_model=VisitResponse)
def cancel_visit(id: int, service: VisitService = Depends(get_visit_service)):
    return service.cancel(id)
