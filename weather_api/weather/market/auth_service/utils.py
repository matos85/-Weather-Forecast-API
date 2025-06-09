import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import UploadFile
from dotenv import load_dotenv
import shutil

# Загружаем переменные окружения
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Контекст для хэширования паролей с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хэширует пароль с использованием bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введённый пароль хэшированному."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    """Создаёт JWT-токен для пользователя."""
    to_encode = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """Декодирует JWT-токен и возвращает его содержимое."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def save_photo(photo: UploadFile, user_id: int) -> str:
    """Сохраняет загруженное фото в директорию static/photos/<user_id>."""
    current_date = datetime.utcnow()
    day = current_date.strftime("%d")
    month = current_date.strftime("%m")
    year = current_date.strftime("%Y")

    base_path = f"static/photos/{user_id}"
    os.makedirs(base_path, exist_ok=True)

    existing_files = len([f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))])
    file_number = existing_files + 1
