from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    weekday = Column(Integer)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    activity = relationship("Activity")
    duration_minutes = Column(Integer)
    intensity = Column(String)
    calories = Column(Integer)
