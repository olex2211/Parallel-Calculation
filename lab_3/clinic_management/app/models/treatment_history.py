from datetime import datetime
from typing import Optional

from app.schemas.visit import VisitResponse


class TreatmentHistory:
    """Агрегат — не має таблиці в БД, збирається динамічно сервісом."""

    def __init__(
        self,
        patient_id: int,
        visits: Optional[list[VisitResponse]] = None,
        total_visits: int = 0,
        last_visit_at: Optional[datetime] = None,
    ):
        self.patient_id = patient_id
        self.visits = visits or []
        self.total_visits = total_visits
        self.last_visit_at = last_visit_at
