import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import User, FlashcardSet, Flashcard, StudySession

def test_user_model(test_db: Session):
    """Test that the User model can be created and has the expected attributes."""
    # Create a user
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    
    # Add to database
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    # Check attributes
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpassword"
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)
    
    # Check relationships
    assert hasattr(user, "flashcard_sets")
    assert hasattr(user, "study_sessions")

def test_flashcard_set_model(test_db: Session):
    """Test that the FlashcardSet model can be created and has the expected attributes."""
    # Create a user first
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    test_db.add(user)
    test_db.commit()
    
    # Create a flashcard set
    flashcard_set = FlashcardSet(
        title="Test Set",
        description="Test Description",
        user_id=user.id
    )
    
    # Add to database
    test_db.add(flashcard_set)
    test_db.commit()
    test_db.refresh(flashcard_set)
    
    # Check attributes
    assert flashcard_set.id is not None
    assert flashcard_set.title == "Test Set"
    assert flashcard_set.description == "Test Description"
    assert flashcard_set.user_id == user.id
    assert isinstance(flashcard_set.created_at, datetime)
    
    # Check relationships
    assert hasattr(flashcard_set, "owner")
    assert hasattr(flashcard_set, "flashcards")
    assert hasattr(flashcard_set, "study_sessions")
    
    # Check relationship with user
    assert flashcard_set.owner.id == user.id

def test_flashcard_model(test_db: Session):
    """Test that the Flashcard model can be created and has the expected attributes."""
    # Create a user first
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    test_db.add(user)
    test_db.commit()
    
    # Create a flashcard set
    flashcard_set = FlashcardSet(
        title="Test Set",
        description="Test Description",
        user_id=user.id
    )
    test_db.add(flashcard_set)
    test_db.commit()
    
    # Create a flashcard
    flashcard = Flashcard(
        question="Test Question",
        answer="Test Answer",
        set_id=flashcard_set.id
    )
    
    # Add to database
    test_db.add(flashcard)
    test_db.commit()
    test_db.refresh(flashcard)
    
    # Check attributes
    assert flashcard.id is not None
    assert flashcard.question == "Test Question"
    assert flashcard.answer == "Test Answer"
    assert flashcard.set_id == flashcard_set.id
    assert isinstance(flashcard.created_at, datetime)
    
    # Check relationships
    assert hasattr(flashcard, "flashcard_set")
    
    # Check relationship with flashcard set
    assert flashcard.flashcard_set.id == flashcard_set.id

def test_study_session_model(test_db: Session):
    """Test that the StudySession model can be created and has the expected attributes."""
    # Create a user first
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword"
    )
    test_db.add(user)
    test_db.commit()
    
    # Create a flashcard set
    flashcard_set = FlashcardSet(
        title="Test Set",
        description="Test Description",
        user_id=user.id
    )
    test_db.add(flashcard_set)
    test_db.commit()
    
    # Create a study session
    study_session = StudySession(
        user_id=user.id,
        set_id=flashcard_set.id
    )
    
    # Add to database
    test_db.add(study_session)
    test_db.commit()
    test_db.refresh(study_session)
    
    # Check attributes
    assert study_session.id is not None
    assert study_session.user_id == user.id
    assert study_session.set_id == flashcard_set.id
    assert isinstance(study_session.start_time, datetime)
    assert study_session.end_time is None
    
    # Check relationships
    assert hasattr(study_session, "user")
    assert hasattr(study_session, "flashcard_set")
    
    # Check relationship with user and flashcard set
    assert study_session.user.id == user.id
    assert study_session.flashcard_set.id == flashcard_set.id
