from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Абстрактний базовий репозиторій.
    В ЛР №2 реалізується через in-memory словник.
    В ЛР №3 реалізується через SQLAlchemy Session — інтерфейс не змінюється.
    """

    @abstractmethod
    def get_all(self) -> list[T]:
        """Повернути всі записи."""
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Повернути запис за ID або None."""
        ...

    @abstractmethod
    def create(self, entity: T) -> T:
        """Зберегти новий запис і повернути його з присвоєним ID."""
        ...

    @abstractmethod
    def update(self, id: int, data: dict) -> Optional[T]:
        """Оновити поля запису за ID. Повернути оновлений запис або None."""
        ...

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Видалити запис за ID. Повернути True якщо видалено, False якщо не знайдено."""
        ...
