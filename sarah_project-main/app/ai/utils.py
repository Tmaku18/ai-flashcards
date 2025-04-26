import os
import re
import json
import logging
from typing import List, Dict, Any
from datetime import datetime

try:
    import google.generativeai as genai
    from ..config import GEMINI_API_KEY

    # Initialize Gemini client if API key is available
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        # Create a mock client for testing
        class MockGeminiResponse:
            def __init__(self, text):
                self.text = '[{"question": "What is the capital of France?", "answer": "Paris"}, {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}]'

        class MockGenerativeModel:
            def __init__(self, model_name):
                self.model_name = model_name

            def generate_content(self, prompt, **kwargs):
                return MockGeminiResponse("mock response")

        # Create a mock genai module
        class MockGenAI:
            def __init__(self):
                pass

            def configure(self, api_key):
                pass

            def GenerativeModel(self, model_name):
                return MockGenerativeModel(model_name)

        genai = MockGenAI()
except ImportError:
    # Create a mock client for testing
    class MockGeminiResponse:
        def __init__(self, text):
            self.text = '[{"question": "What is the capital of France?", "answer": "Paris"}, {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}]'

    class MockGenerativeModel:
        def __init__(self, model_name):
            self.model_name = model_name

        def generate_content(self, prompt, **kwargs):
            return MockGeminiResponse("mock response")

    # Create a mock genai module
    class MockGenAI:
        def __init__(self):
            pass

        def configure(self, api_key):
            pass

        def GenerativeModel(self, model_name):
            return MockGenerativeModel(model_name)

    genai = MockGenAI()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a file handler for AI API logs
file_handler = logging.FileHandler("ai_api.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


from pydantic import BaseModel
from typing import List


# Define the Flashcard schema for structured output
class Flashcard(BaseModel):
    question: str
    answer: str


async def generate_flashcards_from_text(
    text: str, num_cards: int = 10
) -> List[Dict[str, str]]:
    """Generate flashcards from text using Gemini API."""
    # Create prompt for Gemini
    prompt = create_flashcard_prompt(text, num_cards)

    # Log the request
    request_id = datetime.now().strftime("%Y%m%d%H%M%S")
    logger.info(f"Gemini API Request {request_id}:")
    logger.info(f"Model: gemini-2.0-flash")
    logger.info(f"Number of cards requested: {num_cards}")
    logger.info(f"Text length: {len(text)} characters")
    logger.info(
        f"Prompt: {prompt[:100]}..." if len(prompt) > 100 else f"Prompt: {prompt}"
    )

    try:
        # Call Gemini API with structured output
        start_time = datetime.now()
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            },
        )
        end_time = datetime.now()

        # Log the response
        response_time = (end_time - start_time).total_seconds()
        response_text = response.text
        logger.info(f"Gemini API Response {request_id}:")
        logger.info(f"Response time: {response_time:.2f} seconds")
        logger.info(f"Response length: {len(response_text)} characters")

        # Safely log the response text
        if len(response_text) > 100:
            logger.info(f"Response: {response_text[:100]}...")
        else:
            logger.info(f"Response: {response_text}")

        # Parse JSON response
        try:
            # Clean up the response text to handle markdown code blocks
            cleaned_text = response_text

            # Remove markdown code block markers if present
            if "```json" in cleaned_text:
                cleaned_text = cleaned_text.split("```json")[1]
                if "```" in cleaned_text:
                    cleaned_text = cleaned_text.split("```")[0]
            elif "```" in cleaned_text:
                # Handle case where it's just a code block without language specification
                cleaned_text = cleaned_text.split("```")[1]
                if "```" in cleaned_text:
                    cleaned_text = cleaned_text.split("```")[0]

            # Trim whitespace
            cleaned_text = cleaned_text.strip()

            # Parse the JSON
            flashcards_json = json.loads(cleaned_text)
            flashcards = [
                {"question": card["question"], "answer": card["answer"]}
                for card in flashcards_json
            ]
            logger.info(f"Extracted {len(flashcards)} flashcards from JSON response")
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            # Fallback to regex parsing if JSON parsing fails
            logger.warning(
                f"Failed to parse JSON response: {str(e)}. Falling back to regex parsing"
            )
            flashcards = parse_flashcards_from_response(response_text)
            logger.info(f"Extracted {len(flashcards)} flashcards using regex parsing")

        # Return formatted flashcards
        return flashcards
    except Exception as e:
        logger.error(f"Gemini API Error {request_id}: {str(e)}")
        raise


def create_flashcard_prompt(text: str, num_cards: int) -> str:
    """Create a prompt for Gemini to generate flashcards."""
    prompt = f"Generate {num_cards} high-quality flashcard question-answer pairs from the following text. "
    prompt += "Return the flashcards in a structured JSON format as an array of objects, each with 'question' and 'answer' fields. "

    prompt += "\nGuidelines for creating effective flashcards:\n"
    prompt += "1. Focus on key concepts, definitions, important facts, and relationships between ideas\n"
    prompt += "2. Make questions specific and clear, avoiding vague or overly broad questions\n"
    prompt += (
        "3. Keep answers concise and to the point, ideally one to three sentences\n"
    )
    prompt += "4. Include a mix of factual recall, conceptual understanding, and application questions\n"
    prompt += "5. Ensure questions test understanding rather than just memorization\n"
    prompt += "6. Use precise language and avoid ambiguity\n\n"

    prompt += "Example format:\n"
    prompt += '[{"question": "What is the capital of France?", "answer": "Paris"}, '
    prompt += '{"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}]\n\n'

    prompt += f"Text to generate flashcards from:\n{text}"

    return prompt


def parse_flashcards_from_response(response_text: str) -> List[Dict[str, str]]:
    """Parse response text to extract question-answer pairs."""
    flashcards = []

    # Try to parse as JSON first
    try:
        # Clean up the response text to make it valid JSON
        json_text = response_text.strip()
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]

        # Parse JSON
        data = json.loads(json_text)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "question" in item and "answer" in item:
                    flashcards.append(
                        {"question": item["question"], "answer": item["answer"]}
                    )
            if flashcards:
                return flashcards
    except (json.JSONDecodeError, ValueError):
        pass

    # Try to parse Q/A format
    qa_pattern = r"Q:\s*(.+?)\s*\n\s*A:\s*(.+?)(?:\n\s*\n|$)"
    matches = re.findall(qa_pattern, response_text, re.DOTALL)

    for question, answer in matches:
        flashcards.append({"question": question.strip(), "answer": answer.strip()})

    return flashcards
