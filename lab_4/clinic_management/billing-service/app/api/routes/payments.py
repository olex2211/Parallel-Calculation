from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_payment_service
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter()

@router.get("/", response_model=list[PaymentResponse])
async def get_all_payments(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    service: PaymentService = Depends(get_payment_service),
):
    return await service.get_all(skip, limit)


@router.get("/{id}", response_model=PaymentResponse)
async def get_payment(
    id: int, service: PaymentService = Depends(get_payment_service)
):
    return await service.get_by_id(id)


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    data: PaymentCreate, service: PaymentService = Depends(get_payment_service)
):
    return await service.create(data)


@router.patch("/{id}/complete", response_model=PaymentResponse)
async def complete_payment(
    id: int, service: PaymentService = Depends(get_payment_service)
):
    return await service.complete_payment(id)


@router.patch("/{id}/refund", response_model=PaymentResponse)
async def refund_payment(
    id: int, service: PaymentService = Depends(get_payment_service)
):
    return await service.refund_payment(id)
