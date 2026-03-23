from datetime import datetime, timezone

from app.core.exceptions import (
    BusinessRuleException,
    ConflictException,
    EntityNotFoundException,
)
from app.models.visit import Visit, VisitStatus
from app.repositories.doctor_repository import SQLAlchemyDoctorRepository
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.schemas.visit import VisitCreate


class VisitService:
    def __init__(
        self,
        visit_repository: SQLAlchemyVisitRepository,
        patient_repository: SQLAlchemyPatientRepository,
        doctor_repository: SQLAlchemyDoctorRepository,
    ) -> None:
        self._visit_repo = visit_repository
        self._patient_repo = patient_repository
        self._doctor_repo = doctor_repository

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Visit]:
        return await self._visit_repo.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Visit:
        visit = await self._visit_repo.get_by_id(id)
        if not visit:
            raise EntityNotFoundException("Visit", id)
        return visit

    async def get_by_patient(self, patient_id: int) -> list[Visit]:
        if not await self._patient_repo.get_by_id(patient_id):
            raise EntityNotFoundException("Patient", patient_id)
        return await self._visit_repo.get_by_patient_id(patient_id)

    async def get_by_doctor(self, doctor_id: int) -> list[Visit]:
        if not await self._doctor_repo.get_by_id(doctor_id):
            raise EntityNotFoundException("Doctor", doctor_id)
        return await self._visit_repo.get_by_doctor_id(doctor_id)

    async def create(self, data: VisitCreate) -> Visit:
        if not await self._patient_repo.get_by_id(data.patient_id):
            raise EntityNotFoundException("Patient", data.patient_id)

        if not await self._doctor_repo.get_by_id(data.doctor_id):
            raise EntityNotFoundException("Doctor", data.doctor_id)

        if data.scheduled_at <= datetime.now(timezone.utc):
            raise BusinessRuleException("Scheduled time must be in the future")

        conflicting = await self._visit_repo.get_conflicting(
            data.doctor_id, data.scheduled_at, data.duration_minutes
        )
        if conflicting:
            raise ConflictException(
                "Doctor already has appointment at this time"
            )

        visit = Visit(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            scheduled_at=data.scheduled_at,
            duration_minutes=data.duration_minutes,
            reason=data.reason,
            status=VisitStatus.SCHEDULED,
        )
        return await self._visit_repo.create(visit)

    async def complete(self, id: int) -> Visit:
        visit = await self.get_by_id(id)
        if visit.status == VisitStatus.CANCELLED:
            raise BusinessRuleException("Cannot complete a cancelled visit")
        return await self._visit_repo.update(
            id, {"status": VisitStatus.COMPLETED}
        )

    async def cancel(self, id: int) -> Visit:
        visit = await self.get_by_id(id)
        if visit.status == VisitStatus.COMPLETED:
            raise BusinessRuleException("Cannot cancel a completed visit")
        return await self._visit_repo.update(
            id, {"status": VisitStatus.CANCELLED}
        )
