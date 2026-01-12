from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from database import Base
from datetime import datetime


# ---------- SQLAlchemy Models ----------
class CategoryDB(Base):
    __tablename__ = "categories"
    #id
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String, nullable=False)
    """    #bench
    bench_id = Column(Integer, ForeignKey("benches.id"), nullable=False)
   """    
    #service columns
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=True)
    created_by = Column(String, nullable=True, default="system")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    updated_by = Column(String, nullable=True)
    
 

    # relatinonships
    tests = relationship("TestsDB", back_populates="category", lazy="selectin")

# ---------- Pydantic Schemas ----------
class CategoryCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )
    
    """

    bench_id:  """
    
    created_by: Optional[str] 

    
class Category(BaseModel):
    #id
    id: Optional[int] = None 
    
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name must be between 2 and 50 characters",
    )

    """
  bench_id: int
        """

    #service columns
    created_at: Optional[datetime] = None
    created_by: Optional[str]
    updated_at: Optional[datetime] = None
    updated_by: Optional[str]
    

    class Config:
        orm_mode = True
        
class CategoryWithDetail(Category):
    pass