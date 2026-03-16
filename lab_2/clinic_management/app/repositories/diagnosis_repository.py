from datetime import datetime, timezone
from typing import Optional

from app.models.diagnosis import Diagnosis
from app.repositories.base import BaseRepository


class InMemoryDiagnosisRepository(BaseRepository[Diagnosis]):
    def __init__(self):
        self._storage: dict[int, Diagnosis] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Diagnosis]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[Diagnosis]:
        return self._storage.get(id)

    def get_by_visit_id(self, visit_id: int) -> Optional[Diagnosis]:
        for d in self._storage.values():
            if d.visit_id == visit_id:
                return d
        return None

    def create(self, entity: Diagnosis) -> Diagnosis:
        entity.id = self._next_id()
        entity.diagnosed_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[Diagnosis]:
        diagnosis = self._storage.get(id)
        if not diagnosis:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(diagnosis, key, value)
        return diagnosis

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
