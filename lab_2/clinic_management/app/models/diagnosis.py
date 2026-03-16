from datetime import datetime
from enum import Enum
from typing import Optional


class DiagnosisSeverity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Diagnosis:
    def __init__(
        self,
        visit_id: int,
        icd_code: str,
        title: str,
        severity: DiagnosisSeverity,
        description: Optional[str] = None,
        id: Optional[int] = None,
        diagnosed_at: Optional[datetime] = None,
    ):
        self.id = id
        self.visit_id = visit_id
        self.icd_code = icd_code
        self.title = title
        self.description = description
        self.severity = severity
        self.diagnosed_at = diagnosed_at
