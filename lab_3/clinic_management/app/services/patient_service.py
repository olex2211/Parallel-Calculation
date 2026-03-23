from app.core.exceptions import EntityNotFoundException
from app.models.patient import Patient
from app.repositories.patient_repository import SQLAlchemyPatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, repository: SQLAlchemyPatientRepository) -> None:
        self._repository = repository

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Patient]:
        return await self._repository.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Patient:
        patient = await self._repository.get_by_id(id)
        if not patient:
            raise EntityNotFoundException("Patient", id)
        return patient

    async def create(self, data: PatientCreate) -> Patient:
        patient = Patient(
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            phone=data.phone,
            email=data.email,
        )
        return await self._repository.create(patient)

    async def update(self, id: int, data: PatientUpdate) -> Patient:
        patient = await self._repository.update(
            id, data.model_dump(exclude_unset=True)
        )
        if not patient:
            raise EntityNotFoundException("Patient", id)
        return patient

    async def delete(self, id: int) -> bool:
        if not await self._repository.delete(id):
            raise EntityNotFoundException("Patient", id)
        return True
