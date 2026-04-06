from sqlalchemy import select

from app.models.prescription import Prescription
from app.repositories.base import BaseRepository


class SQLAlchemyPrescriptionRepository(BaseRepository[Prescription]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Prescription]:
        result = await self.session.execute(
            select(Prescription).order_by(Prescription.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Prescription | None:
        result = await self.session.execute(
            select(Prescription).where(Prescription.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_diagnosis_id(self, diagnosis_id: int) -> list[Prescription]:
        result = await self.session.execute(
            select(Prescription).where(
                Prescription.diagnosis_id == diagnosis_id
            )
        )
        return list(result.scalars().all())

    async def create(self, entity: Prescription) -> Prescription:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Prescription | None:
        prescription = await self.get_by_id(id)
        if not prescription:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(prescription, key, value)
        return await self._commit_and_refresh(prescription)

    async def delete(self, id: int) -> bool:
        prescription = await self.get_by_id(id)
        if not prescription:
            return False
        await self.session.delete(prescription)
        await self.session.commit()
        return True
