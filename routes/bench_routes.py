from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models.bench_model import Bench, BenchDB, BenchWithDetail
from models.user_model import UserDB

router = APIRouter(prefix="/lab-benches", tags=["Benchs"])


@router.post("/create", response_model=Bench)
async def create_type(bench: Bench, db: AsyncSession = Depends(get_db)):
    # check user exists
    result = await db.execute(select(UserDB).where(UserDB.id == bench.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"The user with id '{bench.user_id}' does not exist"
        )
        
    db_user = BenchDB(
        # user
        user_id=bench.user_id,
        # details
        name=bench.name,
        description=bench.description,
        # service
        created_by=user.email,
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create bench: f{e}"
        )
    return db_user

@router.get("/id/{bench_id}", response_model=Bench)
async def get_knowledgebase_category(bench_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BenchDB)
        .filter(BenchDB.id == bench_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Unable to find bench with id '{bench_id}'")
    return category


@router.put("/update/{bench_id}", response_model=Bench)
async def update_category(bench_id: int, bench_update: Bench, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(BenchDB)
        .where(BenchDB.id == bench_id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Unable to find bench with id '{bench_id}'")
    
    # Update fields that are not None
    for key, value in bench_update.dict(exclude_unset=True).items():
        setattr(config, key, value)
        
    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Unable to update bench {e}")
    return config

@router.get("/list", response_model=List[Bench])
async def list_benches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BenchDB))
    return result.scalars().all()
