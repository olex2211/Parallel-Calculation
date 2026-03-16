from datetime import datetime, timezone
from typing import Optional

from app.models.payment import Payment
from app.repositories.base import BaseRepository


class InMemoryPaymentRepository(BaseRepository[Payment]):
    def __init__(self):
        self._storage: dict[int, Payment] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Payment]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[Payment]:
        return self._storage.get(id)

    def get_by_visit_id(self, visit_id: int) -> Optional[Payment]:
        for p in self._storage.values():
            if p.visit_id == visit_id:
                return p
        return None

    def get_by_patient_id(self, patient_id: int) -> list[Payment]:
        return [
            p for p in self._storage.values()
            if p.patient_id == patient_id
        ]

    def create(self, entity: Payment) -> Payment:
        entity.id = self._next_id()
        entity.created_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[Payment]:
        payment = self._storage.get(id)
        if not payment:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(payment, key, value)
        return payment

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
