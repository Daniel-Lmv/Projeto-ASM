from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )

    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    icon: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    color: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
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
    
    expenses: Mapped[list["ExpenseModel"]] = relationship(
        "ExpenseModel",
        back_populates="category"
    )

    user: Mapped["UserModel | None"] = relationship(
        "UserModel",
        back_populates="categories"
    )