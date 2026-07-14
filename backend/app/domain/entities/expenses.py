import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from backend.app.domain.entities.category import Category


@dataclass
class Expense:
    description: str
    value: Decimal
    category: Category
    expense_date: datetime
    is_recurring: bool
    observation: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=lambda: uuid.uuid4())

    def __post_init__(self):
        self._validate_category()
        self._validate_description()
        self._validate_value()

    def rename_description(self, descripition: str) -> None:
        self.description = descripition
        self._validate_description()
        self._touch()

    def change_value(self, value: Decimal) -> None:
        self.value = value
        self._validate_value()
        self._touch()

    def change_category(self, category: Category) -> None:
        self.category = category
        self._validate_category()
        self._touch()

    def change_observation(self, obs: str) -> None:
        self.observation = obs
        self._validate_observation()
        self._touch()

    def change_expense_date(self, time: datetime) -> None:
        self.expense_date = time
        self._touch()

    def change_recurring(self) -> None:
        self.is_recurring = not self.is_recurring
        self._touch()

    def _validate_value(self) -> None:
        if self.value <= 0:
            raise ValueError("O valor da despesa deve ser maior que 0")

    def _validate_description(self) -> None:
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("A descrição não pode ser vazia!")
        if len(self.description) < 3:
            raise ValueError("A descrição não pode ter menos que 3 letras")
        self.description = self.description.title()

    def _validate_category(self) -> None:
        if self.category is None:
            raise ValueError("A despesa deve ter uma categoria valida!")

    def _validate_observation(self) -> None:
        if self.observation is not None:
            self.observation = self.observation.strip()
            if not self.observation:
                raise ValueError("A observação não pode ser vazia!")
            if len(self.observation) < 3:
                raise ValueError("A observação não pode ter menos que 3 letras")
            self.observation = self.observation.title()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
