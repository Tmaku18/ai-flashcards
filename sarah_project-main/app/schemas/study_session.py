from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StudySessionBase(BaseModel):
    set_id: int


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionUpdate(BaseModel):
    end_time: Optional[datetime] = None


class StudySession(StudySessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True
