from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    city = Column(String)
    first_name = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    photo_path = Column(String, nullable=True)
    telegram = Column(String, unique=True, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)