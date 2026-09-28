from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Please provide text to summarize.")

    prompt = f"""Summarize the educational passage below for quick revision.
Keep the core facts and relationships. Remove repetition.
Use a short heading followed by concise bullet points.
Do not add facts that are not in the passage.

PASSAGE:
{text}
"""
    return generate_text(prompt, temperature=0.2, max_output_tokens=1000)
