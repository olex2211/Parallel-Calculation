from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.doctor_repository import SQLAlchemyDoctorRepository
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.repositories.prescription_repository import SQLAlchemyPrescriptionRepository
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.services.diagnosis_service import DiagnosisService
from app.services.doctor_service import DoctorService
from app.services.patient_service import PatientService
from app.services.payment_service import PaymentService
from app.services.prescription_service import PrescriptionService
from app.services.treatment_history_service import TreatmentHistoryService
from app.services.visit_service import VisitService


def get_patient_service(
    session: AsyncSession = Depends(get_session),
) -> PatientService:
    return PatientService(SQLAlchemyPatientRepository(session))


def get_doctor_service(
    session: AsyncSession = Depends(get_session),
) -> DoctorService:
    return DoctorService(SQLAlchemyDoctorRepository(session))


def get_visit_service(
    session: AsyncSession = Depends(get_session),
) -> VisitService:
    return VisitService(
        SQLAlchemyVisitRepository(session),
        SQLAlchemyPatientRepository(session),
        SQLAlchemyDoctorRepository(session),
    )


def get_diagnosis_service(
    session: AsyncSession = Depends(get_session),
) -> DiagnosisService:
    return DiagnosisService(
        SQLAlchemyDiagnosisRepository(session),
        SQLAlchemyVisitRepository(session),
    )


def get_prescription_service(
    session: AsyncSession = Depends(get_session),
) -> PrescriptionService:
    return PrescriptionService(
        SQLAlchemyPrescriptionRepository(session),
        SQLAlchemyDiagnosisRepository(session),
    )


def get_payment_service(
    session: AsyncSession = Depends(get_session),
) -> PaymentService:
    return PaymentService(
        SQLAlchemyPaymentRepository(session),
        SQLAlchemyVisitRepository(session),
        SQLAlchemyDoctorRepository(session),
        SQLAlchemyDiagnosisRepository(session),
        SQLAlchemyPrescriptionRepository(session),
        SQLAlchemyPatientRepository(session),
    )


def get_treatment_history_service(
    session: AsyncSession = Depends(get_session),
) -> TreatmentHistoryService:
    return TreatmentHistoryService(
        SQLAlchemyPatientRepository(session),
        SQLAlchemyVisitRepository(session),
        SQLAlchemyDiagnosisRepository(session),
        SQLAlchemyPrescriptionRepository(session),
    )
