import json
from typing import Dict, List

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"


def get_client(api_key: str) -> OpenAI:
    """Create a reusable OpenAI client instance."""
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)


def chat_gpt_summarize(client: OpenAI, text: str, model: str = DEFAULT_MODEL) -> str:
    """Generate a concise summary for the provided text."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You summarize technical lecture slides into short, clear study notes.",
            },
            {
                "role": "user",
                "content": (
                    "Summarize the following content for students. "
                    "Keep it under 8 bullet points and emphasize key concepts and definitions.\n\n"
                    f"{text}"
                ),
            },
        ],
        temperature=0.35,
        max_tokens=320,
    )
    return completion.choices[0].message.content.strip()


def generate_flashcards(
    client: OpenAI, text: str, model: str = DEFAULT_MODEL, limit: int = 10
) -> List[Dict[str, str]]:
    """
    Generate structured flashcards using the Chat Completions API.

    Returns a list of dictionaries with ``front`` and ``back`` keys.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You create clear, factual study flashcards in JSON."},
            {
                "role": "user",
                "content": (
                    f"Create up to {limit} concise Q&A flashcards from the text below. "
                    "Focus on key facts, definitions, formulas, and relationships. "
                    "Return strictly formatted JSON matching this shape:\n"
                    '{"flashcards":[{"front":"question or term","back":"brief answer"}]}\n\n'
                    f"Text:\n{text}"
                ),
            },
        ],
        temperature=0.4,
        max_tokens=900,
        response_format={"type": "json_object"},
    )

    try:
        payload = json.loads(completion.choices[0].message.content)
        flashcards = payload.get("flashcards", [])
        return [card for card in flashcards if "front" in card and "back" in card]
    except json.JSONDecodeError:
        # Fall back to no flashcards when the model fails to return valid JSON.
        return []
