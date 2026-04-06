from pydantic import BaseModel
from decimal import Decimal

class ExternalVisitResponse(BaseModel):
    id: int
    status: str
    duration_minutes: int
    doctor_hourly_rate: Decimal

class ExternalPrescriptionResponse(BaseModel):
    id: int
    cost: Decimal
