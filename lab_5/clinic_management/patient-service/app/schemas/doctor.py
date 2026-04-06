from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DoctorCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)
    hourly_rate: Decimal = Field(..., gt=0)
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr


class DoctorUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=2, max_length=100)
    last_name: str | None = Field(None, min_length=2, max_length=100)
    specialization: str | None = Field(None, min_length=2, max_length=100)
    hourly_rate: Decimal | None = Field(None, gt=0)
    phone: str | None = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr | None = None


class DoctorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: str
    hourly_rate: Decimal
    phone: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
