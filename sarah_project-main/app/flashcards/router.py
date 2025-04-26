from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_active_user

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


# Flashcard Set endpoints
@router.post(
    "/sets",
    response_model=schemas.FlashcardSetWithCards,
    status_code=status.HTTP_201_CREATED,
)
def create_flashcard_set(
    flashcard_set: schemas.FlashcardSetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create a new flashcard set."""
    # Create new flashcard set
    db_flashcard_set = models.FlashcardSet(
        **flashcard_set.model_dump(), user_id=current_user.id
    )

    # Add to database
    db.add(db_flashcard_set)
    db.commit()
    db.refresh(db_flashcard_set)

    # Return created set
    return db_flashcard_set


@router.get("/sets", response_model=List[schemas.FlashcardSet])
def get_flashcard_sets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all flashcard sets for the current user."""
    # Get all flashcard sets for current user with pagination
    return (
        db.query(models.FlashcardSet)
        .filter(models.FlashcardSet.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/sets/{set_id}", response_model=schemas.FlashcardSetWithCards)
def get_flashcard_set(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get a specific flashcard set with its cards."""
    # Get flashcard set by ID and check if user has access
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Return set with cards
    return db_flashcard_set


@router.put("/sets/{set_id}", response_model=schemas.FlashcardSetWithCards)
def update_flashcard_set(
    set_id: int,
    flashcard_set: schemas.FlashcardSetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update a flashcard set."""
    # Get flashcard set by ID and check if user has access
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Update set
    update_data = flashcard_set.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flashcard_set, key, value)

    db.commit()
    db.refresh(db_flashcard_set)

    # Return updated set
    return db_flashcard_set


@router.delete("/sets/{set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flashcard_set(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete a flashcard set."""
    # Get flashcard set by ID and check if user has access
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Delete set
    db.delete(db_flashcard_set)
    db.commit()

    # Return success (handled by status_code=status.HTTP_204_NO_CONTENT)


# Flashcard endpoints
@router.post(
    "/sets/{set_id}/cards",
    response_model=schemas.Flashcard,
    status_code=status.HTTP_201_CREATED,
)
def create_flashcard(
    set_id: int,
    flashcard: schemas.FlashcardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Create a new flashcard in a set."""
    # Get flashcard set by ID and check if user has access
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Create new flashcard
    db_flashcard = models.Flashcard(**flashcard.model_dump(), set_id=set_id)

    # Add to database
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)

    # Return created flashcard
    return db_flashcard


@router.get("/sets/{set_id}/cards", response_model=List[schemas.Flashcard])
def get_flashcards(
    set_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all flashcards in a set."""
    # Get flashcard set by ID and check if user has access
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Get all flashcards in set with pagination
    return (
        db.query(models.Flashcard)
        .filter(models.Flashcard.set_id == set_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.put("/sets/{set_id}/cards/{card_id}", response_model=schemas.Flashcard)
def update_flashcard(
    set_id: int,
    card_id: int,
    flashcard: schemas.FlashcardUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update a flashcard."""
    # Check if the flashcard set exists and belongs to the user
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Get the flashcard
    db_flashcard = (
        db.query(models.Flashcard)
        .filter(models.Flashcard.id == card_id, models.Flashcard.set_id == set_id)
        .first()
    )

    if db_flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found"
        )

    # Update flashcard
    update_data = flashcard.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_flashcard, key, value)

    db.commit()
    db.refresh(db_flashcard)

    # Return updated flashcard
    return db_flashcard


@router.delete("/sets/{set_id}/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flashcard(
    set_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete a flashcard."""
    # Check if the flashcard set exists and belongs to the user
    db_flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if db_flashcard_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found"
        )

    # Get the flashcard
    db_flashcard = (
        db.query(models.Flashcard)
        .filter(models.Flashcard.id == card_id, models.Flashcard.set_id == set_id)
        .first()
    )

    if db_flashcard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found"
        )

    # Delete flashcard
    db.delete(db_flashcard)
    db.commit()

    # Return success (handled by status_code=status.HTTP_204_NO_CONTENT)
