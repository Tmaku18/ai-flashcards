import os
import pytest
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User
from app.auth.utils import get_password_hash, create_access_token


@pytest.fixture
def test_user(test_db: Session):
    """Create a test user."""
    user = User(
        username="docuser",
        email="doc@example.com",
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


def test_upload_document(client: TestClient, user_token: str):
    """Test that document upload works correctly."""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is a test document.")
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, "rb") as f:
            response = client.post(
                "/api/documents/upload",
                files={"file": ("test.txt", f, "text/plain")},
                headers={"Authorization": f"Bearer {user_token}"}
            )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.txt"
        assert data["content_type"] == "text/plain"
        assert data["size"] > 0
        assert "text_content" in data
        assert data["text_content"] == "This is a test document."
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_upload_invalid_document(client: TestClient, user_token: str):
    """Test that uploading an invalid document fails."""
    # Create a temporary image file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(b"This is not a valid document.")
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, "rb") as f:
            response = client.post(
                "/api/documents/upload",
                files={"file": ("test.jpg", f, "image/jpeg")},
                headers={"Authorization": f"Bearer {user_token}"}
            )
        
        # Check the response
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_get_document_text(client: TestClient, user_token: str):
    """Test that getting document text works correctly."""
    # First upload a document
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is a test document for text extraction.")
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, "rb") as f:
            upload_response = client.post(
                "/api/documents/upload",
                files={"file": ("test_extract.txt", f, "text/plain")},
                headers={"Authorization": f"Bearer {user_token}"}
            )
        
        # Get the text
        response = client.get(
            "/api/documents/text/test_extract.txt",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["text"] == "This is a test document for text extraction."
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_delete_document(client: TestClient, user_token: str):
    """Test that document deletion works correctly."""
    # First upload a document
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is a test document for deletion.")
        temp_file_path = temp_file.name
    
    try:
        # Upload the file
        with open(temp_file_path, "rb") as f:
            upload_response = client.post(
                "/api/documents/upload",
                files={"file": ("test_delete.txt", f, "text/plain")},
                headers={"Authorization": f"Bearer {user_token}"}
            )
        
        # Delete the file
        response = client.delete(
            "/api/documents/test_delete.txt",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        # Check the response
        assert response.status_code == 204
        
        # Try to get the file (should fail)
        get_response = client.get(
            "/api/documents/text/test_delete.txt",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert get_response.status_code == 404
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
