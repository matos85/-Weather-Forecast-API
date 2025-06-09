from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from schemas import UserCreate, UserOut, UserFilter
from queries import create_user, authenticate_user, get_user_by_id, update_user, delete_user
from filters import get_users_with_filters
from utils import create_access_token, decode_access_token
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # Добавлен OAuth2PasswordRequestForm
from typing import Optional, List
from db_models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(401, "Неверный токен")
    user_id = int(payload["sub"])
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(401, "Пользователь не найден")
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(403, "Недостаточно прав")
    return current_user

@router.post("/register", response_model=UserOut)
async def register(
    login: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    city: str = Form(...),
    first_name: Optional[str] = Form(None),
    patronymic: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    telegram: Optional[str] = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user_data = UserCreate(
        login=login, password=password, email=email, city=city,
        first_name=first_name, patronymic=patronymic, phone=phone, telegram=telegram
    )
    user = create_user(db, user_data, photo)
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Неверные учетные данные")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
async def get_current_user_route(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_route(
    user_id: int,
    city: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    patronymic: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    telegram: Optional[str] = Form(None),
    photo: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Недостаточно прав")
    update_data = {
        "city": city,
        "first_name": first_name,
        "patronymic": patronymic,
        "phone": phone,
        "telegram": telegram
    }
    user = update_user(db, user_id, update_data, photo)
    return user

@router.delete("/users/{user_id}")
async def delete_user_route(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Недостаточно прав")
    is_admin = current_user.is_admin
    return delete_user(db, user_id, is_admin)

@router.post("/users/filter", response_model=List[UserOut])
async def filter_users(
    filters: UserFilter,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    users = get_users_with_filters(
        db,
        city=filters.city,
        first_name=filters.first_name,
        patronymic=filters.patronymic,
        phone=filters.phone,
        telegram=filters.telegram,
        has_photo=filters.has_photo
    )
    return users