from datetime import datetime
from pydantic import BaseModel

class ExternalVisitResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    status: str
    scheduled_at: datetime
