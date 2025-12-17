import csv
import logging
import os
from typing import List

from openai import OpenAI

from utils.openai_api import chat_gpt_summarize, generate_flashcards
from utils.file_operations import write_flashcards, write_summary
from utils.text_processing import pdf_to_formatted_text, split_into_chunks

logging.basicConfig(level=logging.INFO)


def process_pdfs(
    directory: str,
    chunks_directory: str,
    output_directory: str,
    client: OpenAI,
    choice: str,
) -> None:
    """Process PDF files to generate summaries and/or flashcards."""
    pdf_files = [file for file in os.listdir(directory) if file.endswith(".pdf")]

    if not pdf_files:
        logging.info("No PDF files found in %s", directory)
        return

    summaries: List[str] = []
    flashcards: List[dict] = []

    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(directory, pdf_file)
        formatted_text = pdf_to_formatted_text(pdf_file_path)

        if formatted_text:
            chunks = split_into_chunks(formatted_text)

            for i, chunk in enumerate(chunks):
                if choice in ['1', '3']:
                    try:
                        summary = chat_gpt_summarize(client, chunk)
                        write_summary(chunks_directory, pdf_file, i, summary)
                        summaries.append(summary)
                    except Exception as exc:  # noqa: BLE001
                        logging.error("Failed to summarize %s chunk %s: %s", pdf_file, i, exc)
                
                if choice in ['2', '3']:
                    try:
                        chunk_flashcards = generate_flashcards(client, chunk)
                        write_flashcards(chunks_directory, pdf_file, i, chunk_flashcards)
                        flashcards.extend(chunk_flashcards)
                    except Exception as exc:  # noqa: BLE001
                        logging.error("Failed to create flashcards for %s chunk %s: %s", pdf_file, i, exc)
    
    if choice in ['1', '3']:
        combined_summary_path = os.path.join(output_directory, "combined_summary.txt")
        with open(combined_summary_path, "w", encoding="utf-8") as summary_file:
            summary_file.write("\n\n".join(summaries))
        logging.info("Combined summary saved to %s", combined_summary_path)

    if choice in ['2', '3']:
        combined_flashcards_path = os.path.join(output_directory, "combined_flashcards.csv")
        with open(combined_flashcards_path, "w", encoding="utf-8", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Front", "Back"])
            for flashcard in flashcards:
                csvwriter.writerow([flashcard["front"].strip(), flashcard["back"].strip()])
        logging.info("Combined flashcards saved to %s", combined_flashcards_path)
