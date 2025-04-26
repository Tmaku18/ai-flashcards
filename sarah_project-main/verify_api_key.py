import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

def verify_api_key():
    """Verify that the OpenAI API key is correctly formatted."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    print(f"API Key found in .env file: {api_key[:5]}...{api_key[-4:]}")
    
    # Check for common formatting issues
    if "/" in api_key or "+" in api_key or "=" in api_key:
        print("Warning: API key contains special characters (/, +, =) which are not typically found in OpenAI API keys")
    
    if not api_key.startswith("sk-"):
        print("Warning: OpenAI API keys typically start with 'sk-'")
    
    print("\nTo get a valid API key:")
    print("1. Go to https://platform.openai.com/account/api-keys")
    print("2. Create a new API key")
    print("3. Copy the key and update your .env file with:")
    print("   OPENAI_API_KEY=your_new_api_key_here")
    print("\nMake sure there are no spaces, quotes, or special characters in the API key")

if __name__ == "__main__":
    verify_api_key()
