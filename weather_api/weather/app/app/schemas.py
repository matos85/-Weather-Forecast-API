from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ActivityBase(BaseModel):
    name: str


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    activity_name: str
    duration_minutes: int
    intensity: str
    calories: int


class RecordCreate(RecordBase):
    pass


class RecordResponse(BaseModel):
    id: int
    timestamp: datetime
    weekday: int
    activity_name: str
    duration_minutes: int
    intensity: str
    calories: int

    class Config:
        orm_mode = True
