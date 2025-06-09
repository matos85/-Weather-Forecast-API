# app/crud.py

from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas

def get_or_create_activity(db: Session, name: str) -> models.Activity:
    activity = db.query(models.Activity).filter_by(name=name).first()
    if not activity:
        activity = models.Activity(name=name)
        db.add(activity)
        db.commit()
        db.refresh(activity)
    return activity

def create_record(db: Session, record: schemas.RecordCreate, user_id: int) -> models.Record:
    # Найти или создать активность
    activity = get_or_create_activity(db, record.activity_name)

    # Текущее время и день недели
    now = datetime.utcnow()
    weekday = now.isoweekday()

    # Создание записи с корректным полем timestamp
    db_record = models.Record(
        user_id=user_id,
        timestamp=now,
        weekday=weekday,
        activity_id=activity.id,
        duration_minutes=record.duration_minutes,
        intensity=record.intensity,
        calories=record.calories,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session, user_id: int) -> list[models.Record]:
    return db.query(models.Record).filter_by(user_id=user_id).all()

def get_record(db: Session, record_id: int, user_id: int) -> models.Record | None:
    return db.query(models.Record).filter_by(id=record_id, user_id=user_id).first()

def update_record(db: Session, record_id: int, user_id: int, data: schemas.RecordCreate) -> models.Record | None:
    record = get_record(db, record_id, user_id)
    if not record:
        return None

    # Найти или создать активность
    activity = get_or_create_activity(db, data.activity_name)

    # Обновление полей
    record.activity_id = activity.id
    record.duration_minutes = data.duration_minutes
    record.intensity = data.intensity
    record.calories = data.calories

    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, record_id: int, user_id: int) -> models.Record | None:
    record = get_record(db, record_id, user_id)
    if record:
        db.delete(record)
        db.commit()
        return record
    return None
