import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.http_client import get_http_client
from app.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.services.appointment_client import AppointmentClient
from app.services.payment_service import PaymentService
from app.services.treatment_client import TreatmentClient

def get_appointment_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> AppointmentClient:
    return AppointmentClient(http_client)


def get_treatment_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> TreatmentClient:
    return TreatmentClient(http_client)


def get_payment_service(
    session: AsyncSession = Depends(get_session),
    appointment_client: AppointmentClient = Depends(get_appointment_client),
    treatment_client: TreatmentClient = Depends(get_treatment_client),
) -> PaymentService:
    return PaymentService(
        SQLAlchemyPaymentRepository(session),
        appointment_client,
        treatment_client,
    )
