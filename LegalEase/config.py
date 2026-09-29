import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
EXPLANATION_BACKEND = os.getenv("EXPLANATION_BACKEND", "gemini").strip().lower()
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "20000"))

if not GEMINI_API_KEY:
    # The app can still start so the UI/health endpoint can be tested.
    # AI endpoints return a clear configuration error until a key is supplied.
    pass
