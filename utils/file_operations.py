import os
import csv

def setup_directories(directory):
    """Set up directories for chunks and output."""
    chunks_directory = os.path.join(directory, 'chunks')
    output_directory = os.path.join(directory, 'output')
    os.makedirs(chunks_directory, exist_ok=True)
    os.makedirs(output_directory, exist_ok=True)
    return chunks_directory, output_directory

def write_summary(chunks_directory, pdf_file, chunk_index, summary):
    """Write summary to a file."""
    summary_file_path = os.path.join(chunks_directory, f'summary_{pdf_file[:-4]}_chunk_{chunk_index}.txt')
    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(summary)
    print(f"Summary generated and saved to {summary_file_path}")

def write_flashcards(chunks_directory, pdf_file, chunk_index, flashcards):
    """Write flashcards to a CSV file."""
    flashcard_file_path = os.path.join(chunks_directory, f'flashcards_{pdf_file[:-4]}_chunk_{chunk_index}.csv')
    with open(flashcard_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Front', 'Back'])
        for flashcard in flashcards:
            front, back = flashcard.split(':', 1)
            csvwriter.writerow([front.strip(), back.strip()])
    print(f"Flashcards generated and saved to {flashcard_file_path}")
