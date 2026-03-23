from app.core.exceptions import EntityNotFoundException
from app.models.doctor import Doctor
from app.repositories.doctor_repository import SQLAlchemyDoctorRepository
from app.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:
    def __init__(self, repository: SQLAlchemyDoctorRepository) -> None:
        self._repository = repository

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Doctor]:
        return await self._repository.get_all(skip, limit)

    async def get_by_id(self, id: int) -> Doctor:
        doctor = await self._repository.get_by_id(id)
        if not doctor:
            raise EntityNotFoundException("Doctor", id)
        return doctor

    async def get_by_specialization(self, specialization: str) -> list[Doctor]:
        return await self._repository.get_by_specialization(specialization)

    async def create(self, data: DoctorCreate) -> Doctor:
        doctor = Doctor(
            first_name=data.first_name,
            last_name=data.last_name,
            specialization=data.specialization,
            hourly_rate=data.hourly_rate,
            phone=data.phone,
            email=data.email,
        )
        return await self._repository.create(doctor)

    async def update(self, id: int, data: DoctorUpdate) -> Doctor:
        doctor = await self._repository.update(
            id, data.model_dump(exclude_unset=True)
        )
        if not doctor:
            raise EntityNotFoundException("Doctor", id)
        return doctor

    async def delete(self, id: int) -> bool:
        if not await self._repository.delete(id):
            raise EntityNotFoundException("Doctor", id)
        return True
