import json
from typing import Dict, List

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"


def get_client(api_key: str) -> OpenAI:
    """Create a reusable OpenAI client instance."""
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)


def chat_gpt_summarize(
    client: OpenAI,
    text: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.35,
    max_tokens: int = 360,
) -> str:
    """Generate a concise summary for the provided text."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize technical lecture slides into short, clear study notes for university students. "
                    "Favor bullet points, key terms, and important relationships. Avoid filler."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Summarize the following content into <=8 bullets. "
                    "Highlight definitions, formulas, and cause/effect if present.\n\n"
                    f"{text}"
                ),
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        presence_penalty=0.0,
        frequency_penalty=0.1,
    )
    return completion.choices[0].message.content.strip()


def _parse_flashcard_lines(raw_text: str) -> List[Dict[str, str]]:
    cards: List[Dict[str, str]] = []
    for line in raw_text.splitlines():
        if ":" in line:
            front, back = line.split(":", 1)
            if front.strip() and back.strip():
                cards.append({"front": front.strip(), "back": back.strip()})
    return cards


def generate_flashcards(
    client: OpenAI,
    text: str,
    model: str = DEFAULT_MODEL,
    limit: int = 10,
    temperature: float = 0.35,
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
        temperature=temperature,
        max_tokens=900,
        response_format={"type": "json_object"},
    )

    message_content = completion.choices[0].message.content

    try:
        payload = json.loads(message_content)
        flashcards = payload.get("flashcards", [])
        parsed = [card for card in flashcards if "front" in card and "back" in card]
        if parsed:
            return parsed
    except json.JSONDecodeError:
        pass

    # Fall back to parsing plain text lines with "front: back"
    return _parse_flashcard_lines(message_content)
