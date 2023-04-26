import openai
import os
import PyPDF2

def generate_flashcards(api_key, pdf_file_path):

    # Initialize the OpenAI API
    openai.api_key = api_key

    # Read the text file
    with open(pdf_file_path, 'r', encoding='utf-8') as text_file:
        text = text_file.read()

    # Call the OpenAI API to generate flashcards
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create flashcards for the following text:\n{text}\n\nFlashcards:",
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Process the API response
    flashcards_raw = response.choices[0].text.strip()
    flashcards = flashcards_raw.split("\n")

    return flashcards
