from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Абстрактний базовий репозиторій з AsyncSession."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _commit_and_refresh(self, entity: T) -> T:
        """Commit та refresh з обробкою IntegrityError (unique constraint тощо)."""
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            detail = str(exc.orig) if exc.orig else str(exc)
            raise ConflictException(
                f"Database integrity error: {detail}"
            ) from exc
        await self.session.refresh(entity)
        return entity

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Повернути записи з пагінацією."""
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        """Повернути запис за ID або None."""
        ...

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Зберегти новий запис і повернути його з присвоєним ID."""
        ...

    @abstractmethod
    async def update(self, id: int, data: dict) -> T | None:
        """Оновити поля запису за ID. Повернути оновлений запис або None."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Видалити запис за ID. Повернути True якщо видалено, False якщо не знайдено."""
        ...

