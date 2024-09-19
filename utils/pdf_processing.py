import os
import logging
from utils.openai_api import chat_gpt_summarize, generate_flashcards
from utils.file_operations import write_summary, write_flashcards
from utils.text_processing import pdf_to_formatted_text, split_into_chunks

logging.basicConfig(level=logging.INFO)

def process_pdfs(directory, chunks_directory, output_directory, api_key, choice):
    """Process PDF files to generate summaries and/or flashcards."""
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]
    
    summaries = []
    flashcards = []

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(directory, pdf_file)
        formatted_text = pdf_to_formatted_text(pdf_file_path)

        if formatted_text:
            chunks = split_into_chunks(formatted_text)

            for i, chunk in enumerate(chunks):
                if choice in ['1', '3']:
                    summary = chat_gpt_summarize(api_key, chunk)
                    write_summary(chunks_directory, pdf_file, i, summary)
                    summaries.append(summary)
                
                if choice in ['2', '3']:
                    chunk_flashcards = generate_flashcards(api_key, chunk)
                    write_flashcards(chunks_directory, pdf_file, i, chunk_flashcards)
                    flashcards.extend(chunk_flashcards)
    
    if choice in ['1', '3']:
        combined_summary_path = os.path.join(output_directory, 'combined_summary.txt')
        with open(combined_summary_path, 'w', encoding='utf-8') as summary_file:
            summary_file.write('\n\n'.join(summaries))
        logging.info(f"Combined summary saved to {combined_summary_path}")

    if choice in ['2', '3']:
        combined_flashcards_path = os.path.join(output_directory, 'combined_flashcards.csv')
        with open(combined_flashcards_path, 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Front', 'Back'])
            for flashcard in flashcards:
                front, back = flashcard.split(':', 1)
                csvwriter.writerow([front.strip(), back.strip()])
        logging.info(f"Combined flashcards saved to {combined_flashcards_path}")
