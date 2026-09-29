from config import EXPLANATION_BACKEND
from gemini_client import generate_text


def _gemini_explain(topic: str) -> str:
    prompt = f"""You are EduGenie, a friendly educational tutor.
Explain the following topic to a beginner.
Topic: {topic}

Rules:
- Start with a one-sentence definition.
- Explain how/why it works in simple language.
- Use short sections and bullet points.
- Include one simple real-life analogy.
- Avoid unnecessary jargon.
- Do not invent facts.
"""
    return generate_text(prompt, temperature=0.35, max_output_tokens=1000)


def _local_explain(topic: str) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode needs the optional packages in requirements-local.txt. "
            "Either install them or set EXPLANATION_BACKEND=gemini."
        ) from exc

    generator = pipeline("text2text-generation", model="MBZUAI/LaMini-Flan-T5-783M")
    result = generator(
        f"Explain {topic} to a beginner in simple language with short bullet points.",
        max_new_tokens=300,
    )
    return result[0]["generated_text"]


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic to explain.")
    if EXPLANATION_BACKEND == "local":
        try:
            return _local_explain(topic)
        except Exception:
            # Cloud Gemini remains the reliable fallback for local-model failures.
            return _gemini_explain(topic)
    return _gemini_explain(topic)
