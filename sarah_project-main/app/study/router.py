from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from sqlalchemy import func

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_active_user

router = APIRouter(prefix="/study", tags=["study"])


@router.post(
    "/sessions/start",
    response_model=schemas.StudySession,
    status_code=status.HTTP_201_CREATED,
)
def start_study_session(
    session_input: schemas.StudySessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Start a new study session with consistent timezone handling."""
    from datetime import timezone

    # Get flashcard set by ID and check if user has access
    flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == session_input.set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if not flashcard_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found or you don't have access to it",
        )

    # Create new study session
    study_session = models.StudySession(
        user_id=current_user.id, set_id=session_input.set_id
    )

    # Add to database
    db.add(study_session)
    db.commit()
    db.refresh(study_session)

    # Return created session
    return study_session


@router.put("/sessions/{session_id}/end", response_model=schemas.StudySession)
def end_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """End a study session."""
    # Get study session by ID and check if user has access
    study_session = (
        db.query(models.StudySession)
        .filter(
            models.StudySession.id == session_id,
            models.StudySession.user_id == current_user.id,
        )
        .first()
    )

    if not study_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found or you don't have access to it",
        )

    if study_session.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Study session has already ended",
        )

    # Update end time
    study_session = study_session.end_session(db)

    # Return updated session
    return study_session


@router.get("/sessions", response_model=List[schemas.StudySession])
def get_study_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get all study sessions for the current user."""
    # Get all study sessions for current user with pagination
    return (
        db.query(models.StudySession)
        .filter(models.StudySession.user_id == current_user.id)
        .order_by(models.StudySession.start_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/sessions/{session_id}", response_model=schemas.StudySession)
def get_study_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get a specific study session."""
    # Get study session by ID and check if user has access
    study_session = (
        db.query(models.StudySession)
        .filter(
            models.StudySession.id == session_id,
            models.StudySession.user_id == current_user.id,
        )
        .first()
    )

    if not study_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found or you don't have access to it",
        )

    # Return session
    return study_session


@router.get("/stats/set/{set_id}", response_model=schemas.StudySetStats)
def get_study_stats_for_set(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get study statistics for a flashcard set."""
    # Get flashcard set by ID and check if user has access
    flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if not flashcard_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found or you don't have access to it",
        )

    # Calculate study statistics
    # 1. Total number of sessions
    total_sessions = (
        db.query(func.count(models.StudySession.id))
        .filter(
            models.StudySession.set_id == set_id,
            models.StudySession.user_id == current_user.id,
        )
        .scalar()
    )

    # 2. Average duration of sessions
    avg_duration = (
        db.query(
            func.avg(
                func.julianday(models.StudySession.end_time)
                - func.julianday(models.StudySession.start_time)
            )
            * 24
            * 60
            * 60  # Convert to seconds
        )
        .filter(
            models.StudySession.set_id == set_id,
            models.StudySession.user_id == current_user.id,
            models.StudySession.end_time.isnot(None),
        )
        .scalar()
    )

    # 3. Last session date
    last_session = (
        db.query(func.max(models.StudySession.start_time))
        .filter(
            models.StudySession.set_id == set_id,
            models.StudySession.user_id == current_user.id,
        )
        .scalar()
    )

    # 4. Total cards in the set
    total_cards = (
        db.query(func.count(models.Flashcard.id))
        .filter(models.Flashcard.set_id == set_id)
        .scalar()
    )

    # 5. Mastered cards (correct answers > 2 times and average difficulty < 2)
    mastered_cards = 0
    struggling_cards = 0

    # Get progress stats for all cards in the set
    progress_stats = models.FlashcardProgress.get_stats_by_set(
        db, set_id, current_user.id
    )

    for stat in progress_stats:
        if (
            stat.correct_count
            and stat.correct_count > 2
            and stat.average_difficulty
            and stat.average_difficulty < 2
        ):
            mastered_cards += 1
        elif stat.incorrect_count and stat.incorrect_count > stat.correct_count:
            struggling_cards += 1

    # Return statistics
    return schemas.StudySetStats(
        set_id=set_id,
        total_sessions=total_sessions or 0,
        average_duration_seconds=avg_duration,
        last_session_date=last_session,
        total_cards=total_cards or 0,
        mastered_cards=mastered_cards,
        struggling_cards=struggling_cards,
    )


@router.post(
    "/sessions/{session_id}/progress",
    response_model=schemas.FlashcardProgress,
    status_code=status.HTTP_201_CREATED,
)
def update_flashcard_progress(
    session_id: int,
    progress: schemas.FlashcardProgressBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Update progress for a flashcard in a study session."""
    # Check if the study session exists and belongs to the user
    study_session = (
        db.query(models.StudySession)
        .filter(
            models.StudySession.id == session_id,
            models.StudySession.user_id == current_user.id,
        )
        .first()
    )

    if not study_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study session not found or you don't have access to it",
        )

    # Check if the flashcard exists and belongs to the set being studied
    flashcard = (
        db.query(models.Flashcard)
        .join(models.FlashcardSet, models.Flashcard.set_id == models.FlashcardSet.id)
        .filter(
            models.Flashcard.id == progress.flashcard_id,
            models.FlashcardSet.id == study_session.set_id,
        )
        .first()
    )

    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found or doesn't belong to the set being studied",
        )

    # Create progress record
    progress_record = models.FlashcardProgress(
        user_id=current_user.id,
        flashcard_id=progress.flashcard_id,
        session_id=session_id,
        is_correct=progress.is_correct,
        difficulty=progress.difficulty,
    )

    # Add to database
    db.add(progress_record)
    db.commit()
    db.refresh(progress_record)

    # Return created progress record
    return progress_record


@router.get(
    "/progress/flashcard/{flashcard_id}", response_model=List[schemas.FlashcardProgress]
)
def get_flashcard_progress(
    flashcard_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get progress history for a specific flashcard."""
    # Check if the flashcard exists
    flashcard = (
        db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    )

    if not flashcard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found"
        )

    # Check if the user has access to the flashcard
    flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == flashcard.set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if not flashcard_set:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this flashcard",
        )

    # Get progress records
    progress_records = models.FlashcardProgress.get_by_flashcard(
        db, flashcard_id, current_user.id
    )

    # Return progress records
    return progress_records


@router.get(
    "/progress/set/{set_id}", response_model=List[schemas.FlashcardProgressStats]
)
def get_set_progress(
    set_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get progress statistics for all flashcards in a set."""
    # Check if the flashcard set exists and belongs to the user
    flashcard_set = (
        db.query(models.FlashcardSet)
        .filter(
            models.FlashcardSet.id == set_id,
            models.FlashcardSet.user_id == current_user.id,
        )
        .first()
    )

    if not flashcard_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard set not found or you don't have access to it",
        )

    # Get progress stats for all cards in the set
    progress_stats = models.FlashcardProgress.get_stats_by_set(
        db, set_id, current_user.id
    )

    # Convert to schema objects
    result = []
    for stat in progress_stats:
        result.append(
            schemas.FlashcardProgressStats(
                flashcard_id=stat.flashcard_id,
                correct_count=stat.correct_count or 0,
                incorrect_count=stat.incorrect_count or 0,
                last_studied=stat.last_studied,
                average_difficulty=stat.average_difficulty,
            )
        )

    # Return progress stats
    return result
