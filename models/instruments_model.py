from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime

#-------------SQLAlchemy Models-------------
class InstrumentsDB(Base):
    __tablename__ = "instruments"
    #id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String, nullable=False)
    
    cost = Column(Float, nullable=False)
    
    #bench
    bench_id = Column(Integer, ForeignKey("benches.id"), nullable=False)
    
    #service columns
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    created_by = Column(String, nullable=True, default="system")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    updated_by = Column(String, nullable=True)
    
   # relationships
    benches = relationship("BenchDB", back_populates="instruments")


#------------Pydantic Schemas--------------
class Instruments(BaseModel):
    #id
    id: Optional[int] = None
    
    name: str = Field(
        ...,
        min_lenth=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    cost: float 
    
    #bench
    bench_id: int
    
    #service columns
    created_at: Optional[datetime] = None
    created_by: Optional[str]
    updated_at: Optional[datetime] = None
    updated_by: Optional[str]
    
    class Config:
        orm_mode = True

class InstrumentsWithDetail(Instruments):
    pass