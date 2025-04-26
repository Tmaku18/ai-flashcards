import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, FlashcardSet, Flashcard
from app.auth.utils import get_password_hash, create_access_token


@pytest.fixture
def test_user(test_db: Session):
    """Create a test user."""
    user = User(
        username="flashcarduser",
        email="flashcard@example.com",
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
        title="Test Flashcard Set",
        description="This is a test flashcard set",
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
        )
    ]
    test_db.add_all(flashcards)
    test_db.commit()
    for flashcard in flashcards:
        test_db.refresh(flashcard)
    return flashcards


def test_create_flashcard_set(client: TestClient, user_token: str):
    """Test creating a flashcard set."""
    response = client.post(
        "/api/flashcards/sets",
        json={
            "title": "New Flashcard Set",
            "description": "This is a new flashcard set"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Flashcard Set"
    assert data["description"] == "This is a new flashcard set"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "user_id" in data
    assert "flashcards" in data
    assert len(data["flashcards"]) == 0


def test_get_flashcard_sets(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test getting all flashcard sets."""
    response = client.get(
        "/api/flashcards/sets",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(set["title"] == "Test Flashcard Set" for set in data)


def test_get_flashcard_set(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test getting a specific flashcard set."""
    response = client.get(
        f"/api/flashcards/sets/{test_flashcard_set.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Flashcard Set"
    assert data["description"] == "This is a test flashcard set"
    assert data["id"] == test_flashcard_set.id


def test_update_flashcard_set(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test updating a flashcard set."""
    response = client.put(
        f"/api/flashcards/sets/{test_flashcard_set.id}",
        json={
            "title": "Updated Flashcard Set",
            "description": "This is an updated flashcard set"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Flashcard Set"
    assert data["description"] == "This is an updated flashcard set"
    assert data["id"] == test_flashcard_set.id


def test_delete_flashcard_set(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test deleting a flashcard set."""
    response = client.delete(
        f"/api/flashcards/sets/{test_flashcard_set.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 204
    
    # Verify the flashcard set is deleted
    response = client.get(
        f"/api/flashcards/sets/{test_flashcard_set.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404


def test_create_flashcard(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet):
    """Test creating a flashcard."""
    response = client.post(
        f"/api/flashcards/sets/{test_flashcard_set.id}/cards",
        json={
            "question": "What is the capital of Germany?",
            "answer": "Berlin"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == "What is the capital of Germany?"
    assert data["answer"] == "Berlin"
    assert data["set_id"] == test_flashcard_set.id
    assert "id" in data


def test_get_flashcards(client: TestClient, user_token: str, test_flashcard_set: FlashcardSet, test_flashcards):
    """Test getting all flashcards in a set."""
    response = client.get(
        f"/api/flashcards/sets/{test_flashcard_set.id}/cards",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(card["question"] == "What is the capital of France?" for card in data)
    assert any(card["question"] == "What is the largest planet in our solar system?" for card in data)


def test_update_flashcard(client: TestClient, user_token: str, test_flashcards):
    """Test updating a flashcard."""
    flashcard_id = test_flashcards[0].id
    set_id = test_flashcards[0].set_id
    
    response = client.put(
        f"/api/flashcards/sets/{set_id}/cards/{flashcard_id}",
        json={
            "question": "What is the capital of France? (Updated)",
            "answer": "Paris (Updated)"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is the capital of France? (Updated)"
    assert data["answer"] == "Paris (Updated)"
    assert data["id"] == flashcard_id


def test_delete_flashcard(client: TestClient, user_token: str, test_flashcards):
    """Test deleting a flashcard."""
    flashcard_id = test_flashcards[0].id
    set_id = test_flashcards[0].set_id
    
    response = client.delete(
        f"/api/flashcards/sets/{set_id}/cards/{flashcard_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 204
    
    # Verify the flashcard is deleted
    response = client.get(
        f"/api/flashcards/sets/{set_id}/cards",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert all(card["id"] != flashcard_id for card in data)
