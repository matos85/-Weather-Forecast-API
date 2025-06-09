from sqlalchemy.orm import Session
from db_models import User
from typing import Optional


def get_users_with_filters(
        db: Session,
        city: Optional[str] = None,
        first_name: Optional[str] = None,
        patronymic: Optional[str] = None,
        phone: Optional[str] = None,
        telegram: Optional[str] = None,
        has_photo: Optional[bool] = None
):
    query = db.query(User).filter(User.is_deleted == False)

    if city:
        query = query.filter(User.city == city)
    if first_name:
        query = query.filter(User.first_name == first_name)
    if patronymic:
        query = query.filter(User.patronymic == patronymic)
    if phone:
        query = query.filter(User.phone == phone)
    if telegram:
        query = query.filter(User.telegram == telegram)
    if has_photo is not None:
        if has_photo:
            query = query.filter(User.photo_path != None)
        else:
            query = query.filter(User.photo_path == None)

    return query.all()