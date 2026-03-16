from app.repositories.diagnosis_repository import InMemoryDiagnosisRepository
from app.repositories.doctor_repository import InMemoryDoctorRepository
from app.repositories.patient_repository import InMemoryPatientRepository
from app.repositories.payment_repository import InMemoryPaymentRepository
from app.repositories.prescription_repository import InMemoryPrescriptionRepository
from app.repositories.visit_repository import InMemoryVisitRepository
from app.services.diagnosis_service import DiagnosisService
from app.services.doctor_service import DoctorService
from app.services.patient_service import PatientService
from app.services.payment_service import PaymentService
from app.services.prescription_service import PrescriptionService
from app.services.treatment_history_service import TreatmentHistoryService
from app.services.visit_service import VisitService

# Singleton репозиторії
_patient_repo = InMemoryPatientRepository()
_doctor_repo = InMemoryDoctorRepository()
_visit_repo = InMemoryVisitRepository()
_diagnosis_repo = InMemoryDiagnosisRepository()
_prescription_repo = InMemoryPrescriptionRepository()
_payment_repo = InMemoryPaymentRepository()


def get_patient_service() -> PatientService:
    return PatientService(_patient_repo)


def get_doctor_service() -> DoctorService:
    return DoctorService(_doctor_repo)


def get_visit_service() -> VisitService:
    return VisitService(_visit_repo, _patient_repo, _doctor_repo)


def get_diagnosis_service() -> DiagnosisService:
    return DiagnosisService(_diagnosis_repo, _visit_repo)


def get_prescription_service() -> PrescriptionService:
    return PrescriptionService(_prescription_repo, _diagnosis_repo)


def get_payment_service() -> PaymentService:
    return PaymentService(
        _payment_repo, _visit_repo, _doctor_repo,
        _diagnosis_repo, _prescription_repo,
        _patient_repo,
    )


def get_treatment_history_service() -> TreatmentHistoryService:
    return TreatmentHistoryService(
        _patient_repo, _visit_repo, _diagnosis_repo, _prescription_repo
    )
