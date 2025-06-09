# app/routers/records.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, crud
from app.database import get_db
from app.auth import get_current_user_id

router = APIRouter(prefix="/records", tags=["records"])


@router.post("/", response_model=schemas.RecordResponse)
def create_record(
    record_data: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    # Найти или создать тип активности
    activity = (
        db.query(models.Activity)
          .filter(models.Activity.name == record_data.activity_name)
          .first()
    )
    if not activity:
        activity = models.Activity(name=record_data.activity_name)
        db.add(activity)
        db.commit()
        db.refresh(activity)

    # Создать запись через CRUD
    db_record = crud.create_record(db, record_data, user_id)

    return schemas.RecordResponse(
        id=db_record.id,
        timestamp=db_record.timestamp,
        weekday=db_record.weekday,
        activity_name=activity.name,
        duration_minutes=db_record.duration_minutes,
        intensity=db_record.intensity,
        calories=db_record.calories,
    )


@router.get("/", response_model=list[schemas.RecordResponse])
def get_records(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    records = crud.get_records(db, user_id)
    return [
        schemas.RecordResponse(
            id=r.id,
            timestamp=r.timestamp,
            weekday=r.weekday,
            activity_name=r.activity.name,
            duration_minutes=r.duration_minutes,
            intensity=r.intensity,
            calories=r.calories,
        )
        for r in records
    ]


@router.get("/{record_id}", response_model=schemas.RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    r = crud.get_record(db, record_id, user_id)
    if not r:
        raise HTTPException(status_code=404, detail="Record not found")
    return schemas.RecordResponse(
        id=r.id,
        timestamp=r.timestamp,
        weekday=r.weekday,
        activity_name=r.activity.name,
        duration_minutes=r.duration_minutes,
        intensity=r.intensity,
        calories=r.calories,
    )


@router.put("/{record_id}", response_model=schemas.RecordResponse)
def update_record(
    record_id: int,
    record_data: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    updated = crud.update_record(db, record_id, user_id, record_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return schemas.RecordResponse(
        id=updated.id,
        timestamp=updated.timestamp,
        weekday=updated.weekday,
        activity_name=updated.activity.name,
        duration_minutes=updated.duration_minutes,
        intensity=updated.intensity,
        calories=updated.calories,
    )


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    deleted = crud.delete_record(db, record_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted"}
