from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.visit import VisitStatus


class VisitCreate(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime = Field(..., description="Must be in the future")
    duration_minutes: int = Field(default=30, ge=15, le=120)
    reason: str = Field(..., min_length=5, max_length=500)


class VisitUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: VisitStatus | None = None
    notes: str | None = None
    duration_minutes: int | None = Field(None, ge=15, le=120)


class VisitResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    duration_minutes: int
    status: VisitStatus
    reason: str
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
