# summarize_text.py
import openai
import os
from pdf_to_text import pdf_to_formatted_text

def chat_gpt_summarize(api_key, text):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please summarize the following text and make it easier to understand:\n{text}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

def main():
    directory = input('Enter the directory containing the PDF files: ')

    # Extract and format text from the PDF files
    output_file_path = pdf_to_formatted_text(directory)

    # Read the formatted text from the output file
    with open(output_file_path, 'r', encoding='utf-8') as file:
        formatted_text = file.read()

    # Summarize the formatted text using ChatGPT API
    api_key = "YOUR_API_KEY"
    summary = chat_gpt_summarize(api_key, formatted_text)

    # Save the summary to a new file
    summary_file_path = os.path.join(directory, 'summary.txt')
    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(summary)

    print(f'Summary generated and saved to {summary_file_path}')

if __name__ == "__main__":
    main()
