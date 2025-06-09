from sqlalchemy.orm import Session
from db_models import User
from schemas import UserCreate
from utils import hash_password, save_photo, verify_password
from fastapi import HTTPException, UploadFile

def create_user(db: Session, user: UserCreate, photo: UploadFile = None):
    hashed_password = hash_password(user.password)
    db_user = User(
        login=user.login,
        password=hashed_password,
        email=user.email,
        city=user.city,
        first_name=user.first_name,
        patronymic=user.patronymic,
        phone=user.phone,
        telegram=user.telegram
        # registration_date не указываем, оно устанавливается автоматически в модели
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Обновляем объект, чтобы получить id
        if photo:
            db_user.photo_path = save_photo(photo, db_user.id)  # Передаем user_id
            db.commit()
            db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка создания пользователя: {str(e)}")

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login, User.is_deleted == False).first()

def authenticate_user(db: Session, login: str, password: str):
    user = get_user_by_login(db, login)
    if user and verify_password(password, user.password):
        return user
    return None

def update_user(db: Session, user_id: int, update_data: dict, photo: UploadFile = None):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    if photo:
        update_data["photo_path"] = save_photo(photo, user_id)
    for key, value in update_data.items():
        if value is not None:
            setattr(user, key, value)
    try:
        db.commit()
        db.refresh(user)
        return user
    except:
        db.rollback()
        raise HTTPException(400, "Ошибка обновления, возможно нарушение уникальности")

def delete_user(db: Session, user_id: int, is_admin: bool):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    if is_admin:
        db.delete(user)
    else:
        user.is_deleted = True
    db.commit()
    return {"message": "Пользователь удален"}