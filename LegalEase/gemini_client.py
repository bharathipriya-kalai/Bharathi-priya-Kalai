from functools import lru_cache
from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to the .env file and restart EduGenie."
        )
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, *, temperature: float = 0.4, max_output_tokens: int = 1200) -> str:
    from google.genai import types

    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
