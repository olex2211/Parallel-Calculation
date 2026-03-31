from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PrescriptionCreate(BaseModel):
    diagnosis_id: int
    medication_name: str = Field(..., min_length=2, max_length=200)
    dosage: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)
    duration_days: int = Field(..., ge=1)
    cost: Decimal = Field(..., ge=0)
    notes: str | None = None


class PrescriptionUpdate(BaseModel):
    medication_name: str | None = Field(None, min_length=2, max_length=200)
    dosage: str | None = Field(None, min_length=1, max_length=100)
    frequency: str | None = Field(None, min_length=1, max_length=100)
    duration_days: int | None = Field(None, ge=1)
    cost: Decimal | None = Field(None, ge=0)
    notes: str | None = None


class PrescriptionResponse(BaseModel):
    id: int
    diagnosis_id: int
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int
    cost: Decimal
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
