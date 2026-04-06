from datetime import datetime
from enum import Enum as PyEnum
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SAEnum, Integer, String, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class VisitStatus(str, PyEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # New field: denormalized hourly rate from doctor at time of visit
    doctor_hourly_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    status: Mapped[VisitStatus] = mapped_column(
        SAEnum(VisitStatus, name="visit_status", create_constraint=True),
        default=VisitStatus.SCHEDULED,
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
