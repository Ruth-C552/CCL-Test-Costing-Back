from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
#from helpers import assist
from models.instruments_model import Instruments, InstrumentsDB, InstrumentsWithDetail 
from models.user_model import UserDB 


router = APIRouter(prefix="/lab-instruments", tags=["Instruments"])

@router.post("/create", response_model=Instruments)
async def create_instruments(instruments: Instruments, db: AsyncSession = Depends(get_db)):
    #check instrument exists
    result = await db.execute(select(UserDB).where(UserDB.email == instruments.created_by))
    user = result.scalars().first()
    if not user:
      raise HTTPException(
          status_code=400, detail=f"The user with email '{instruments.created_by}' does not exist"
      )  
      
    db_instruments = InstrumentsDB(
       name=instruments.name,
       cost=instruments.cost,
       bench_id=instruments.bench_id,
       created_by=instruments.created_by,
    )
    
    db.add(db_instruments)
    try:
        await db.commit()
        await db.refresh(db_instruments)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create instrument: f{e}"
        )
    return db_instruments


@router.put("/update/{instruments_id}", response_model=Instruments)
async def update_instruments(instruments_id: int, instruments_update: Instruments, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InstrumentsDB).where(InstrumentsDB.id == instruments_id)
    )
    config = result.scalar_one_or_more()
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Unable to fimd Instrument with id '{instruments_id}'") 
    
    #update fields that are not None
    for key, value in instruments_update.dict(exclude_unset=True).items():
        setattr(config, key, value)
        
    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Unable to update instrument {e}")
    return config

@router.get("/list", response_model=List[Instruments])
async def list_instruments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InstrumentsDB))
    return result.scalars().all()
      