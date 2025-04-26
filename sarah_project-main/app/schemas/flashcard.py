from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlashcardBase(BaseModel):
    question: str
    answer: str


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None


class Flashcard(FlashcardBase):
    id: int
    set_id: int
    created_at: datetime

    class Config:
        from_attributes = True
