import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import User, FlashcardSet, Flashcard, StudySession
from app.auth.utils import get_password_hash, create_access_token


@pytest.fixture
def test_user(test_db: Session):
    """Create a test user."""
    user = User(
        username="studyuser",
        email="study@example.com",
        hashed_password=get_password_hash("password")
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
        title="Test Study Set",
        description="This is a test flashcard set for studying",
        user_id=test_user.id
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
            set_id=test_flashcard_set.id
        ),
        Flashcard(
            question="What is the largest planet in our solar system?",
            answer="Jupiter",
            set_id=test_flashcard_set.id
        ),
        Flashcard(
            question="What is the chemical symbol for gold?",
            answer="Au",
            set_id=test_flashcard_set.id
        )
    ]
    test_db.add_all(flashcards)
    test_db.commit()
    for flashcard in flashcards:
        test_db.refresh(flashcard)
    return flashcards


@pytest.fixture
def test_study_session(test_db: Session, test_user: User, test_flashcard_set: FlashcardSet):
    """Create a test study session."""
    study_session = StudySession(
        user_id=test_user.id,
        set_id=test_flashcard_set.id
    )
    test_db.add(study_session)
    test_db.commit()
    test_db.refresh(study_session)
    return study_session


def test_start_study_session(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test starting a study session."""
    response = client.post(
        "/api/study/sessions/start",
        json={"set_id": test_flashcard_set.id},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["set_id"] == test_flashcard_set.id
    assert "id" in data
    assert "start_time" in data
    assert data["end_time"] is None


def test_end_study_session(client: TestClient, user_token: str, test_study_session: StudySession):
    """Test ending a study session."""
    response = client.put(
        f"/api/study/sessions/{test_study_session.id}/end",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_study_session.id
    assert data["end_time"] is not None


def test_get_study_sessions(client: TestClient, user_token: str, test_study_session: StudySession):
    """Test getting all study sessions."""
    response = client.get(
        "/api/study/sessions",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(session["id"] == test_study_session.id for session in data)


def test_get_study_session(client: TestClient, user_token: str, test_study_session: StudySession):
    """Test getting a specific study session."""
    response = client.get(
        f"/api/study/sessions/{test_study_session.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_study_session.id
    assert data["set_id"] == test_study_session.set_id
    assert data["user_id"] == test_study_session.user_id


def test_get_study_stats(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet, test_study_session: StudySession):
    """Test getting study statistics for a set."""
    # First, end the study session to have complete data
    client.put(
        f"/api/study/sessions/{test_study_session.id}/end",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    response = client.get(
        f"/api/study/stats/set/{test_flashcard_set.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["set_id"] == test_flashcard_set.id
    assert "total_sessions" in data
    assert data["total_sessions"] >= 1
    assert "average_duration_seconds" in data
    assert "last_session_date" in data
