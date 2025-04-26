import os
import shutil
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from ..database import get_db
from ..auth.utils import get_current_active_user
from .utils import (
    is_valid_document,
    save_upload_file,
    extract_text_from_document,
    chunk_text,
)
from ..config import UPLOAD_DIRECTORY, MAX_UPLOAD_SIZE

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=schemas.DocumentUpload)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Upload a document and extract text."""
    # Validate file type
    if not is_valid_document(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Supported types: PDF, DOCX, TXT",
        )

    # Check file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    await file.seek(0)

    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE / (1024 * 1024)}MB",
        )

    # Save file to disk
    file_path = await save_upload_file(file, file.filename)

    # Extract text from document
    text_content = extract_text_from_document(file_path)

    # Return document information
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file_size,
        "text_content": text_content,
    }


@router.get("/text/{filename}")
async def get_document_text(
    filename: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Get text from an uploaded document."""
    # Check if file exists
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Extract text from document
    text = extract_text_from_document(file_path)

    # Return text
    return {"text": text}


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    filename: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """Delete an uploaded document."""
    # Check if file exists
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    # Delete file
    os.remove(file_path)

    # Return success (handled by status_code=status.HTTP_204_NO_CONTENT)
