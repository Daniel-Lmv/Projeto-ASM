import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from backend.app.domain.entities.expenses import Expense
from backend.app.domain.entities.income import Income


@dataclass
class BudgetCycle:
    reference_date: date
    user_id: UUID
    is_closed: bool
    incomes: list[Income] = field(default_factory=list)
    expenses: list[Expense] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: UUID = field(default_factory=lambda: uuid.uuid4())

    def __post_init__(self):
        self._validate_user_id()
        self._validate_reference_date()

    def _validate_user_id(self) -> None:
        if self.user_id is None:
            raise ValueError("ID do usuário inválido")

    def _validate_reference_date(self) -> None:
        if self.reference_date is None:
            raise ValueError("Data inválida")
        if type(self.reference_date) is not date:
            raise ValueError("Tipo de data inválido")

    def add_income(self, nv_income: Income) -> None:
        if not self.is_closed:
            self.incomes.append(nv_income)
            self._touch()

    def remove_income(self, rm_income: Income) -> None:
        if not self.is_closed:
            self.incomes.remove(rm_income)
            self._touch()

    def add_expense(self, nv_expense: Expense) -> None:
        if not self.is_closed:
            self.expenses.append(nv_expense)
            self._touch()

    def remove_expense(self, rm_expense: Expense) -> None:
        if not self.is_closed:
            self.expenses.remove(rm_expense)
            self._touch()

    def close_cycle(self) -> None:
        self.is_closed = True
        self._touch()

    def reopen_cycle(self) -> None:
        self.is_closed = False
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    def can_edit(self) -> bool:
        return not self.is_closed
