from datetime import datetime, timezone
from typing import Optional

from app.models.doctor import Doctor
from app.repositories.base import BaseRepository


class InMemoryDoctorRepository(BaseRepository[Doctor]):
    def __init__(self):
        self._storage: dict[int, Doctor] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Doctor]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[Doctor]:
        return self._storage.get(id)

    def get_by_specialization(self, specialization: str) -> list[Doctor]:
        return [
            d for d in self._storage.values()
            if d.specialization.lower() == specialization.lower()
        ]

    def create(self, entity: Doctor) -> Doctor:
        entity.id = self._next_id()
        entity.created_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[Doctor]:
        doctor = self._storage.get(id)
        if not doctor:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(doctor, key, value)
        return doctor

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
