from fastapi import FastAPI
from app.database import Base, engine
from app.routers import records, health

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router, tags=["health"])
app.include_router(records.router, prefix="/physical-activity_api", tags=["records"])
