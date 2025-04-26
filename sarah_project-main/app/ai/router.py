from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_active_user
from .utils import generate_flashcards_from_text
from ..document.utils import extract_text_from_document

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-flashcards", response_model=List[schemas.FlashcardCreate])
async def generate_flashcards(
    text_input: schemas.TextInput,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Generate flashcards from text."""
    try:
        # Call OpenAI to generate flashcards
        flashcards = await generate_flashcards_from_text(
            text_input.text, text_input.num_cards
        )

        # Convert to FlashcardCreate schema
        result = [
            schemas.FlashcardCreate(question=card["question"], answer=card["answer"])
            for card in flashcards
        ]

        # Return generated flashcards
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating flashcards: {str(e)}",
        )


@router.post("/generate-from-document", response_model=schemas.FlashcardSetWithCards)
async def generate_flashcards_from_document(
    document_input: schemas.DocumentInput,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Generate flashcards from an uploaded document."""
    try:
        # Get document text
        import os
        from ..config import UPLOAD_DIRECTORY

        file_path = os.path.join(UPLOAD_DIRECTORY, document_input.document_id)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
            )

        text = extract_text_from_document(file_path)

        # Generate flashcards from text
        flashcards = await generate_flashcards_from_text(text, document_input.num_cards)

        # Create flashcard set with generated cards
        title = document_input.title or f"Flashcards from {document_input.document_id}"
        description = (
            document_input.description or f"Generated from {document_input.document_id}"
        )

        flashcard_set = models.FlashcardSet(
            title=title,
            description=description,
            user_id=current_user.id,
            source_document=document_input.document_id,
        )

        db.add(flashcard_set)
        db.commit()
        db.refresh(flashcard_set)

        # Add flashcards to the set
        for card in flashcards:
            flashcard = models.Flashcard(
                question=card["question"],
                answer=card["answer"],
                set_id=flashcard_set.id,
            )
            db.add(flashcard)

        db.commit()
        db.refresh(flashcard_set)

        # Return created set with cards
        return flashcard_set
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating flashcards from document: {str(e)}",
        )
