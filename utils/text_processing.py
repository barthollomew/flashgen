import PyPDF2
from PyPDF2.errors import PdfReadError

def pdf_to_formatted_text(pdf_file_path, max_tokens=2000):
    """Extract text from a PDF and format it."""
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            formatted_text = text.replace('\n', ' ').replace('  ', ' ')
            return formatted_text
    except PdfReadError:
        print(f"Error: Could not read the PDF file: {pdf_file_path}. It might be encrypted or corrupted.")
        return None

def split_into_chunks(text, max_tokens=2000):
    """Split text into chunks that are under max_tokens."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
