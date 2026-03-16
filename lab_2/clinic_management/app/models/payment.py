from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Payment:
    def __init__(
        self,
        visit_id: int,
        patient_id: int,
        amount: Decimal,
        consultation_fee: Decimal,
        prescriptions_cost: Decimal,
        status: PaymentStatus = PaymentStatus.PENDING,
        paid_at: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.visit_id = visit_id
        self.patient_id = patient_id
        self.amount = amount
        self.consultation_fee = consultation_fee
        self.prescriptions_cost = prescriptions_cost
        self.status = status
        self.paid_at = paid_at
        self.created_at = created_at
