import logging
from fastapi import FastAPI
from routes import router
from database import Base, engine
import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("auth_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Auth Service",
    description="Сервис авторизации с использованием JWT",
    version="1.0.0",
    openapi_tags=[{"name": "users", "description": "Операции с пользователями"}],
    docs_url="/docs" if ENVIRONMENT != "production" else None,
    redoc_url=None
)

# Убираем Base.metadata.create_all, так как миграции выполняются через Alembic
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Приложение запущено")