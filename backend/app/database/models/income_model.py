from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base

class IncomeModel(Base):
    __tablename__ = "incomes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    budget_cycle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("budget_cycles.id"),
        index=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
       String(150),
       nullable=False
    )

    value: Mapped[Decimal] = mapped_column(
        Numeric(12,2),
        nullable=False
     )

    income_type: Mapped[str] = mapped_column(
       String(20),
       nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    budget_cycle: Mapped["BudgetCycleModel"] = relationship(
        "BudgetCycleModel",
        back_populates="incomes"
    )






