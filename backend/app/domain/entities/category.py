import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from backend.app.domain.enums.category_type import CategoryType


@dataclass
class Category:
    name: str
    type: CategoryType
    id: UUID = field(default_factory=lambda: uuid.uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    icon: str | None = None
    color: str | None = None

    def __post_init__(self):
        self._validate_name()

    def _validate_name(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("O nome da categoria não pode ser vazio!")
        if len(self.name) < 3:
            raise ValueError("O nome da categoria não pode ter menos que 3 letras")
        self.name = self.name.title()

    def rename(self, name: str) -> None:
        self.name = name
        self._validate_name()
        self._touch()

    def change_color(self, color: str) -> None:
        self.color = color
        self._touch()

    def change_icon(self, icon: str) -> None:
        self.icon = icon
        self._touch()

    def can_be_deleted(self) -> bool:
        return self.type != CategoryType.SYSTEM

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
