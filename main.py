import os
from config import Config
from utils.pdf_processing import process_pdfs
from utils.file_operations import setup_directories

def main():
    """Main entry point of the application."""
    print("Welcome to pdfProfessor!")
    print("Generate summaries and flashcards from PDF slides in bulk using the ChatGPT API.")
    print("Built for university students.")
    print()

    config = Config()

    directory = input("Enter the directory containing the PDF files: ")
    chunks_directory, output_directory = setup_directories(directory)

    print("\nWhat would you like to do?")
    print("1. Summarize text")
    print("2. Create flashcards")
    print("3. Summarize text and create flashcards")
    choice = input("Enter your choice (1, 2, or 3): ")
    print()

    process_pdfs(directory, chunks_directory, output_directory, config.api_key, choice)

if __name__ == "__main__":
    main()
