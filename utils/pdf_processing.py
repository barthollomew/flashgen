import csv
import logging
import os
from typing import List

from openai import OpenAI
from tqdm.auto import tqdm

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
    model: str,
    temperature: float,
    flashcard_limit: int,
    chunk_tokens: int,
    chunk_overlap: int,
    encoding_name: str = "o200k_base",
) -> None:
    """Process PDF files to generate summaries and/or flashcards."""
    pdf_files = [
        file
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file)) and file.lower().endswith(".pdf")
    ]
    pdf_files.sort()

    if not pdf_files:
        logging.info("No PDF files found in %s", directory)
        return

    summaries: List[str] = []
    flashcards: List[dict] = []

    for pdf_file in tqdm(pdf_files, desc="PDFs", unit="pdf"):
        pdf_file_path = os.path.join(directory, pdf_file)
        formatted_text = pdf_to_formatted_text(pdf_file_path)

        if not formatted_text:
            continue

        chunks = split_into_chunks(
            formatted_text, max_tokens=chunk_tokens, overlap_tokens=chunk_overlap, encoding_name=encoding_name
        )

        pdf_summaries: List[str] = []
        pdf_flashcards: List[dict] = []

        for i, chunk in tqdm(enumerate(chunks), total=len(chunks), desc=f"{pdf_file} chunks", leave=False):
            if choice in ["1", "3"]:
                try:
                    summary = chat_gpt_summarize(client, chunk, model=model, temperature=temperature)
                    write_summary(chunks_directory, pdf_file, i, summary)
                    pdf_summaries.append(summary)
                except Exception as exc:  # noqa: BLE001
                    logging.error("Failed to summarize %s chunk %s: %s", pdf_file, i, exc)

            if choice in ["2", "3"]:
                try:
                    chunk_flashcards = generate_flashcards(
                        client, chunk, model=model, limit=flashcard_limit, temperature=temperature
                    )
                    write_flashcards(chunks_directory, pdf_file, i, chunk_flashcards)
                    flashcards.extend(chunk_flashcards)
                    pdf_flashcards.extend(chunk_flashcards)
                except Exception as exc:  # noqa: BLE001
                    logging.error("Failed to create flashcards for %s chunk %s: %s", pdf_file, i, exc)

        # Per-PDF rollups
        pdf_stem = os.path.splitext(pdf_file)[0]

        if choice in ["1", "3"] and pdf_summaries:
            pdf_summary_path = os.path.join(output_directory, f"{pdf_stem}_summary.txt")
            refined_summary = "\n\n".join(pdf_summaries)
            try:
                refined_summary = chat_gpt_summarize(
                    client,
                    refined_summary,
                    model=model,
                    temperature=max(0.1, temperature - 0.05),  # slightly more deterministic on the rollup
                    max_tokens=420,
                )
            except Exception as exc:  # noqa: BLE001
                logging.error("Failed to refine summary for %s: %s", pdf_file, exc)
            with open(pdf_summary_path, "w", encoding="utf-8") as summary_file:
                summary_file.write(refined_summary)
            summaries.append(refined_summary)

        if choice in ["2", "3"] and pdf_flashcards:
            pdf_flashcards_path = os.path.join(output_directory, f"{pdf_stem}_flashcards.csv")
            with open(pdf_flashcards_path, "w", encoding="utf-8", newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Front", "Back"])
                for flashcard in pdf_flashcards:
                    csvwriter.writerow([flashcard["front"].strip(), flashcard["back"].strip()])

    if choice in ["1", "3"] and summaries:
        combined_summary_path = os.path.join(output_directory, "combined_summary.txt")
        with open(combined_summary_path, "w", encoding="utf-8") as summary_file:
            summary_file.write("\n\n".join(summaries))
        logging.info("Combined summary saved to %s", combined_summary_path)

    if choice in ["2", "3"] and flashcards:
        combined_flashcards_path = os.path.join(output_directory, "combined_flashcards.csv")
        with open(combined_flashcards_path, "w", encoding="utf-8", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Front", "Back"])
            for flashcard in flashcards:
                csvwriter.writerow([flashcard["front"].strip(), flashcard["back"].strip()])
        logging.info("Combined flashcards saved to %s", combined_flashcards_path)
