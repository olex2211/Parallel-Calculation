import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.http_client import get_http_client
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.services.patient_client import PatientClient
from app.services.visit_service import VisitService


def get_patient_client(
    http_client: httpx.AsyncClient = Depends(get_http_client),
) -> PatientClient:
    return PatientClient(http_client)


def get_visit_service(
    session: AsyncSession = Depends(get_session),
    patient_client: PatientClient = Depends(get_patient_client),
) -> VisitService:
    return VisitService(
        SQLAlchemyVisitRepository(session),
        patient_client,
    )
