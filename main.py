import os
import csv
from pdf_to_text import pdf_to_formatted_text
import summarise_text
import flashcard_text

# To do: 
# - Write function that goes through flashcards folder and deletes all empty ones containing just front back
# - Write function that goes through summaries folder and deletes all empty ones containing just summary and combines them all into one.

def main():
    api_key = input("Enter your OpenAI API key: ")

    directory = input('Enter the directory containing the PDF files: ')

    # Extract and format text from the PDF files
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    # Create directories to store the split text files, summaries, and flashcards
    split_directory = os.path.join(directory, 'split')
    summaries_directory = os.path.join(directory, 'summaries')
    flashcards_directory = os.path.join(directory, 'flashcards')
    os.makedirs(split_directory, exist_ok=True)
    os.makedirs(summaries_directory, exist_ok=True)
    os.makedirs(flashcards_directory, exist_ok=True)

    print("Preparing files...")
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(directory, pdf_file)
        pdf_to_formatted_text(pdf_file_path, split_directory)

    # Ask the user what they want to do with the extracted text
    print("\nWhat would you like to do?")
    print("1. Summarise text")
    print("2. Create flashcards")
    print("3. Summarise text and create flashcards")
    choice = input("Enter your choice (1, 2, or 3): ")

    for chunk_file_name in os.listdir(split_directory):
        if not chunk_file_name.endswith('.txt'):
            continue

        chunk_file_path = os.path.join(split_directory, chunk_file_name)

        if choice == '1' or choice == '3':
            with open(chunk_file_path, 'r', encoding='utf-8') as chunk_file:
                chunk = chunk_file.read()

            summary = summarise_text.chat_gpt_summarise(api_key, chunk)
            summary_file_path = os.path.join(summaries_directory, f'summary_{chunk_file_name}')

            with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                summary_file.write(summary)

            print(f'Summary generated and saved to {summary_file_path}')

        if choice == '2' or choice == '3':
            if choice == '3':
                chunk_file_path = summary_file_path

            flashcards = flashcard_text.generate_flashcards(api_key, chunk_file_path)
            flashcard_file_path = os.path.join(flashcards_directory, f'flashcards_{chunk_file_name[:-4]}.csv')

            with open(flashcard_file_path, 'w', encoding='utf-8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(['Front', 'Back'])  # Headers for Anki import

                for flashcard in flashcards:
                    if ':' not in flashcard:
                        continue
                    front, back = flashcard.split(':', 1)
                    csvwriter.writerow([front.strip(), back.strip()])

            print(f'Flashcards generated and saved to {flashcard_file_path}')


if __name__ == "__main__":
    main()
