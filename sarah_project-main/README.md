# Flashcard App MVP

A simple flashcard application that allows users to upload documents and automatically generate flashcards using AI. This project follows Test-Driven Development (TDD) principles.

## Features

- User authentication (register/login)
- Document upload (PDF, DOCX, TXT)
- AI-powered flashcard generation from documents
- Flashcard set management (create, view, edit, delete)
- Basic flashcard study mode
- Simple progress tracking

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **AI Integration**: OpenAI ChatGPT API
- **Document Processing**: PyPDF2, python-docx
- **Testing**: pytest, pytest-cov for test coverage

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your OpenAI API key
5. Run the application:
   ```
   python run.py
   ```
6. Access the API at http://localhost:8000
7. Access the API documentation at http://localhost:8000/docs

## Running Tests

To run the tests:

```
pytest
```

To run tests with coverage report:

```
pytest --cov=app
```

## Development Approach

This project follows Test-Driven Development (TDD) principles:

1. **Write a failing test**: Create a test that defines the expected functionality
2. **Make the test pass**: Implement the minimum code needed to pass the test
3. **Refactor**: Clean up the code while ensuring tests still pass

## Project Structure

```
flashcard_app/
├── app/
│   ├── ai/              # AI integration
│   ├── auth/            # Authentication
│   ├── document/        # Document upload and processing
│   ├── flashcards/      # Flashcard management
│   ├── schemas/         # Pydantic models
│   ├── study/           # Study session management
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── main.py          # FastAPI application
│   └── models.py        # SQLAlchemy models
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── conftest.py      # Test configuration and fixtures
├── uploads/             # Uploaded documents
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── requirements.txt     # Dependencies
├── pytest.ini          # Pytest configuration
├── run.py               # Entry point
└── README.md            # Documentation
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user information

### Documents

- `POST /documents/upload` - Upload a document
- `GET /documents/text/{filename}` - Get text from a document
- `DELETE /documents/{filename}` - Delete a document

### AI

- `POST /ai/generate-flashcards` - Generate flashcards from text
- `POST /ai/generate-from-document` - Generate flashcards from a document

### Flashcards

- `POST /flashcards/sets` - Create a flashcard set
- `GET /flashcards/sets` - Get all flashcard sets
- `GET /flashcards/sets/{set_id}` - Get a specific flashcard set
- `PUT /flashcards/sets/{set_id}` - Update a flashcard set
- `DELETE /flashcards/sets/{set_id}` - Delete a flashcard set
- `POST /flashcards/sets/{set_id}/cards` - Create a flashcard
- `GET /flashcards/sets/{set_id}/cards` - Get all flashcards in a set
- `PUT /flashcards/sets/{set_id}/cards/{card_id}` - Update a flashcard
- `DELETE /flashcards/sets/{set_id}/cards/{card_id}` - Delete a flashcard

### Study

- `POST /study/sessions/start` - Start a study session
- `PUT /study/sessions/{session_id}/end` - End a study session
- `GET /study/sessions` - Get all study sessions
- `GET /study/sessions/{session_id}` - Get a specific study session
- `GET /study/stats/set/{set_id}` - Get study statistics for a set
