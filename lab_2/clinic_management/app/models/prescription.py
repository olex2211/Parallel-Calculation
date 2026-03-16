from datetime import datetime
from decimal import Decimal
from typing import Optional


class Prescription:
    def __init__(
        self,
        diagnosis_id: int,
        medication_name: str,
        dosage: str,
        frequency: str,
        duration_days: int,
        cost: Decimal,
        notes: Optional[str] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.diagnosis_id = diagnosis_id
        self.medication_name = medication_name
        self.dosage = dosage
        self.frequency = frequency
        self.duration_days = duration_days
        self.cost = cost
        self.notes = notes
        self.created_at = created_at
