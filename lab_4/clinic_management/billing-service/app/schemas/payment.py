from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    visit_id: int


class PaymentResponse(BaseModel):
    id: int
    visit_id: int
    consultation_fee: Decimal
    prescriptions_cost: Decimal
    total_amount: Decimal
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
