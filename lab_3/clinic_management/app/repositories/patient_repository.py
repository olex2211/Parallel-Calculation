from sqlalchemy import select

from app.models.patient import Patient
from app.repositories.base import BaseRepository


class SQLAlchemyPatientRepository(BaseRepository[Patient]):
    #NOTE implement explicit override by decorator
    #@override
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        result = await self.session.execute(
            select(Patient).order_by(Patient.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.id == id)
        )
        return result.scalar_one_or_none()

    async def create(self, entity: Patient) -> Patient:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Patient | None:
        patient = await self.get_by_id(id)
        if not patient:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(patient, key, value)
        return await self._commit_and_refresh(patient)

    async def delete(self, id: int) -> bool:
        patient = await self.get_by_id(id)
        if not patient:
            return False
        await self.session.delete(patient)
        await self.session.commit()
        return True
