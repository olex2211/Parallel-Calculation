from app.core.exceptions import BusinessRuleException, EntityNotFoundException
from app.models.diagnosis import Diagnosis
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.schemas.diagnosis import DiagnosisCreate
from app.services.appointment_client import AppointmentClient


class DiagnosisService:
    def __init__(
        self,
        diagnosis_repository: SQLAlchemyDiagnosisRepository,
        appointment_client: AppointmentClient,
    ) -> None:
        self._diagnosis_repo = diagnosis_repository
        self._appointment_client = appointment_client

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Diagnosis]:
        return await self._diagnosis_repo.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Diagnosis:
        diagnosis = await self._diagnosis_repo.get_by_id(id)
        if not diagnosis:
            raise EntityNotFoundException("Diagnosis", id)
        return diagnosis

    async def get_by_visit(self, visit_id: int) -> list[Diagnosis]:
        diagnosis = await self._diagnosis_repo.get_by_visit_id(visit_id)
        return [diagnosis] if diagnosis else []

    async def create(self, data: DiagnosisCreate) -> Diagnosis:
        # Cross-service verification
        visit = await self._appointment_client.get_visit(data.visit_id)

        # 2. Check that visit is completed
        if visit.status != "completed":
            raise BusinessRuleException(
                "Cannot create diagnosis for a visit that is not completed"
            )

        # 3. Check uniqueness locally
        existing = await self._diagnosis_repo.get_by_visit_id(data.visit_id)
        if existing:
            raise BusinessRuleException("Visit already has a diagnosis")

        diagnosis = Diagnosis(
            visit_id=data.visit_id,
            icd_code=data.icd_code,
            title=data.title,
            description=data.description,
            severity=data.severity,
        )
        return await self._diagnosis_repo.create(diagnosis)
