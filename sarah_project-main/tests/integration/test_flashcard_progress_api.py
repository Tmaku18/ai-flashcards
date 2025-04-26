import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, FlashcardSet, Flashcard, StudySession, FlashcardProgress
from app.auth.utils import get_password_hash, create_access_token


@pytest.fixture
def test_user(test_db: Session):
    """Create a test user."""
    user = User(
        username="progressuser",
        email="progress@example.com",
        hashed_password=get_password_hash("password"),
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def user_token(test_user: User):
    """Create a token for the test user."""
    access_token = create_access_token(data={"sub": test_user.username})
    return access_token


@pytest.fixture
def test_flashcard_set(test_db: Session, test_user: User):
    """Create a test flashcard set."""
    flashcard_set = FlashcardSet(
        title="Test Progress Set",
        description="This is a test flashcard set for tracking progress",
        user_id=test_user.id,
    )
    test_db.add(flashcard_set)
    test_db.commit()
    test_db.refresh(flashcard_set)
    return flashcard_set


@pytest.fixture
def test_flashcards(test_db: Session, test_flashcard_set: FlashcardSet):
    """Create test flashcards."""
    flashcards = [
        Flashcard(
            question="What is the capital of France?",
            answer="Paris",
            set_id=test_flashcard_set.id,
        ),
        Flashcard(
            question="What is the largest planet in our solar system?",
            answer="Jupiter",
            set_id=test_flashcard_set.id,
        ),
    ]
    test_db.add_all(flashcards)
    test_db.commit()
    for flashcard in flashcards:
        test_db.refresh(flashcard)
    return flashcards


@pytest.fixture
def test_study_session(
    test_db: Session, test_user: User, test_flashcard_set: FlashcardSet
):
    """Create a test study session."""
    study_session = StudySession(user_id=test_user.id, set_id=test_flashcard_set.id)
    test_db.add(study_session)
    test_db.commit()
    test_db.refresh(study_session)
    return study_session


def test_update_flashcard_progress(
    client: TestClient,
    user_token: str,
    test_study_session: StudySession,
    test_flashcards,
):
    """Test updating flashcard progress."""
    flashcard_id = test_flashcards[0].id

    response = client.post(
        f"/api/study/sessions/{test_study_session.id}/progress",
        json={
            "flashcard_id": flashcard_id,
            "session_id": test_study_session.id,
            "is_correct": True,
            "difficulty": "easy",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    print(f"Response: {response.status_code} - {response.text}")
    assert response.status_code == 201
    data = response.json()
    assert data["flashcard_id"] == flashcard_id
    assert data["session_id"] == test_study_session.id
    assert data["is_correct"] is True
    assert data["difficulty"] == "easy"


def test_get_flashcard_progress(
    client: TestClient,
    user_token: str,
    test_flashcards,
    test_user: User,
    test_db: Session,
):
    """Test getting flashcard progress."""
    flashcard_id = test_flashcards[0].id

    # Create a progress record directly in the database
    progress = FlashcardProgress(
        user_id=test_user.id,
        flashcard_id=flashcard_id,
        is_correct=True,
        difficulty="easy",
    )
    test_db.add(progress)
    test_db.commit()
    test_db.refresh(progress)

    response = client.get(
        f"/api/study/progress/flashcard/{flashcard_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["flashcard_id"] == flashcard_id
    assert data[0]["user_id"] == test_user.id


def test_get_set_progress(
    client: TestClient,
    user_token: str,
    test_flashcard_set: FlashcardSet,
    test_flashcards,
    test_user: User,
    test_db: Session,
):
    """Test getting progress for all flashcards in a set."""
    # Create progress records for all flashcards in the set
    for flashcard in test_flashcards:
        progress = FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=flashcard.id,
            is_correct=True,
            difficulty="medium",
        )
        test_db.add(progress)

    test_db.commit()

    response = client.get(
        f"/api/study/progress/set/{test_flashcard_set.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(test_flashcards)

    # Check that each flashcard has progress data
    flashcard_ids = [flashcard.id for flashcard in test_flashcards]
    for progress in data:
        assert progress["flashcard_id"] in flashcard_ids
        assert "correct_count" in progress
        assert "incorrect_count" in progress
        assert "last_studied" in progress
