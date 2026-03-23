from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class DiagnosisSeverity(str, PyEnum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id: Mapped[int] = mapped_column(primary_key=True)
    visit_id: Mapped[int] = mapped_column(
        ForeignKey("visits.id", ondelete="RESTRICT"), unique=True, nullable=False
    )
    icd_code: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    severity: Mapped[DiagnosisSeverity] = mapped_column(
        SAEnum(DiagnosisSeverity, name="diagnosis_severity", create_constraint=True),
        nullable=False,
    )
    diagnosed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    visit: Mapped["Visit"] = relationship(back_populates="diagnosis")
    prescriptions: Mapped[list["Prescription"]] = relationship(
        back_populates="diagnosis", cascade="all, delete-orphan"
    )
