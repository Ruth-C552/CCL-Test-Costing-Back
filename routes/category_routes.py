from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from helpers import assist
from models.category_model import Category, CategoryCreate, CategoryDB,  CategoryWithDetail
from models.user_model import UserDB 
from datetime import datetime
 
router = APIRouter(prefix="/transaction-categories", tags=["Category"])


@router.post("/create", response_model=Category)
async def create_type(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    
    created_by_email = category.created_by if category.created_by else "system"
    #check user exists
    result = await db.execute(select(UserDB).where(UserDB.email == category.created_by))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"The user with email '{category.created_by}' does not exist"
        )
    
    db_category = CategoryDB(
        name=category.name,
    )

    db.add(db_category)
    
    try:
        #commit test first to get ID
        await db.commit()
        await db.refresh(db_category)        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create category: f{e}"
        )

    return db_category


@router.put("/update/{category_id}", response_model=Category)
async def update_category(category_id: int, category_update: Category, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CategoryDB).where(CategoryDB.id == category_id)
    )
    config = result.scalars().first()

    
    if not config:
        raise HTTPException(status_code=404, detail=f"Unable to find category with id '{category_id}'")
    
    #update fields that are not None
    for key, value in category_update.dict(exclude_unset=True).items():
        setattr(config, key, value)
        
    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Unable to update category {e}")
    return config

@router.get("/list", response_model=List[Category])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryDB))
    return result.scalars().all()