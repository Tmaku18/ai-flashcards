from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class DashboardSummary(BaseModel):
    total_sets: int
    total_cards: int
    total_study_sessions: int
    total_study_time_minutes: float
    mastered_cards: int
    struggling_cards: int
    completion_percentage: float


class ActivityItem(BaseModel):
    id: int
    type: str  # "study_session", "flashcard_set_created", "flashcard_progress"
    timestamp: datetime
    details: Dict[str, str]

    class Config:
        from_attributes = True


class SetStatistics(BaseModel):
    set_id: int
    title: str
    total_cards: int
    mastery_percentage: float
    last_studied: Optional[datetime] = None
    study_count: int
    average_session_minutes: Optional[float] = None

    class Config:
        from_attributes = True


class TimePoint(BaseModel):
    date: str
    minutes: float


class StudyTimeDistribution(BaseModel):
    daily: List[TimePoint]
    weekly: List[TimePoint]
    monthly: List[TimePoint]
