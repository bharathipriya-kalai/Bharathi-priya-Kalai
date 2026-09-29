import json
import re
from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(passage: str):
    passage = passage.strip()
    if not passage:
        raise ValueError("Please provide a topic or passage for the quiz.")

    prompt = f"""Create exactly 3 multiple-choice questions from the educational text below.
Return ONLY valid JSON. No Markdown and no commentary.
JSON shape:
{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":"A"}}]}}
The answer must be the exact option text, not a letter.
Make distractors plausible and ensure every answer is supported by the source text.

SOURCE TEXT:
{passage}
"""
    raw = clean_json_block(generate_text(prompt, temperature=0.25, max_output_tokens=1400))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid quiz JSON. Please try again.") from exc

    questions = data.get("questions") if isinstance(data, dict) else None
    if not isinstance(questions, list) or len(questions) != 3:
        raise RuntimeError("Quiz generation did not return exactly 3 questions.")

    validated = []
    for item in questions:
        if not isinstance(item, dict):
            raise RuntimeError("Quiz contains an invalid question object.")
        options = item.get("options")
        answer = item.get("answer")
        if not isinstance(options, list) or len(options) != 4 or answer not in options:
            raise RuntimeError("Quiz question must contain 4 options and a valid answer.")
        validated.append({
            "question": str(item.get("question", "")).strip(),
            "options": [str(x).strip() for x in options],
            "answer": str(answer).strip(),
        })
    return {"questions": validated}
