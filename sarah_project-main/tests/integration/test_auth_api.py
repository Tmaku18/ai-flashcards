import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User
from app.auth.utils import get_password_hash


def test_register_user(client: TestClient, test_db: Session):
    """Test that user registration works correctly."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    
    # Check that the user was created in the database
    user = test_db.query(User).filter(User.username == "testuser").first()
    assert user is not None
    assert user.email == "test@example.com"
    
    # Password should be hashed
    assert user.hashed_password != "testpassword"


def test_register_duplicate_username(client: TestClient, test_db: Session):
    """Test that registering with a duplicate username fails."""
    # Create a user first
    user = User(
        username="existinguser",
        email="existing@example.com",
        hashed_password=get_password_hash("password")
    )
    test_db.add(user)
    test_db.commit()
    
    # Try to register with the same username
    response = client.post(
        "/api/auth/register",
        json={
            "username": "existinguser",
            "email": "new@example.com",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_register_duplicate_email(client: TestClient, test_db: Session):
    """Test that registering with a duplicate email fails."""
    # Create a user first
    user = User(
        username="userwithemail",
        email="duplicate@example.com",
        hashed_password=get_password_hash("password")
    )
    test_db.add(user)
    test_db.commit()
    
    # Try to register with the same email
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "duplicate@example.com",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login(client: TestClient, test_db: Session):
    """Test that login works correctly."""
    # Create a user first
    username = "loginuser"
    password = "loginpassword"
    user = User(
        username=username,
        email="login@example.com",
        hashed_password=get_password_hash(password)
    )
    test_db.add(user)
    test_db.commit()
    
    # Login with correct credentials
    response = client.post(
        "/api/auth/token",
        data={
            "username": username,
            "password": password
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, test_db: Session):
    """Test that login with incorrect password fails."""
    # Create a user first
    username = "wrongpassuser"
    password = "correctpass"
    user = User(
        username=username,
        email="wrongpass@example.com",
        hashed_password=get_password_hash(password)
    )
    test_db.add(user)
    test_db.commit()
    
    # Login with incorrect password
    response = client.post(
        "/api/auth/token",
        data={
            "username": username,
            "password": "wrongpass"
        }
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Test that login with non-existent user fails."""
    response = client.post(
        "/api/auth/token",
        data={
            "username": "nonexistentuser",
            "password": "password"
        }
    )
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_get_current_user(client: TestClient, test_db: Session):
    """Test that getting the current user works correctly."""
    # Create a user first
    username = "currentuser"
    password = "currentpass"
    user = User(
        username=username,
        email="current@example.com",
        hashed_password=get_password_hash(password)
    )
    test_db.add(user)
    test_db.commit()
    
    # Login to get a token
    response = client.post(
        "/api/auth/token",
        data={
            "username": username,
            "password": password
        }
    )
    
    token = response.json()["access_token"]
    
    # Get current user with token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username
    assert data["email"] == "current@example.com"


def test_get_current_user_invalid_token(client: TestClient):
    """Test that getting the current user with an invalid token fails."""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]
