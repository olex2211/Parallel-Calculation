from app.core.exceptions import EntityNotFoundException
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.repositories.prescription_repository import SQLAlchemyPrescriptionRepository
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.schemas.diagnosis import DiagnosisResponse
from app.schemas.prescription import PrescriptionResponse
from app.schemas.treatment_history import TreatmentHistoryResponse, VisitDetail
from app.schemas.visit import VisitResponse


class TreatmentHistoryService:
    def __init__(
        self,
        patient_repository: SQLAlchemyPatientRepository,
        visit_repository: SQLAlchemyVisitRepository,
        diagnosis_repository: SQLAlchemyDiagnosisRepository,
        prescription_repository: SQLAlchemyPrescriptionRepository,
    ) -> None:
        self._patient_repo = patient_repository
        self._visit_repo = visit_repository
        self._diagnosis_repo = diagnosis_repository
        self._prescription_repo = prescription_repository

    async def get_by_patient(self, patient_id: int) -> TreatmentHistoryResponse:
        # 1. Перевірити що пацієнт існує
        patient = await self._patient_repo.get_by_id(patient_id)
        if not patient:
            raise EntityNotFoundException("Patient", patient_id)

        # 2. Отримати всі візити пацієнта
        visits = await self._visit_repo.get_by_patient_id(patient_id)

        # 3. Для кожного візиту отримати діагноз та призначення
        visit_details = []
        last_visit_at = None

        for visit in visits:
            visit_response = VisitResponse.model_validate(visit, from_attributes=True)

            # Отримати діагноз
            diagnosis = await self._diagnosis_repo.get_by_visit_id(visit.id)
            diagnosis_response = None
            prescriptions_response = []

            if diagnosis:
                diagnosis_response = DiagnosisResponse.model_validate(
                    diagnosis, from_attributes=True
                )
                # Отримати призначення для діагнозу
                prescriptions = await self._prescription_repo.get_by_diagnosis_id(
                    diagnosis.id
                )
                prescriptions_response = [
                    PrescriptionResponse.model_validate(p, from_attributes=True)
                    for p in prescriptions
                ]

            visit_details.append(
                VisitDetail(
                    visit=visit_response,
                    diagnosis=diagnosis_response,
                    prescriptions=prescriptions_response,
                )
            )

            # Визначити дату останнього візиту
            if last_visit_at is None or visit.scheduled_at > last_visit_at:
                last_visit_at = visit.scheduled_at

        # 4. Зібрати агрегований об'єкт
        return TreatmentHistoryResponse(
            patient_id=patient_id,
            visits=visit_details,
            total_visits=len(visits),
            last_visit_at=last_visit_at,
        )
