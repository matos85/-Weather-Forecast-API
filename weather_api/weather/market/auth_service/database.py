from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Проверка и логирование значения DATABASE_URL
logger.info(f"DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")
if not SQLALCHEMY_DATABASE_URL:
    logger.error("DATABASE_URL is not set in environment variables")
    raise ValueError("DATABASE_URL is not set in environment variables")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
except Exception as e:
    logger.error(f"Failed to create engine: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()