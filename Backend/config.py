import os
from dotenv import load_dotenv

# Load .env (must be at project root or Backend folder)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv()  # fallback

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY NOT LOADED — check your .env file!")

if not GROQ_API_KEY:
    print("⚠️ GROQ_API_KEY missing (optional)")

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY missing (optional)")

if not DEEPSEEK_API_KEY:
    print("⚠️ DEEPSEEK_API_KEY missing (optional)")
