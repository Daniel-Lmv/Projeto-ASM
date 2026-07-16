import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID


from backend.app.domain.enums.income_type import IncomeType


@dataclass
class Income:
    type: IncomeType
    description: str
    value: Decimal
    id: UUID = field(default_factory=lambda: uuid.uuid4())
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        self._validate_description()
        self._validate_value()

    def _validate_value(self) -> None:
        if self.value <= 0:
            raise ValueError("A renda deve ser maior que 0")

    def _validate_description(self) -> None:
        self.description = self.description.strip()
        if not self.description:
            raise ValueError("A descrição não pode ser vazia!")
        if len(self.description) < 3:
            raise ValueError("A descrição não pode ter menos que 3 letras")
        self.description = self.description.title()

    def rename_description(self, desc: str) -> None:
        self.description = desc
        self._validate_description()
        self._touch()

    def change_income_value(self, val: Decimal) -> None:
        self.value = val
        self._validate_value()
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    def return_type(self) -> IncomeType:
        return self.type
