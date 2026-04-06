from sqlalchemy import select

from app.models.doctor import Doctor
from app.repositories.base import BaseRepository


class SQLAlchemyDoctorRepository(BaseRepository[Doctor]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Doctor]:
        result = await self.session.execute(
            select(Doctor).order_by(Doctor.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Doctor | None:
        result = await self.session.execute(
            select(Doctor).where(Doctor.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_specialization(self, specialization: str) -> list[Doctor]:
        result = await self.session.execute(
            select(Doctor).where(
                Doctor.specialization.ilike(f"%{specialization}%")
            )
        )
        return list(result.scalars().all())

    async def create(self, entity: Doctor) -> Doctor:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Doctor | None:
        doctor = await self.get_by_id(id)
        if not doctor:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(doctor, key, value)
        return await self._commit_and_refresh(doctor)

    async def delete(self, id: int) -> bool:
        doctor = await self.get_by_id(id)
        if not doctor:
            return False
        await self.session.delete(doctor)
        await self.session.commit()
        return True
