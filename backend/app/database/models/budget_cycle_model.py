import uuid
from datetime import date, datetime

from app.database.base import Base
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BudgetCycleModel(Base):
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "reference_date",
            name="uq_user_reference_date",
        ),
    )

    __tablename__ = "budget_cycles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    reference_date: Mapped[date] = mapped_column(Date, nullable=False)

    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="budget_cycles", lazy="selectin"
    )

    incomes: Mapped[list["IncomeModel"]] = relationship(
        "IncomeModel",
        back_populates="budget_cycle",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    expenses: Mapped[list["ExpenseModel"]] = relationship(
        "ExpenseModel",
        back_populates="budget_cycle",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
