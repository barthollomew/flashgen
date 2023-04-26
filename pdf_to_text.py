import os
import PyPDF2
from PyPDF2.errors import PdfReadError

def pdf_to_formatted_text(pdf_file_path, directory, max_tokens=2000):
    with open(pdf_file_path, 'rb') as pdf_file:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        except PdfReadError:
            print(f"Error: Could not read the PDF file: {pdf_file_path}. It might be encrypted or corrupted.")
            return

        text = ""
        chunk = ""
        chunk_counter = 0
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
            formatted_text = text.replace('\n', ' ').replace('  ', ' ')
            words = formatted_text.split()

            for word in words:
                word_tokens = len(word)
                if len(chunk) + word_tokens <= max_tokens:
                    chunk += f"{word} "
                else:
                    chunk_file_path = os.path.join(directory, f'{os.path.basename(pdf_file_path)[:-4]}_chunk_{chunk_counter}.txt')
                    with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
                        chunk_file.write(chunk)
                    chunk_counter += 1
                    chunk = f"{word} "
            text = ""

        if chunk:
            chunk_file_path = os.path.join(directory, f'{os.path.basename(pdf_file_path)[:-4]}_chunk_{chunk_counter}.txt')
            with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
                chunk_file.write(chunk)
