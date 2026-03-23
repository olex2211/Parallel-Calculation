from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    visit_id: int


class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    visit_id: int
    patient_id: int
    amount: Decimal
    consultation_fee: Decimal
    prescriptions_cost: Decimal
    status: PaymentStatus
    paid_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
