from datetime import datetime, timezone
from typing import Optional

from app.models.prescription import Prescription
from app.repositories.base import BaseRepository


class InMemoryPrescriptionRepository(BaseRepository[Prescription]):
    def __init__(self):
        self._storage: dict[int, Prescription] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Prescription]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[Prescription]:
        return self._storage.get(id)

    def get_by_diagnosis_id(self, diagnosis_id: int) -> list[Prescription]:
        return [
            p for p in self._storage.values()
            if p.diagnosis_id == diagnosis_id
        ]

    def create(self, entity: Prescription) -> Prescription:
        entity.id = self._next_id()
        entity.created_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[Prescription]:
        prescription = self._storage.get(id)
        if not prescription:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(prescription, key, value)
        return prescription

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
