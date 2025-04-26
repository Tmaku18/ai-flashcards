import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import User, FlashcardSet, Flashcard, StudySession, FlashcardProgress
from app.auth.utils import get_password_hash, create_access_token


@pytest.fixture
def test_user(test_db: Session):
    """Create a test user."""
    user = User(
        username="dashboarduser",
        email="dashboard@example.com",
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
def test_flashcard_sets(test_db: Session, test_user: User):
    """Create test flashcard sets."""
    sets = [
        FlashcardSet(
            title="Math Flashcards",
            description="Basic math concepts",
            user_id=test_user.id
        ),
        FlashcardSet(
            title="Science Flashcards",
            description="Basic science concepts",
            user_id=test_user.id
        ),
        FlashcardSet(
            title="History Flashcards",
            description="Important historical events",
            user_id=test_user.id
        )
    ]
    test_db.add_all(sets)
    test_db.commit()
    for flashcard_set in sets:
        test_db.refresh(flashcard_set)
    return sets


@pytest.fixture
def test_flashcards(test_db: Session, test_flashcard_sets):
    """Create test flashcards."""
    flashcards = []
    
    # Math flashcards
    math_cards = [
        Flashcard(
            question="What is 2+2?",
            answer="4",
            set_id=test_flashcard_sets[0].id
        ),
        Flashcard(
            question="What is 3×3?",
            answer="9",
            set_id=test_flashcard_sets[0].id
        )
    ]
    
    # Science flashcards
    science_cards = [
        Flashcard(
            question="What is H2O?",
            answer="Water",
            set_id=test_flashcard_sets[1].id
        ),
        Flashcard(
            question="What is the closest planet to the sun?",
            answer="Mercury",
            set_id=test_flashcard_sets[1].id
        )
    ]
    
    # History flashcards
    history_cards = [
        Flashcard(
            question="When did World War II end?",
            answer="1945",
            set_id=test_flashcard_sets[2].id
        ),
        Flashcard(
            question="Who was the first president of the United States?",
            answer="George Washington",
            set_id=test_flashcard_sets[2].id
        )
    ]
    
    flashcards = math_cards + science_cards + history_cards
    test_db.add_all(flashcards)
    test_db.commit()
    for flashcard in flashcards:
        test_db.refresh(flashcard)
    return flashcards


@pytest.fixture
def test_study_sessions(test_db: Session, test_user: User, test_flashcard_sets):
    """Create test study sessions."""
    now = datetime.now()
    
    # Create completed sessions
    sessions = [
        StudySession(
            user_id=test_user.id,
            set_id=test_flashcard_sets[0].id,
            start_time=now - timedelta(days=2),
            end_time=now - timedelta(days=2) + timedelta(minutes=15)
        ),
        StudySession(
            user_id=test_user.id,
            set_id=test_flashcard_sets[1].id,
            start_time=now - timedelta(days=1),
            end_time=now - timedelta(days=1) + timedelta(minutes=20)
        ),
        StudySession(
            user_id=test_user.id,
            set_id=test_flashcard_sets[2].id,
            start_time=now - timedelta(hours=3),
            end_time=now - timedelta(hours=3) + timedelta(minutes=10)
        )
    ]
    
    # Create an active session
    active_session = StudySession(
        user_id=test_user.id,
        set_id=test_flashcard_sets[0].id,
        start_time=now - timedelta(minutes=5)
    )
    
    sessions.append(active_session)
    test_db.add_all(sessions)
    test_db.commit()
    for session in sessions:
        test_db.refresh(session)
    return sessions


@pytest.fixture
def test_flashcard_progress(test_db: Session, test_user: User, test_flashcards, test_study_sessions):
    """Create test flashcard progress records."""
    progress_records = []
    
    # Progress for math flashcards (mostly correct)
    progress_records.extend([
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[0].id,
            session_id=test_study_sessions[0].id,
            is_correct=True,
            difficulty="easy"
        ),
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[1].id,
            session_id=test_study_sessions[0].id,
            is_correct=True,
            difficulty="medium"
        )
    ])
    
    # Progress for science flashcards (mixed results)
    progress_records.extend([
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[2].id,
            session_id=test_study_sessions[1].id,
            is_correct=False,
            difficulty="hard"
        ),
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[3].id,
            session_id=test_study_sessions[1].id,
            is_correct=True,
            difficulty="medium"
        )
    ])
    
    # Progress for history flashcards (mostly incorrect)
    progress_records.extend([
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[4].id,
            session_id=test_study_sessions[2].id,
            is_correct=False,
            difficulty="hard"
        ),
        FlashcardProgress(
            user_id=test_user.id,
            flashcard_id=test_flashcards[5].id,
            session_id=test_study_sessions[2].id,
            is_correct=False,
            difficulty="medium"
        )
    ])
    
    test_db.add_all(progress_records)
    test_db.commit()
    for record in progress_records:
        test_db.refresh(record)
    return progress_records


def test_get_dashboard_summary(client: TestClient, user_token: str, test_flashcard_sets, test_study_sessions, test_flashcard_progress):
    """Test getting the dashboard summary."""
    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that the summary contains the expected fields
    assert "total_sets" in data
    assert "total_cards" in data
    assert "total_study_sessions" in data
    assert "total_study_time_minutes" in data
    assert "mastered_cards" in data
    assert "struggling_cards" in data
    
    # Check the values
    assert data["total_sets"] == len(test_flashcard_sets)
    assert data["total_study_sessions"] == len(test_study_sessions)
    assert data["total_study_time_minutes"] > 0


def test_get_recent_activity(client: TestClient, user_token: str, test_study_sessions):
    """Test getting recent activity."""
    response = client.get(
        "/api/dashboard/activity",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that the activity list is returned
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check that each activity has the expected fields
    for activity in data:
        assert "id" in activity
        assert "type" in activity
        assert "timestamp" in activity
        assert "details" in activity


def test_get_set_statistics(client: TestClient, user_token: str, test_flashcard_sets):
    """Test getting statistics for all sets."""
    response = client.get(
        "/api/dashboard/sets/stats",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that the set statistics are returned
    assert isinstance(data, list)
    assert len(data) == len(test_flashcard_sets)
    
    # Check that each set statistic has the expected fields
    for set_stat in data:
        assert "set_id" in set_stat
        assert "title" in set_stat
        assert "total_cards" in set_stat
        assert "mastery_percentage" in set_stat
        assert "last_studied" in set_stat


def test_get_study_time_distribution(client: TestClient, user_token: str):
    """Test getting study time distribution."""
    response = client.get(
        "/api/dashboard/study-time",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that the time distribution is returned
    assert "daily" in data
    assert "weekly" in data
    assert "monthly" in data
    
    # Check that each distribution has data
    assert isinstance(data["daily"], list)
    assert isinstance(data["weekly"], list)
    assert isinstance(data["monthly"], list)
