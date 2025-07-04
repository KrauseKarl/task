from enum import Enum as PyEnum

from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import BigInteger, String, Enum, DateTime, func, ForeignKey, Integer

from .db.base import Base


class BaseModel(Base):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=func.now())


class StatenEnum(PyEnum):
    OPERATE = "работает"
    OUT_OF_SERVICE = "не работает"
    UNSTABLE = "работает нестабильно"


class ServiceModel(BaseModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(450), nullable=True)
    current_state: Mapped[StatenEnum] = mapped_column(Enum(StatenEnum, name='state_service'))
    history: Mapped[List["HistoryModel"]] = relationship(
        argument="HistoryModel",
        backref=backref("services", lazy="selectin"),
        uselist=True,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class HistoryModel(BaseModel):
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id", ondelete="CASCADE")
    )
    service = relationship("Campaign", back_populates="structures")
    state = Mapped[StatenEnum] = mapped_column(Enum(StatenEnum, name='state_service'))