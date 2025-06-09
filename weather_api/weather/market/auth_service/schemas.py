from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    login: str
    password: str
    email: EmailStr
    city: str
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None

class UserOut(BaseModel):
    id: int
    login: str
    email: EmailStr
    city: str
    first_name: Optional[str]
    patronymic: Optional[str]
    phone: Optional[str]
    photo_path: Optional[str]
    telegram: Optional[str]
    registration_date: datetime
    is_deleted: bool
    is_admin: bool

    class Config:
        from_attributes = True

# Обновленная модель для фильтров без login и email
class UserFilter(BaseModel):
    city: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    phone: Optional[str] = None
    telegram: Optional[str] = None
    has_photo: Optional[bool] = None