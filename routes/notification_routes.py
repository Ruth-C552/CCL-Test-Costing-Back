from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models.notification_model import Notification, NotificationDB, NotificationWithDetail

router = APIRouter(prefix="/notification", tags=["Notification"])


@router.post("/create", response_model=Notification)
async def create_notification(
    notification: Notification,
    db: AsyncSession = Depends(get_db)
):
    db_notification = NotificationDB(
        title=notification.title
    )

    db.add(db_notification)
    try:
        await db.commit()
        await db.refresh(db_notification)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to create notification: {e}"
        )

    return db_notification


@router.put("/update/{notification_id}", response_model=Notification)
async def update_notification(
    notification_id: int,
    notification_update: Notification,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(NotificationDB).where(NotificationDB.id == notification_id)
    )
    config = result.scalars().first()

    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to find notification with id '{notification_id}'"
        )

    # update only provided fields
    for key, value in notification_update.dict(exclude_unset=True).items():
        setattr(config, key, value)

    try:
        await db.commit()
        await db.refresh(config)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Unable to update notification: {e}"
        )

    return config


@router.get("/list", response_model=List[Notification])
async def list_notifications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(NotificationDB).order_by(NotificationDB.date.desc())
    )
    return result.scalars().all()
