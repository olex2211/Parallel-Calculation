from app.core.exceptions import EntityNotFoundException
from app.models.prescription import Prescription
from app.repositories.diagnosis_repository import InMemoryDiagnosisRepository
from app.repositories.prescription_repository import InMemoryPrescriptionRepository
from app.schemas.prescription import PrescriptionCreate


class PrescriptionService:
    def __init__(
        self,
        prescription_repository: InMemoryPrescriptionRepository,
        diagnosis_repository: InMemoryDiagnosisRepository,
    ):
        self._prescription_repo = prescription_repository
        self._diagnosis_repo = diagnosis_repository

    def get_all(self) -> list[Prescription]:
        return self._prescription_repo.get_all()

    def get_by_id(self, id: int) -> Prescription:
        prescription = self._prescription_repo.get_by_id(id)
        if not prescription:
            raise EntityNotFoundException("Prescription", id)
        return prescription

    def get_by_diagnosis(self, diagnosis_id: int) -> list[Prescription]:
        return self._prescription_repo.get_by_diagnosis_id(diagnosis_id)

    def create(self, data: PrescriptionCreate) -> Prescription:
        # 1. Перевірити що diagnosis_id існує
        if not self._diagnosis_repo.get_by_id(data.diagnosis_id):
            raise EntityNotFoundException("Diagnosis", data.diagnosis_id)

        # 2. Створити призначення
        prescription = Prescription(
            diagnosis_id=data.diagnosis_id,
            medication_name=data.medication_name,
            dosage=data.dosage,
            frequency=data.frequency,
            duration_days=data.duration_days,
            cost=data.cost,
            notes=data.notes,
        )
        return self._prescription_repo.create(prescription)

    def delete(self, id: int) -> bool:
        if not self._prescription_repo.delete(id):
            raise EntityNotFoundException("Prescription", id)
        return True
