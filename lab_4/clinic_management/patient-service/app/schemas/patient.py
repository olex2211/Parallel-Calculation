from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PatientCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr


class PatientUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=2, max_length=100)
    last_name: str | None = Field(None, min_length=2, max_length=100)
    phone: str | None = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    email: EmailStr | None = None


class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
