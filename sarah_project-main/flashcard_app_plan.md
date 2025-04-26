# Flashcard App MVP Plan

## Overview

This document outlines the plan for building a simplified MVP version of a flashcard app that allows users to upload documents and automatically generate flashcards using AI (OpenAI ChatGPT). The development will follow Test-Driven Development (TDD) principles.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (lightweight, file-based)
- **AI Integration**: OpenAI ChatGPT API
- **Document Processing**: PyPDF2 for PDFs, python-docx for Word documents
- **Testing**: pytest for unit and integration tests

## Development Approach

This project will follow Test-Driven Development (TDD) principles:

1. **Write a failing test**: Create a test that defines the expected functionality
2. **Make the test pass**: Implement the minimum code needed to pass the test
3. **Refactor**: Clean up the code while ensuring tests still pass

Each ticket will include both test implementation and feature implementation.

## Implementation Tickets

### Ticket 1: Project Scaffolding and Basic Setup

- Initialize FastAPI project
- Configure SQLite database connection
- Set up project directory structure
- Create requirements.txt with necessary dependencies (including pytest)
- Implement basic configuration management
- Set up CORS middleware
- Create test directory structure

### Ticket 2: Database Models Implementation

- Write tests for database models
- Create User model
- Create FlashcardSet model
- Create Flashcard model
- Create StudySession model
- Implement database initialization function
- Add relationships between models
- Verify all model tests pass

### Ticket 3: User Authentication Implementation

- Write tests for authentication functionality
- Create authentication schemas
- Implement password hashing and verification
- Create registration endpoint
- Create login endpoint
- Implement JWT token generation and validation
- Create authentication dependency for protected routes
- Verify all authentication tests pass

### Ticket 4: Document Upload and Processing

- Write tests for document upload and processing
- Create file upload endpoint
- Implement file validation
- Create document storage service
- Implement text extraction for different file types
- Add text chunking for large documents
- Verify all document processing tests pass

### Ticket 5: OpenAI Integration for Flashcard Generation

- Write tests for AI flashcard generation (with mocks for OpenAI API)
- Set up OpenAI API client
- Create flashcard generation service
- Implement prompt engineering for effective flashcard creation
- Add response parsing to extract question-answer pairs
- Create endpoint for generating flashcards from text
- Verify all AI integration tests pass

### Ticket 6: Flashcard Set and Flashcard Management

- Write tests for flashcard set and flashcard CRUD operations
- Create schemas for flashcard sets and flashcards
- Implement CRUD endpoints for flashcard sets
- Implement CRUD endpoints for flashcards
- Add validation and error handling
- Verify all flashcard management tests pass

### Ticket 7: Study Session Management

- Write tests for study session functionality
- Create schemas for study sessions
- Implement endpoint to start a study session
- Implement endpoint to update study progress
- Implement endpoint to end a study session
- Add basic analytics for completed sessions
- Verify all study session tests pass

### Ticket 8: Simple Frontend Implementation

- Write tests for frontend components (if using a testable frontend framework)
- Create login and registration pages
- Implement document upload interface
- Create flashcard set management interface
- Implement basic flashcard study interface
- Add minimal styling for usability
- Verify frontend functionality through tests

### Ticket 9: Integration Testing and Deployment

- Write end-to-end integration tests
- Ensure all components work together correctly
- Perform user acceptance testing
- Fix any bugs or issues
- Document API endpoints
- Prepare for deployment

## Core Features for MVP

1. User authentication (register/login)
2. Document upload (PDF, DOCX, TXT)
3. AI-powered flashcard generation from documents
4. Flashcard set management (create, view, edit, delete)
5. Basic flashcard study mode
6. Simple progress tracking

## Testing Strategy

### Unit Tests

- Test individual functions and methods in isolation
- Mock external dependencies (database, OpenAI API)
- Focus on edge cases and error handling

### Integration Tests

- Test interactions between components
- Test API endpoints with test client
- Verify database operations

### End-to-End Tests

- Test complete user workflows
- Verify system behavior as a whole

### Test Coverage

- Aim for at least 80% code coverage
- Focus on testing business logic thoroughly
