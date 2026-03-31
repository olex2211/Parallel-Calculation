import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.http_client import get_http_client
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.prescription_repository import SQLAlchemyPrescriptionRepository
from app.services.appointment_client import AppointmentClient
from app.services.diagnosis_service import DiagnosisService
from app.services.prescription_service import PrescriptionService
from app.services.treatment_history_service import TreatmentHistoryService


def get_appointment_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> AppointmentClient:
    return AppointmentClient(http_client)


def get_diagnosis_service(
    session: AsyncSession = Depends(get_session),
    appointment_client: AppointmentClient = Depends(get_appointment_client),
) -> DiagnosisService:
    return DiagnosisService(
        SQLAlchemyDiagnosisRepository(session),
        appointment_client,
    )


def get_prescription_service(
    session: AsyncSession = Depends(get_session),
) -> PrescriptionService:
    return PrescriptionService(
        SQLAlchemyPrescriptionRepository(session),
        SQLAlchemyDiagnosisRepository(session),
    )


def get_treatment_history_service(
    session: AsyncSession = Depends(get_session),
    appointment_client: AppointmentClient = Depends(get_appointment_client),
) -> TreatmentHistoryService:
    return TreatmentHistoryService(
        appointment_client,
        SQLAlchemyDiagnosisRepository(session),
        SQLAlchemyPrescriptionRepository(session),
    )
