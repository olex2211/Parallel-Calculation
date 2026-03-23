from datetime import timedelta

from sqlalchemy import and_, select

from app.models.visit import Visit, VisitStatus
from app.repositories.base import BaseRepository


class SQLAlchemyVisitRepository(BaseRepository[Visit]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Visit]:
        result = await self.session.execute(
            select(Visit).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Visit | None:
        result = await self.session.execute(
            select(Visit).where(Visit.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_patient_id(self, patient_id: int) -> list[Visit]:
        result = await self.session.execute(
            select(Visit).where(Visit.patient_id == patient_id)
        )
        return list(result.scalars().all())

    async def get_by_doctor_id(self, doctor_id: int) -> list[Visit]:
        result = await self.session.execute(
            select(Visit).where(Visit.doctor_id == doctor_id)
        )
        return list(result.scalars().all())

    async def get_by_status(self, status: VisitStatus) -> list[Visit]:
        result = await self.session.execute(
            select(Visit).where(Visit.status == status)
        )
        return list(result.scalars().all())

    async def get_conflicting(
        self, doctor_id: int, scheduled_at, duration_minutes: int
    ) -> Visit | None:
        """Перевірити перетин часових проміжків для лікаря на рівні SQL."""
        new_end = scheduled_at + timedelta(minutes=duration_minutes)

        result = await self.session.execute(
            select(Visit).where(
                and_(
                    Visit.doctor_id == doctor_id,
                    Visit.status != VisitStatus.CANCELLED,
                    Visit.scheduled_at < new_end,
                    (
                        Visit.scheduled_at
                        + timedelta(minutes=1) * Visit.duration_minutes
                    )
                    > scheduled_at,
                )
            )
        )
        return result.scalars().first()

    async def create(self, entity: Visit) -> Visit:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Visit | None:
        visit = await self.get_by_id(id)
        if not visit:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(visit, key, value)
        return await self._commit_and_refresh(visit)

    async def delete(self, id: int) -> bool:
        visit = await self.get_by_id(id)
        if not visit:
            return False
        await self.session.delete(visit)
        await self.session.commit()
        return True
