from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.prescription_repository import SQLAlchemyPrescriptionRepository
from app.schemas.diagnosis import DiagnosisResponse
from app.schemas.prescription import PrescriptionResponse
from app.schemas.treatment_history import TreatmentHistoryResponse, VisitDetail
from app.services.appointment_client import AppointmentClient

class TreatmentHistoryService:
    def __init__(
        self,
        appointment_client: AppointmentClient,
        diagnosis_repository: SQLAlchemyDiagnosisRepository,
        prescription_repository: SQLAlchemyPrescriptionRepository,
    ) -> None:
        self._appointment_client = appointment_client
        self._diagnosis_repo = diagnosis_repository
        self._prescription_repo = prescription_repository

    async def get_by_patient(self, patient_id: int) -> TreatmentHistoryResponse:
        # Cross-service call: GET /api/visits?patient_id={patient_id}
        visits = await self._appointment_client.get_visits_by_patient(patient_id)

        visit_details = []
        last_visit_at = None

        for visit in visits:
            diagnosis = await self._diagnosis_repo.get_by_visit_id(visit.id)
            diagnosis_response = None
            prescriptions_response = []

            if diagnosis:
                diagnosis_response = DiagnosisResponse.model_validate(
                    diagnosis, from_attributes=True
                )
                prescriptions = await self._prescription_repo.get_by_diagnosis_id(
                    diagnosis.id
                )
                prescriptions_response = [
                    PrescriptionResponse.model_validate(p, from_attributes=True)
                    for p in prescriptions
                ]

            visit_details.append(
                VisitDetail(
                    visit=visit,
                    diagnosis=diagnosis_response,
                    prescriptions=prescriptions_response,
                )
            )

            if last_visit_at is None or visit.scheduled_at > last_visit_at:
                last_visit_at = visit.scheduled_at

        return TreatmentHistoryResponse(
            patient_id=patient_id,
            visits=visit_details,
            total_visits=len(visits),
            last_visit_at=last_visit_at,
        )
