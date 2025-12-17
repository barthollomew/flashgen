import os

import click

from config import Config
from utils.file_operations import setup_directories
from utils.pdf_processing import process_pdfs

@click.command()
@click.option('--directory', prompt='PDF directory', help='The directory containing the PDF files.')
@click.option('--choice', type=click.Choice(['1', '2', '3']), prompt='Your choice',
              help='1: Summarize text, 2: Create flashcards, 3: Summarize text and create flashcards.')
@click.option('--model', default=None, show_default=True, help='OpenAI model to use (default: env OPENAI_MODEL or gpt-4o-mini).')
@click.option('--temperature', default=0.35, show_default=True, help='Sampling temperature for generation.')
@click.option('--flashcard-limit', default=10, show_default=True, help='Max cards per chunk.')
@click.option('--chunk-tokens', default=1400, show_default=True, help='Approximate tokens per chunk.')
@click.option('--chunk-overlap', default=150, show_default=True, help='Token overlap between chunks.')
def main(directory, choice, model, temperature, flashcard_limit, chunk_tokens, chunk_overlap):
    """
    Main entry point of the application.
    
    Args:
        directory (str): The directory containing the PDF files.
        choice (str): The operation choice: '1' for summarizing, '2' for flashcards, '3' for both.
    """
    print("Bulk generate summaries and flashcards from PDF slides using ChatGPT.")
    print("Built for university students.")
    print()

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    config = Config()

    chunks_directory, output_directory = setup_directories(directory)

    process_pdfs(
        directory=directory,
        chunks_directory=chunks_directory,
        output_directory=output_directory,
        client=config.client,
        choice=choice,
        model=model or config.model,
        temperature=temperature,
        flashcard_limit=flashcard_limit,
        chunk_tokens=chunk_tokens,
        chunk_overlap=chunk_overlap,
    )

if __name__ == "__main__":
    main()
