import PyPDF2
import os
import re

def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

def format_text(text):
    # Remove excessive whitespaces and line breaks
    formatted_text = re.sub(r'\s{2,}', ' ', text)
    formatted_text = re.sub(r'\n{2,}', '\n', formatted_text)
    return formatted_text.strip()

def main():
    directory = input('Enter the directory containing the PDF files: ')

    # Collect all the PDF files in the given directory
    pdf_files = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    # Create and open the output text file
    output_file_path = os.path.join(directory, 'output.txt')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for pdf_file in pdf_files:
            pdf_file_path = os.path.join(directory, pdf_file)
            text = extract_text_from_pdf(pdf_file_path)
            formatted_text = format_text(text)
            
            # Write the formatted text to the output file
            output_file.write(f'--- {pdf_file} ---\n{formatted_text}\n\n')

    print(f'Formatted text from all PDF files has been extracted and saved to {output_file_path}')

if __name__ == "__main__":
    main()
