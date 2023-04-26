from pdf_to_text import pdf_to_formatted_text
import summarise_text
import flashcard_text

def main():
    api_key = input("Enter your OpenAI API key: ")

    directory = input('Enter the directory containing the PDF files: ')

    # Extract and format text from the PDF files
    output_file_path = pdf_to_formatted_text(directory)

    # Read the formatted text from the output file
    with open(output_file_path, 'r', encoding='utf-8') as file:
        formatted_text = file.read()

    # Ask the user what they want to do with the extracted text
    print("\nWhat would you like to do?")
    print("1. Summarise text")
    print("2. Create flashcards")
    print("3. Summarise text and create flashcards")
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1' or choice == '3':
        # Summarise the formatted text using ChatGPT API
        summary = summarise_text.chat_gpt_summarise(api_key, formatted_text)

        # Save the summary to a new file
        summary_file_path = os.path.join(directory, 'summary.txt')
        with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
            summary_file.write(summary)

        print(f'Summary generated and saved to {summary_file_path}')

    if choice == '2' or choice == '3':
        # Generate flashcards using ChatGPT API
        flashcards = flashcard_text.chat_gpt_flashcards(api_key, formatted_text)

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
