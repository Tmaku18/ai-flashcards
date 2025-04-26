from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .flashcard import Flashcard


class FlashcardSetBase(BaseModel):
    title: str
    description: Optional[str] = None


class FlashcardSetCreate(FlashcardSetBase):
    pass


class FlashcardSetUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class FlashcardSet(FlashcardSetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    source_document: Optional[str] = None

    class Config:
        from_attributes = True


class FlashcardSetWithCards(FlashcardSet):
    flashcards: List[Flashcard] = []
