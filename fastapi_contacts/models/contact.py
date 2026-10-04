from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.user import User


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(255),nullable=False,index=True)
    phone: Mapped[str] = mapped_column(String(30),nullable=False)
    birthday: Mapped[date] = mapped_column(Date,nullable=False)
    additional_data: Mapped[str | None] = mapped_column(Text,nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True)
    owner: Mapped["User"] = relationship(back_populates="contacts")