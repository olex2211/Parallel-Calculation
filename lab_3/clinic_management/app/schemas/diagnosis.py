from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.diagnosis import DiagnosisSeverity


class DiagnosisCreate(BaseModel):
    visit_id: int
    icd_code: str = Field(..., min_length=3, max_length=10)
    title: str = Field(..., min_length=2, max_length=200)
    description: str | None = None
    severity: DiagnosisSeverity


class DiagnosisUpdate(BaseModel):
    icd_code: str | None = Field(None, min_length=3, max_length=10)
    title: str | None = Field(None, min_length=2, max_length=200)
    description: str | None = None
    severity: DiagnosisSeverity | None = None


class DiagnosisResponse(BaseModel):
    id: int
    visit_id: int
    icd_code: str
    title: str
    description: str | None
    severity: DiagnosisSeverity
    diagnosed_at: datetime

    model_config = ConfigDict(from_attributes=True)
