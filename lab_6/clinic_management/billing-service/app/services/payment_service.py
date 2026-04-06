from decimal import Decimal

from app.core.exceptions import (
    BusinessRuleException,
    ConflictException,
    EntityNotFoundException,
)
from app.models.payment import Payment, PaymentStatus
from app.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.schemas.payment import PaymentCreate
from app.services.appointment_client import AppointmentClient
from app.services.treatment_client import TreatmentClient


class PaymentService:
    def __init__(
        self,
        payment_repository: SQLAlchemyPaymentRepository,
        appointment_client: AppointmentClient,
        treatment_client: TreatmentClient,
    ) -> None:
        self._payment_repo = payment_repository
        self._appointment_client = appointment_client
        self._treatment_client = treatment_client

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Payment]:
        return await self._payment_repo.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Payment:
        payment = await self._payment_repo.get_by_id(id)
        if not payment:
            raise EntityNotFoundException("Payment", id)
        return payment

    async def create(self, data: PaymentCreate) -> Payment:
        # Cross-service fetching
        visit = await self._appointment_client.get_visit(data.visit_id)

        if visit.status != "completed":
            raise BusinessRuleException(
                f"Cannot create payment for a visit with status '{visit.status}'"
            )

        existing = await self._payment_repo.get_by_visit_id(data.visit_id)
        if existing:
            raise ConflictException("Payment already exists for this visit")

        prescriptions = await self._treatment_client.get_prescriptions_by_visit(
            data.visit_id
        )

        consultation_fee = visit.doctor_hourly_rate * (
            Decimal(visit.duration_minutes) / Decimal(60)
        )
        prescriptions_cost = sum(p.cost for p in prescriptions)
        total_amount = consultation_fee + prescriptions_cost

        payment = Payment(
            visit_id=data.visit_id,
            consultation_fee=consultation_fee,
            prescriptions_cost=prescriptions_cost,
            total_amount=total_amount,
            status=PaymentStatus.PENDING,
        )
        return await self._payment_repo.create(payment)

    async def complete_payment(self, id: int) -> Payment:
        payment = await self._payment_repo.get_by_id(id)
        if not payment:
            raise EntityNotFoundException("Payment", id)
        if payment.status != PaymentStatus.PENDING:
            raise BusinessRuleException("Can only complete pending payments")
        return await self._payment_repo.update(
            id, {"status": PaymentStatus.COMPLETED}
        )

    async def refund_payment(self, id: int) -> Payment:
        payment = await self._payment_repo.get_by_id(id)
        if not payment:
            raise EntityNotFoundException("Payment", id)
        if payment.status != PaymentStatus.COMPLETED:
            raise BusinessRuleException("Can only refund completed payments")
        return await self._payment_repo.update(
            id, {"status": PaymentStatus.REFUNDED}
        )
