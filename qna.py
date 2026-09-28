from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")

    prompt = f"""You are EduGenie, an accurate educational question-answering assistant.
Answer this student's question:
{question}

Requirements:
- Give the direct answer first.
- Then briefly explain the reasoning or context.
- Use beginner-friendly language.
- If the question is ambiguous, state the assumption you used.
- If you are uncertain, say so rather than inventing information.
"""
    return generate_text(prompt, temperature=0.25, max_output_tokens=900)
