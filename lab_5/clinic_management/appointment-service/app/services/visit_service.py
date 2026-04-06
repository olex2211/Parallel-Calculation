from datetime import datetime, timezone

from app.core.exceptions import (
    BusinessRuleException,
    ConflictException,
    EntityNotFoundException,
)
from app.models.visit import Visit, VisitStatus
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.schemas.visit import VisitCreate
from app.services.patient_client import PatientClient


class VisitService:
    def __init__(
        self,
        visit_repository: SQLAlchemyVisitRepository,
        patient_client: PatientClient,
    ) -> None:
        self._visit_repo = visit_repository
        self._patient_client = patient_client

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Visit]:
        return await self._visit_repo.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Visit:
        visit = await self._visit_repo.get_by_id(id)
        if not visit:
            raise EntityNotFoundException("Visit", id)
        return visit

    async def get_by_patient(self, patient_id: int) -> list[Visit]:
        # Validate patient exists
        await self._patient_client.get_patient(patient_id)
        return await self._visit_repo.get_by_patient_id(patient_id)

    async def get_by_doctor(self, doctor_id: int) -> list[Visit]:
        # Validate doctor exists
        await self._patient_client.get_doctor(doctor_id)
        return await self._visit_repo.get_by_doctor_id(doctor_id)

    async def create(self, data: VisitCreate) -> Visit:
        # Cross-service validation
        await self._patient_client.get_patient(data.patient_id)
        doctor = await self._patient_client.get_doctor(data.doctor_id)

        if data.scheduled_at <= datetime.now(timezone.utc):
            raise BusinessRuleException("Scheduled time must be in the future")

        # Local validation
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
            doctor_hourly_rate=doctor.hourly_rate,
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
