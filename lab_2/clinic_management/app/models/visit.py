from datetime import datetime
from enum import Enum
from typing import Optional


class VisitStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Visit:
    def __init__(
        self,
        patient_id: int,
        doctor_id: int,
        scheduled_at: datetime,
        reason: str,
        duration_minutes: int = 30,
        status: VisitStatus = VisitStatus.SCHEDULED,
        notes: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.scheduled_at = scheduled_at
        self.duration_minutes = duration_minutes
        self.status = status
        self.reason = reason
        self.notes = notes
        self.created_at = created_at
