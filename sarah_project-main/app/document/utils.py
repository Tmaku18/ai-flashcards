import os
import PyPDF2
import docx
from typing import List, Optional
import shutil
from pathlib import Path

from ..config import UPLOAD_DIRECTORY, ALLOWED_EXTENSIONS


def is_valid_document(filename: str) -> bool:
    """Check if file extension is supported."""
    # Get file extension
    _, file_extension = os.path.splitext(filename)

    # Check if extension is in allowed extensions
    return file_extension.lower() in ALLOWED_EXTENSIONS


async def save_upload_file(upload_file, filename: str) -> str:
    """Save uploaded file to disk."""
    # Create file path
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Save file
    content = await upload_file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Return file path
    return file_path


def extract_text_from_document(file_path: str) -> str:
    """Extract text from document based on file type."""
    # Get file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Extract text based on file type
    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    elif file_extension == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    # Open PDF file
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract text from each page
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        # Return combined text
        return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    # Open DOCX file
    doc = docx.Document(file_path)

    # Extract text
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    # Return text
    return text.strip()


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    # Open TXT file and read text
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Return text
    return text.strip()


def chunk_text(text: str, chunk_size: int = 2000) -> List[str]:
    """Split text into manageable chunks for AI processing."""
    # If text is shorter than chunk_size, return it as a single chunk
    if len(text) <= chunk_size:
        return [text]

    # Split text into chunks
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])

    # Return list of chunks
    return chunks
