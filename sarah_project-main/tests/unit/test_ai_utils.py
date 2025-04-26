import pytest
from unittest.mock import patch, MagicMock
from app.ai.utils import (
    create_flashcard_prompt,
    parse_flashcards_from_response,
    generate_flashcards_from_text,
)


def test_create_flashcard_prompt():
    """Test that the flashcard prompt is created correctly."""
    # Test with default number of cards
    text = "This is a test text for creating flashcards."
    prompt = create_flashcard_prompt(text, 10)

    # Check that the prompt contains the text and number of cards
    assert text in prompt
    assert "10" in prompt

    # Test with custom number of cards
    prompt = create_flashcard_prompt(text, 5)
    assert "5" in prompt


def test_parse_flashcards_from_response():
    """Test that flashcards are parsed correctly from the response."""
    # Test with Q/A format
    response_text = """
    Q: What is the capital of France?
    A: Paris

    Q: What is the largest planet in our solar system?
    A: Jupiter
    """

    flashcards = parse_flashcards_from_response(response_text)

    # Check that the flashcards were parsed correctly
    assert len(flashcards) == 2
    assert flashcards[0]["question"] == "What is the capital of France?"
    assert flashcards[0]["answer"] == "Paris"
    assert (
        flashcards[1]["question"] == "What is the largest planet in our solar system?"
    )
    assert flashcards[1]["answer"] == "Jupiter"

    # Test with numbered format
    response_text = """
    1. Q: What is the capital of Germany?
       A: Berlin

    2. Q: What is the largest ocean?
       A: Pacific Ocean
    """

    flashcards = parse_flashcards_from_response(response_text)

    # Check that the flashcards were parsed correctly
    assert len(flashcards) == 2
    assert flashcards[0]["question"] == "What is the capital of Germany?"
    assert flashcards[0]["answer"] == "Berlin"
    assert flashcards[1]["question"] == "What is the largest ocean?"
    assert flashcards[1]["answer"] == "Pacific Ocean"

    # Test with JSON-like format
    response_text = """
    [
      {"question": "What is the capital of Italy?", "answer": "Rome"},
      {"question": "What is the largest desert?", "answer": "Sahara"}
    ]
    """

    flashcards = parse_flashcards_from_response(response_text)

    # Check that the flashcards were parsed correctly
    assert len(flashcards) == 2
    assert flashcards[0]["question"] == "What is the capital of Italy?"
    assert flashcards[0]["answer"] == "Rome"
    assert flashcards[1]["question"] == "What is the largest desert?"
    assert flashcards[1]["answer"] == "Sahara"


@pytest.mark.asyncio
@patch("app.ai.utils.genai.GenerativeModel")
async def test_generate_flashcards_from_text(mock_model):
    """Test that flashcards are generated correctly from text."""
    # Mock the Gemini API response
    mock_instance = mock_model.return_value
    mock_response = MagicMock()
    mock_response.text = '[{"question": "What is the capital of France?", "answer": "Paris"}, {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}]'
    mock_instance.generate_content.return_value = mock_response

    # Generate flashcards
    text = "France is a country in Europe. Its capital is Paris. Jupiter is the largest planet in our solar system."
    flashcards = await generate_flashcards_from_text(text, 2)

    # Check that the flashcards were generated correctly
    assert len(flashcards) == 2
    assert flashcards[0]["question"] == "What is the capital of France?"
    assert flashcards[0]["answer"] == "Paris"
    assert (
        flashcards[1]["question"] == "What is the largest planet in our solar system?"
    )
    assert flashcards[1]["answer"] == "Jupiter"

    # Check that the Gemini API was called with the correct parameters
    mock_model.assert_called_once_with("gemini-2.0-flash")
    mock_instance.generate_content.assert_called_once()
