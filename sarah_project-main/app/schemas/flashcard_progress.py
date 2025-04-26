from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class FlashcardProgressBase(BaseModel):
    flashcard_id: int
    is_correct: bool
    difficulty: DifficultyLevel


class FlashcardProgressCreate(FlashcardProgressBase):
    session_id: int


class FlashcardProgress(FlashcardProgressBase):
    id: int
    user_id: int
    session_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FlashcardProgressStats(BaseModel):
    flashcard_id: int
    correct_count: int
    incorrect_count: int
    last_studied: Optional[datetime] = None
    average_difficulty: Optional[float] = None

    class Config:
        from_attributes = True


class StudySetStats(BaseModel):
    set_id: int
    total_sessions: int
    average_duration_seconds: Optional[float] = None
    last_session_date: Optional[datetime] = None
    total_cards: int
    mastered_cards: int
    struggling_cards: int

    class Config:
        from_attributes = True
