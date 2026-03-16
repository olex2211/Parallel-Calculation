from app.core.exceptions import EntityNotFoundException
from app.models.doctor import Doctor
from app.repositories.doctor_repository import InMemoryDoctorRepository
from app.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:
    def __init__(self, repository: InMemoryDoctorRepository):
        self._repository = repository

    def get_all(self) -> list[Doctor]:
        return self._repository.get_all()

    def get_by_id(self, id: int) -> Doctor:
        doctor = self._repository.get_by_id(id)
        if not doctor:
            raise EntityNotFoundException("Doctor", id)
        return doctor

    def get_by_specialization(self, specialization: str) -> list[Doctor]:
        return self._repository.get_by_specialization(specialization)

    def create(self, data: DoctorCreate) -> Doctor:
        doctor = Doctor(
            first_name=data.first_name,
            last_name=data.last_name,
            specialization=data.specialization,
            hourly_rate=data.hourly_rate,
            phone=data.phone,
            email=data.email,
        )
        return self._repository.create(doctor)

    def update(self, id: int, data: DoctorUpdate) -> Doctor:
        doctor = self._repository.update(
            id, data.model_dump(exclude_unset=True)
        )
        if not doctor:
            raise EntityNotFoundException("Doctor", id)
        return doctor

    def delete(self, id: int) -> bool:
        if not self._repository.delete(id):
            raise EntityNotFoundException("Doctor", id)
        return True
