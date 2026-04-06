from decimal import Decimal
from pydantic import BaseModel

class ExternalPatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

class ExternalDoctorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    hourly_rate: Decimal
