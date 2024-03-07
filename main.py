import os
import csv
import openai
import PyPDF2
from PyPDF2.errors import PdfReadError

def pdf_to_formatted_text(pdf_file_path, max_tokens=2000):
    # Extract text from PDF
    with open(pdf_file_path, 'rb') as pdf_file:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        except PdfReadError:
            print(f"Error: Could not read the PDF file: {pdf_file_path}. It might be encrypted or corrupted.")
            return None

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        formatted_text = text.replace('\n', ' ').replace('  ', ' ')
        return formatted_text

def split_into_chunks(text, max_tokens=2000):
    # Split text into chunks
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def chat_gpt_summarise(api_key, text):
    # Generate summary using ChatGPT
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
    # Generate flashcards using ChatGPT API
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

def main():
    # Main function to run program
    api_key = input("Enter your OpenAI API key: ")
    directory = input('Enter the directory containing the PDF files: ')

    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    summaries_directory = os.path.join(directory, 'summaries')
    flashcards_directory = os.path.join(directory, 'flashcards')
    os.makedirs(summaries_directory, exist_ok=True)
    os.makedirs(flashcards_directory, exist_ok=True)

    print("What would you like to do?")
    print("1. Summarise text")
    print("2. Create flashcards")
    print("3. Summarise text and create flashcards")
    choice = input("Enter your choice (1, 2, or 3): ")

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(directory, pdf_file)
        formatted_text = pdf_to_formatted_text(pdf_file_path)

        if formatted_text:
            chunks = split_into_chunks(formatted_text)

            for i, chunk in enumerate(chunks):
                if choice == '1' or choice == '3':
                    summary = chat_gpt_summarise(api_key, chunk)
                    summary_file_path = os.path.join(summaries_directory, f'summary_{pdf_file[:-4]}_chunk_{i}.txt')
                    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                        summary_file.write(summary)
                    print(f'Summary generated and saved to {summary_file_path}')

                if choice == '2' or choice == '3':
                    flashcards = generate_flashcards(api_key, chunk)
                    flashcard_file_path = os.path.join(flashcards_directory, f'flashcards_{pdf_file[:-4]}_chunk_{i}.csv')
                    with open(flashcard_file_path, 'w', encoding='utf-8', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(['Front', 'Back'])
                        for flashcard in flashcards:
                            front, back = flashcard.split(':', 1)
                            csvwriter.writerow([front.strip(), back.strip()])
                    print(f'Flashcards generated and saved to {flashcard_file_path}')

if __name__ == "__main__":
    main()
