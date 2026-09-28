from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic for the learning path.")

    prompt = f"""Create a personalized learning path for: {topic}

Organize it as:
1. Beginner foundations
2. Intermediate concepts
3. Advanced concepts
4. Suggested practice/projects
5. Suggested resources (resource type and what to look for; do not invent exact URLs)
6. A realistic 7-day starter plan

Keep the language simple. Explain why each stage comes next. The plan should be useful to a learner starting from limited background knowledge.
"""
    return generate_text(prompt, temperature=0.45, max_output_tokens=1600)
