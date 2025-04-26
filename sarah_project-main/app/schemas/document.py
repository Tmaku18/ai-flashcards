from pydantic import BaseModel
from typing import Optional, List

class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    size: int
    text_content: Optional[str] = None

class TextInput(BaseModel):
    text: str
    num_cards: Optional[int] = 10
    title: Optional[str] = "Generated Flashcards"
    description: Optional[str] = "Automatically generated from text"

class DocumentInput(BaseModel):
    document_id: str
    num_cards: Optional[int] = 10
    title: Optional[str] = None
    description: Optional[str] = None
