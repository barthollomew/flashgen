import openai
import textwrap
from pdf_to_text import pdf_to_formatted_text

def chat_gpt_summarise(api_key, text):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please provide a concise summary of the following text:\n\n{text}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary

def summarise_pdf(api_key, pdf_file_path):
    formatted_text = pdf_to_formatted_text(pdf_file_path)
    summary = chat_gpt_summarise(api_key, formatted_text)
    wrapped_summary = textwrap.fill(summary, width=80)
    return wrapped_summary
