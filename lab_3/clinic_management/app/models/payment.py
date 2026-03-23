from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    visit_id: Mapped[int] = mapped_column(
        ForeignKey("visits.id", ondelete="RESTRICT"), unique=True, nullable=False
    )
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="RESTRICT"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    consultation_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    prescriptions_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        SAEnum(PaymentStatus, name="payment_status", create_constraint=True),
        default=PaymentStatus.PENDING,
        nullable=False,
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    visit: Mapped["Visit"] = relationship(back_populates="payment")
    patient: Mapped["Patient"] = relationship(back_populates="payments")
