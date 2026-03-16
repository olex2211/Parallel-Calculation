from app.core.exceptions import EntityNotFoundException
from app.models.patient import Patient
from app.repositories.patient_repository import InMemoryPatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, repository: InMemoryPatientRepository):
        self._repository = repository

    def get_all(self) -> list[Patient]:
        return self._repository.get_all()

    def get_by_id(self, id: int) -> Patient:
        patient = self._repository.get_by_id(id)
        if not patient:
            raise EntityNotFoundException("Patient", id)
        return patient

    def create(self, data: PatientCreate) -> Patient:
        patient = Patient(
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            phone=data.phone,
            email=data.email,
        )
        return self._repository.create(patient)

    def update(self, id: int, data: PatientUpdate) -> Patient:
        patient = self._repository.update(
            id, data.model_dump(exclude_unset=True)
        )
        if not patient:
            raise EntityNotFoundException("Patient", id)
        return patient

    def delete(self, id: int) -> bool:
        if not self._repository.delete(id):
            raise EntityNotFoundException("Patient", id)
        return True
