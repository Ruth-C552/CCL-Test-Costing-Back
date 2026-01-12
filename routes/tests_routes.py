from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from helpers import assist
from models.tests_model import Tests, TestsCreate, TestsDB,  TestsWithDetail
from models.user_model import UserDB 
from models.notification_model import NotificationDB
from datetime import datetime
 
router = APIRouter(prefix="/lab-tests", tags=["Tests"])


@router.post("/create", response_model=Tests)
async def create_type(tests: TestsCreate, db: AsyncSession = Depends(get_db)):
    
    created_by_email = tests.created_by if tests.created_by else "system"
    #check user exists
    result = await db.execute(select(UserDB).where(UserDB.email == tests.created_by))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"The user with email '{tests.created_by}' does not exist"
        )
    
    db_tests = TestsDB(
        name=tests.name,
        bench_id=tests.bench_id,
        category_id=tests.category_id,
        created_by=created_by_email,        
    )
    
    db.add(db_tests)
    
    try:
        #commit test first to get ID
        await db.commit()
        await db.refresh(db_tests)        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create test: f{e}"
        )

    #create notification
    try:
        today = datetime.now().strftime("%Y-%m-%D")
        notification_title = f"{db_tests.name} test created on {today} by {created_by_email}"
        notification = NotificationDB(
            title=notification_title,
            date=datetime.now()
        )                   
        db.add(notification)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create notification: f{e}"
        )
        
    return db_tests


@router.put("/update/{test_id}", response_model=Tests)
async def update_tests(test_id: int, test_update: Tests, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TestsDB).where(TestsDB.id == test_id)
    )
    config = result.scalar_one_or_more()
    
    if not config:
        raise HTTPException(status_code=404, detail=f"Unable to find test with id '{test_id}'")
    
    #update fields that are not None
    for key, value in test_update.dict(exclude_unset=True).items():
        setattr(config, key, value)
        
    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Unable to update test {e}")
    return config

@router.get("/list", response_model=List[Tests])
async def list_tests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestsDB))
    return result.scalars().all()