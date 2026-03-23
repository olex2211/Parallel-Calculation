from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class VisitStatus(str, PyEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="RESTRICT"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"), nullable=False
    )
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

    # Relationships
    patient: Mapped["Patient"] = relationship(back_populates="visits")
    doctor: Mapped["Doctor"] = relationship(back_populates="visits")
    diagnosis: Mapped["Diagnosis | None"] = relationship(
        back_populates="visit", uselist=False
    )
    payment: Mapped["Payment | None"] = relationship(
        back_populates="visit", uselist=False
    )
