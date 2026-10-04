from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.contact import Contact

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,nullable=False)
    contacts: Mapped[list["Contact"]] = relationship(back_populates="owner",cascade="all, delete-orphan")