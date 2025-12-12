from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime


# ---------- SQLAlchemy Models ----------
class TestsDB(Base):
    __tablename__ = "tests"
    #id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String, nullable=False)
    
    #bench
    bench_id = Column(Integer, ForeignKey("benches.id"), nullable=False)
    
    #service columns
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=True)
    created_by = Column(String, nullable=True, default="system")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    updated_by = Column(String, nullable=True)
    
    # relatinonships
    benches = relationship("BenchDB", back_populates="tests")

# ---------- Pydantic Schemas ----------
class Tests(BaseModel):
    #id
    id: Optional[int] = None 
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    #bench
    bench_id: int
    
    #service columns
    created_at: Optional[datetime] = None
    created_by: Optional[str]
    updated_at: Optional[datetime] = None
    updated_by: Optional[str]
    
    class Config:
        orm_mode = True
        
class TestsWithDetail(Tests):
    pass