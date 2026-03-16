from datetime import datetime
from typing import Optional

from app.models.visit import Visit


class TreatmentHistory:
    def __init__(
        self,
        patient_id: int,
        visits: Optional[list[Visit]] = None,
        total_visits: int = 0,
        last_visit_at: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.patient_id = patient_id
        self.visits = visits or []
        self.total_visits = total_visits
        self.last_visit_at = last_visit_at
        self.created_at = created_at
        self.updated_at = updated_at
