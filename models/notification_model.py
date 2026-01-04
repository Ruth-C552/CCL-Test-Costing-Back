from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime


# ---------- SQLAlchemy Model ----------
class NotificationDB(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.now, nullable=False)


# ---------- Pydantic Schemas ----------
class Notification(BaseModel):
    id: Optional[int] = None

    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Notification title",
    )

    date: Optional[datetime] = None

    class Config:
        orm_mode = True


class NotificationWithDetail(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Notification title",
    )
