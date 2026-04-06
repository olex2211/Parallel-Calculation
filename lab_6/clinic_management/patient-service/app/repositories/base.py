from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.exc import IntegrityError, InternalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, ServiceUnavailableException

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository with AsyncSession."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _commit_and_refresh(self, entity: T) -> T:
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            detail = str(exc.orig) if exc.orig else str(exc)
            raise ConflictException(
                f"Database integrity error: {detail}"
            ) from exc
        except InternalError as exc:
            await self.session.rollback()
            raise ServiceUnavailableException(
                service_name="database", detail=str(exc)
            ) from exc
        await self.session.refresh(entity)
        return entity

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        ...

    @abstractmethod
    async def create(self, entity: T) -> T:
        ...

    @abstractmethod
    async def update(self, id: int, data: dict) -> T | None:
        ...

    @abstractmethod
    async def delete(self, id: int) -> bool:
        ...
