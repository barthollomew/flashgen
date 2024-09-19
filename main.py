import click
from config import Config
from utils.pdf_processing import process_pdfs
from utils.file_operations import setup_directories

@click.command()
@click.option('--directory', prompt='PDF directory', help='The directory containing the PDF files.')
@click.option('--choice', type=click.Choice(['1', '2', '3']), prompt='Your choice',
              help='1: Summarize text, 2: Create flashcards, 3: Summarize text and create flashcards.')
def main(directory, choice):
    """
    Main entry point of the application.
    
    Args:
        directory (str): The directory containing the PDF files.
        choice (str): The operation choice: '1' for summarizing, '2' for flashcards, '3' for both.
    """
    print("Welcome to pdfProfessor!")
    print("Generate summaries and flashcards from PDF slides in bulk using the ChatGPT API.")
    print("Built for university students.")
    print()

    config = Config()

    chunks_directory, output_directory = setup_directories(directory)

    process_pdfs(directory, chunks_directory, output_directory, config.api_key, choice)

if __name__ == "__main__":
    main()
