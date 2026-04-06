from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.diagnosis import DiagnosisResponse
from app.schemas.prescription import PrescriptionResponse
from app.schemas.external import ExternalVisitResponse


class VisitDetail(BaseModel):
    visit: ExternalVisitResponse
    diagnosis: DiagnosisResponse | None = None
    prescriptions: list[PrescriptionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TreatmentHistoryResponse(BaseModel):
    patient_id: int
    visits: list[VisitDetail]
    total_visits: int
    last_visit_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
