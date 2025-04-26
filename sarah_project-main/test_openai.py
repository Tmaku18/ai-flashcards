import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

from app.ai.utils import generate_flashcards_from_text

async def test_openai_integration():
    """Test the OpenAI integration by generating flashcards from sample text."""
    print("Testing OpenAI Integration...")
    
    # Sample text for testing
    sample_text = """
    The Python programming language was created by Guido van Rossum and first released in 1991.
    Python is an interpreted, high-level, general-purpose programming language.
    Python's design philosophy emphasizes code readability with its notable use of significant whitespace.
    Python features a dynamic type system and automatic memory management.
    It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural.
    Python is often described as a "batteries included" language due to its comprehensive standard library.
    """
    
    try:
        # Generate flashcards
        flashcards = await generate_flashcards_from_text(sample_text, num_cards=5)
        
        # Print the generated flashcards
        print(f"\nGenerated {len(flashcards)} flashcards:")
        for i, card in enumerate(flashcards, 1):
            print(f"\nFlashcard {i}:")
            print(f"Q: {card['question']}")
            print(f"A: {card['answer']}")
        
        print("\nCheck the 'openai_api.log' file for detailed API request and response logs.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openai_integration())
