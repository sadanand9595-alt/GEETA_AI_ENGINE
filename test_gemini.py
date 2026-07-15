import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Reply with exactly: GEETA AI ENGINE Connected"
    )

    print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")