import pytest
from datetime import timedelta
from jose import jwt
from sqlalchemy.orm import Session

from app.auth.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    authenticate_user,
)
from app.models import User
from app.config import SECRET_KEY, ALGORITHM


def test_password_hashing():
    """Test that password hashing and verification work correctly."""
    password = "testpassword"
    hashed_password = get_password_hash(password)
    
    # Hashed password should be different from original
    assert hashed_password != password
    
    # Verification should work
    assert verify_password(password, hashed_password) is True
    
    # Wrong password should fail verification
    assert verify_password("wrongpassword", hashed_password) is False


def test_create_access_token():
    """Test that access token creation works correctly."""
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    
    token = create_access_token(data, expires_delta)
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Token should be decodable
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser"
    assert "exp" in payload


def test_authenticate_user(test_db: Session):
    """Test that user authentication works correctly."""
    # Create a test user
    username = "authuser"
    password = "testpassword"
    hashed_password = get_password_hash(password)
    
    user = User(
        username=username,
        email="auth@example.com",
        hashed_password=hashed_password
    )
    test_db.add(user)
    test_db.commit()
    
    # Authentication should succeed with correct credentials
    authenticated_user = authenticate_user(test_db, username, password)
    assert authenticated_user is not None
    assert authenticated_user.username == username
    
    # Authentication should fail with incorrect password
    authenticated_user = authenticate_user(test_db, username, "wrongpassword")
    assert authenticated_user is None
    
    # Authentication should fail with non-existent user
    authenticated_user = authenticate_user(test_db, "nonexistentuser", password)
    assert authenticated_user is None
