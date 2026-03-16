from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_payment_service
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter()


@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(
    patient_id: int | None = None,
    service: PaymentService = Depends(get_payment_service),
):
    if patient_id:
        return service.get_by_patient(patient_id)
    return service.get_all()


@router.get("/{id}", response_model=PaymentResponse)
def get_payment(id: int, service: PaymentService = Depends(get_payment_service)):
    return service.get_by_id(id)


@router.post(
    "/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED
)
def create_payment(
    data: PaymentCreate, service: PaymentService = Depends(get_payment_service)
):
    return service.create(data)


@router.patch("/{id}/pay", response_model=PaymentResponse)
def pay_payment(id: int, service: PaymentService = Depends(get_payment_service)):
    return service.pay(id)


@router.patch("/{id}/cancel", response_model=PaymentResponse)
def cancel_payment(id: int, service: PaymentService = Depends(get_payment_service)):
    return service.cancel(id)
