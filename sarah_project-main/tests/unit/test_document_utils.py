import os
import pytest
import tempfile
import asyncio
from pathlib import Path

from app.document.utils import (
    is_valid_document,
    save_upload_file,
    extract_text_from_document,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    chunk_text,
)


def test_is_valid_document():
    """Test that document validation works correctly."""
    # Valid document types
    assert is_valid_document("test.pdf") is True
    assert is_valid_document("test.docx") is True
    assert is_valid_document("test.txt") is True

    # Invalid document types
    assert is_valid_document("test.jpg") is False
    assert is_valid_document("test.png") is False
    assert is_valid_document("test.exe") is False
    assert is_valid_document("test") is False


@pytest.mark.asyncio
async def test_save_upload_file():
    """Test that file saving works correctly."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_file_path = temp_file.name

    try:
        # Create a mock upload file
        class MockUploadFile:
            async def read(self):
                with open(temp_file_path, "rb") as f:
                    return f.read()

        upload_file = MockUploadFile()

        # Save the file
        filename = "test.txt"
        file_path = await save_upload_file(upload_file, filename)

        # Check that the file was saved correctly
        assert os.path.exists(file_path)
        with open(file_path, "r") as f:
            content = f.read()
            assert content == "Test content"

        # Clean up
        os.remove(file_path)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_extract_text_from_txt():
    """Test that text extraction from TXT files works correctly."""
    # Create a temporary TXT file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is a test text file.")
        temp_file_path = temp_file.name

    try:
        # Extract text from the file
        text = extract_text_from_txt(temp_file_path)

        # Check that the text was extracted correctly
        assert text == "This is a test text file."
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def test_chunk_text():
    """Test that text chunking works correctly."""
    # Create a long text
    text = "This is a test text. " * 100

    # Chunk the text
    chunks = chunk_text(text, chunk_size=100)

    # Check that the text was chunked correctly
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 100

    # Reconstruct the text
    reconstructed_text = "".join(chunks)
    assert reconstructed_text == text
