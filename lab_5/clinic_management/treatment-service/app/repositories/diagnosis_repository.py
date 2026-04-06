from sqlalchemy import select

from app.models.diagnosis import Diagnosis
from app.repositories.base import BaseRepository


class SQLAlchemyDiagnosisRepository(BaseRepository[Diagnosis]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Diagnosis]:
        result = await self.session.execute(
            select(Diagnosis).order_by(Diagnosis.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Diagnosis | None:
        result = await self.session.execute(
            select(Diagnosis).where(Diagnosis.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_visit_id(self, visit_id: int) -> Diagnosis | None:
        result = await self.session.execute(
            select(Diagnosis).where(Diagnosis.visit_id == visit_id)
        )
        return result.scalar_one_or_none()

    async def create(self, entity: Diagnosis) -> Diagnosis:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Diagnosis | None:
        diagnosis = await self.get_by_id(id)
        if not diagnosis:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(diagnosis, key, value)
        return await self._commit_and_refresh(diagnosis)

    async def delete(self, id: int) -> bool:
        diagnosis = await self.get_by_id(id)
        if not diagnosis:
            return False
        await self.session.delete(diagnosis)
        await self.session.commit()
        return True
