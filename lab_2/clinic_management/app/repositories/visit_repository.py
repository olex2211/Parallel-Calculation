from datetime import datetime, timedelta, timezone
from typing import Optional

from app.models.visit import Visit, VisitStatus
from app.repositories.base import BaseRepository


class InMemoryVisitRepository(BaseRepository[Visit]):
    def __init__(self):
        self._storage: dict[int, Visit] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        self._counter += 1
        return self._counter

    def get_all(self) -> list[Visit]:
        return list(self._storage.values())

    def get_by_id(self, id: int) -> Optional[Visit]:
        return self._storage.get(id)

    def get_by_patient_id(self, patient_id: int) -> list[Visit]:
        return [v for v in self._storage.values() if v.patient_id == patient_id]

    def get_by_doctor_id(self, doctor_id: int) -> list[Visit]:
        return [v for v in self._storage.values() if v.doctor_id == doctor_id]

    def get_by_status(self, status: VisitStatus) -> list[Visit]:
        return [v for v in self._storage.values() if v.status == status]

    def get_conflicting(
        self, doctor_id: int, scheduled_at: datetime, duration_minutes: int
    ) -> Optional[Visit]:
        """Перевірити наявність конфлікту часу у лікаря."""
        new_start = scheduled_at
        new_end = scheduled_at + timedelta(minutes=duration_minutes)

        for visit in self._storage.values():
            if visit.doctor_id != doctor_id:
                continue
            if visit.status == VisitStatus.CANCELLED:
                continue

            existing_start = visit.scheduled_at
            existing_end = visit.scheduled_at + timedelta(minutes=visit.duration_minutes)

            if new_start < existing_end and new_end > existing_start:
                return visit

        return None

    def create(self, entity: Visit) -> Visit:
        entity.id = self._next_id()
        entity.created_at = datetime.now(timezone.utc)
        self._storage[entity.id] = entity
        return entity

    def update(self, id: int, data: dict) -> Optional[Visit]:
        visit = self._storage.get(id)
        if not visit:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(visit, key, value)
        return visit

    def delete(self, id: int) -> bool:
        if id not in self._storage:
            return False
        del self._storage[id]
        return True
