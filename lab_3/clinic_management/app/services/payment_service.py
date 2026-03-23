from datetime import datetime, timezone
from decimal import Decimal

from app.core.exceptions import BusinessRuleException, EntityNotFoundException
from app.models.payment import Payment, PaymentStatus
from app.models.visit import VisitStatus
from app.repositories.diagnosis_repository import SQLAlchemyDiagnosisRepository
from app.repositories.doctor_repository import SQLAlchemyDoctorRepository
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.repositories.payment_repository import SQLAlchemyPaymentRepository
from app.repositories.prescription_repository import SQLAlchemyPrescriptionRepository
from app.repositories.visit_repository import SQLAlchemyVisitRepository
from app.schemas.payment import PaymentCreate


class PaymentService:
    def __init__(
        self,
        payment_repository: SQLAlchemyPaymentRepository,
        visit_repository: SQLAlchemyVisitRepository,
        doctor_repository: SQLAlchemyDoctorRepository,
        diagnosis_repository: SQLAlchemyDiagnosisRepository,
        prescription_repository: SQLAlchemyPrescriptionRepository,
        patient_repository: SQLAlchemyPatientRepository,
    ) -> None:
        self._payment_repo = payment_repository
        self._visit_repo = visit_repository
        self._doctor_repo = doctor_repository
        self._diagnosis_repo = diagnosis_repository
        self._prescription_repo = prescription_repository
        self._patient_repo = patient_repository

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Payment]:
        return await self._payment_repo.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Payment:
        payment = await self._payment_repo.get_by_id(id)
        if not payment:
            raise EntityNotFoundException("Payment", id)
        return payment

    async def get_by_patient(self, patient_id: int) -> list[Payment]:
        if not await self._patient_repo.get_by_id(patient_id):
            raise EntityNotFoundException("Patient", patient_id)
        return await self._payment_repo.get_by_patient_id(patient_id)

    async def create(self, data: PaymentCreate) -> Payment:
        # 1. Перевірити що visit_id існує
        visit = await self._visit_repo.get_by_id(data.visit_id)
        if not visit:
            raise EntityNotFoundException("Visit", data.visit_id)

        # 2. Перевірити що візит має статус COMPLETED
        if visit.status != VisitStatus.COMPLETED:
            raise BusinessRuleException(
                "Cannot create payment for a visit that is not completed"
            )

        # 3. Перевірити що для цього візиту ще немає платежу
        existing = await self._payment_repo.get_by_visit_id(data.visit_id)
        if existing:
            raise BusinessRuleException("Visit already has a payment")

        # 4. Отримати лікаря → взяти hourly_rate та duration_minutes
        doctor = await self._doctor_repo.get_by_id(visit.doctor_id)
        if not doctor:
            raise EntityNotFoundException("Doctor", visit.doctor_id)

        # 5. Розрахувати consultation_fee
        consultation_fee = doctor.hourly_rate * Decimal(
            str(visit.duration_minutes / 60)
        )

        # 6. Отримати діагноз → отримати всі призначення → скласти prescriptions_cost
        prescriptions_cost = Decimal("0")
        diagnosis = await self._diagnosis_repo.get_by_visit_id(data.visit_id)
        if diagnosis:
            prescriptions = await self._prescription_repo.get_by_diagnosis_id(
                diagnosis.id
            )
            prescriptions_cost = sum(
                (p.cost for p in prescriptions), Decimal("0")
            )

        # 7. amount = consultation_fee + prescriptions_cost
        amount = consultation_fee + prescriptions_cost

        # 8. Створити платіж зі статусом PENDING
        payment = Payment(
            visit_id=data.visit_id,
            patient_id=visit.patient_id,
            amount=amount,
            consultation_fee=consultation_fee,
            prescriptions_cost=prescriptions_cost,
            status=PaymentStatus.PENDING,
        )
        return await self._payment_repo.create(payment)

    async def pay(self, id: int) -> Payment:
        payment = await self.get_by_id(id)
        if payment.status != PaymentStatus.PENDING:
            raise BusinessRuleException(
                "Only pending payments can be marked as paid"
            )
        return await self._payment_repo.update(
            id, {"status": PaymentStatus.PAID, "paid_at": datetime.now(timezone.utc)}
        )

    async def cancel(self, id: int) -> Payment:
        payment = await self.get_by_id(id)
        if payment.status == PaymentStatus.PAID:
            raise BusinessRuleException("Cannot cancel a paid payment")
        return await self._payment_repo.update(
            id, {"status": PaymentStatus.CANCELLED}
        )
