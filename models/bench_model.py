from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime

from models.user_model import User
from models.tests_model import Tests
from models.instruments_model import Instruments


# ---------- SQLAlchemy Models ----------
class BenchDB(Base):
    __tablename__ = "benches"

    # id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # service columns
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=True)
    created_by = Column(String, nullable=True, default="System")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    updated_by = Column(String, nullable=True)

    # relationships
    user = relationship("UserDB", back_populates="benches", lazy="selectin")
    tests = relationship("TestsDB", back_populates="benches", lazy="selectin")
    instruments = relationship("InstrumentsDB", back_populates="benches", lazy="selectin")

    
# ---------- Pydantic Schemas ----------
class BenchCreate(BaseModel):
    # user
    user_id: int

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    description: Optional[str] = None

class Bench(BaseModel):
    # id
    id: Optional[int] = None
    # user
    user_id: int

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    description: Optional[str] = None
    # service columns
    created_at: Optional[datetime] = None
    created_by: Optional[str]
    updated_at: Optional[datetime] = None
    updated_by: Optional[str]

    class Config:
        orm_mode = True

class BenchWithDetail(Bench):
    user: User
    tests: Tests
    instruments: Instruments