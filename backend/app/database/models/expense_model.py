import uuid
from datetime import datetime
from decimal import Decimal

from app.database.base import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    budget_cycle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("budget_cycles.id", ondelete="CASCADE"), index=True, nullable=False
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id"), index=True, nullable=False
    )

    description: Mapped[str] = mapped_column(String(150), nullable=False)

    value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    expense_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    observation: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    budget_cycle: Mapped["BudgetCycleModel"] = relationship(
        "BudgetCycleModel", back_populates="expenses", lazy="selectin"
    )

    category: Mapped["CategoryModel"] = relationship(
        "CategoryModel", back_populates="expenses", lazy="selectin"
    )
