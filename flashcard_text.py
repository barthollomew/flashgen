# flashcard_text.py
import openai
import os
import csv
from pdf_to_text import pdf_to_formatted_text

def chat_gpt_flashcards(api_key, text):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please create flashcards from the following text:\n{text}",
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.5,
    )

    flashcards = response.choices[0].text.strip().split('\n')
    return flashcards

def main():
    directory = input('Enter the directory containing the PDF files: ')

    # Extract and format text from the PDF files
    output_file_path = pdf_to_formatted_text(directory)

    # Read the formatted text from the output file
    with open(output_file_path, 'r', encoding='utf-8') as file:
        formatted_text = file.read()

    # Generate flashcards using ChatGPT API
    api_key = input("Enter your OpenAI API key: ")
    flashcards = chat_gpt_flashcards(api_key, formatted_text)

    # Save the flashcards to a CSV file
    flashcard_file_path = os.path.join(directory, 'flashcards.csv')
    with open(flashcard_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Front', 'Back'])  # Headers for Anki import

        for flashcard in flashcards:
            front, back = flashcard.split(':', 1)
            csvwriter.writerow([front.strip(), back.strip()])

    print(f'Flashcards generated and saved to {flashcard_file_path}')

if __name__ == "__main__":
    main()
