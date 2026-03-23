from sqlalchemy import select

from app.models.payment import Payment
from app.repositories.base import BaseRepository


class SQLAlchemyPaymentRepository(BaseRepository[Payment]):
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).order_by(Payment.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_visit_id(self, visit_id: int) -> Payment | None:
        result = await self.session.execute(
            select(Payment).where(Payment.visit_id == visit_id)
        )
        return result.scalar_one_or_none()

    async def get_by_patient_id(self, patient_id: int) -> list[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.patient_id == patient_id)
        )
        return list(result.scalars().all())

    async def create(self, entity: Payment) -> Payment:
        self.session.add(entity)
        return await self._commit_and_refresh(entity)

    async def update(self, id: int, data: dict) -> Payment | None:
        payment = await self.get_by_id(id)
        if not payment:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(payment, key, value)
        return await self._commit_and_refresh(payment)

    async def delete(self, id: int) -> bool:
        payment = await self.get_by_id(id)
        if not payment:
            return False
        await self.session.delete(payment)
        await self.session.commit()
        return True
