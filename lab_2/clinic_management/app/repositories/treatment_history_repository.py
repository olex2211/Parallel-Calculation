from datetime import datetime, timezone
from typing import Optional

from app.models.treatment_history import TreatmentHistory
from app.repositories.base import BaseRepository


class InMemoryTreatmentHistoryRepository(BaseRepository[TreatmentHistory]):
    def __init__(self):
        self._storage: dict[int, TreatmentHistory] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[TreatmentHistory]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[TreatmentHistory]:
        return self._storage.get(id)

    def get_by_patient_id(self, patient_id: int) -> Optional[TreatmentHistory]:
        for th in self._storage.values():
            if th.patient_id == patient_id:
                return th
        return None

    def create(self, entity: TreatmentHistory) -> TreatmentHistory:
        entity.id = self._next_id()
        entity.created_at = datetime.now(timezone.utc)
        entity.updated_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[TreatmentHistory]:
        history = self._storage.get(id)
        if not history:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(history, key, value)
        history.updated_at = datetime.now(timezone.utc)
        return history

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
