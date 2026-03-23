from app.core.exceptions import BusinessRuleException, EntityNotFoundException
from app.models.diagnosis import Diagnosis
from app.models.visit import VisitStatus
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.schemas.diagnosis import DiagnosisCreate


class DiagnosisService:
    def __init__(
        self,
        diagnosis_repository: SQLAlchemyDiagnosisRepository,
        visit_repository: SQLAlchemyVisitRepository,
    ) -> None:
        self._diagnosis_repo = diagnosis_repository
        self._visit_repo = visit_repository

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
        # 1. Перевірити що visit_id існує
        visit = await self._visit_repo.get_by_id(data.visit_id)
        if not visit:
            raise EntityNotFoundException("Visit", data.visit_id)

        # 2. Перевірити що візит завершений
        if visit.status != VisitStatus.COMPLETED:
            raise BusinessRuleException(
                "Cannot create diagnosis for a visit that is not completed"
            )

        # 3. Перевірити що для цього візиту ще немає діагнозу
        existing = await self._diagnosis_repo.get_by_visit_id(data.visit_id)
        if existing:
            raise BusinessRuleException("Visit already has a diagnosis")

        # 4. Створити діагноз
        diagnosis = Diagnosis(
            visit_id=data.visit_id,
            icd_code=data.icd_code,
            title=data.title,
            description=data.description,
            severity=data.severity,
        )
        return await self._diagnosis_repo.create(diagnosis)
