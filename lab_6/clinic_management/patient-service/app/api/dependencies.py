from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.doctor_repository import SQLAlchemyDoctorRepository
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.services.doctor_service import DoctorService
from app.services.patient_service import PatientService


def get_patient_service(
    session: AsyncSession = Depends(get_session),
) -> PatientService:
    return PatientService(SQLAlchemyPatientRepository(session))


def get_doctor_service(
    session: AsyncSession = Depends(get_session),
) -> DoctorService:
    return DoctorService(SQLAlchemyDoctorRepository(session))
