import openai

def chat_gpt_summarize(api_key, text):
    """Generate summary using ChatGPT."""
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a concise summary of the following text:\n\n{text}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

def generate_flashcards(api_key, text):
    """Generate flashcards using ChatGPT API."""
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create flashcards for the following text:\n{text}\n\nFlashcards:",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    flashcards_raw = response.choices[0].text.strip()
    flashcards = [flashcard.strip() for flashcard in flashcards_raw.split("\n") if flashcard.strip()]
    return flashcards
