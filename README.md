# 📚 Mega PDF Extractor: Insane study hack for uni students 📚

Instantly generate summaries and flashcards from PDF files using ChatGPT. Program that has helped me insanely in crunching large amounts of info quickly for revision.

## 🚀 Getting Started

### Install the required libraries using pip:

```Python
pip install PyPDF2 openai
```

### 🔑 API Key
IMPORTANT: To use ChatGPT, you'll need an API key from OpenAI. Replace YOUR_API_KEY in summarize_text.py with your actual API key. Sign up for an account at https://beta.openai.com/signup/ to obtain your API key. 


```bash

How to use:

1. Place the PDF files (PowerPoint/lecture slides) you want to extract text from in a directory, e.g., pdf_files.
2. Open your terminal or command prompt and navigate to the folder containing the Python scripts
3. Run using main.py
4. Enter your OpenAI API key and the directory containing PDF files to process.
5. Choose an option: summarize text, create flashcards, or do both. 
  - If summarizing, call chat_gpt_summarise to generate summaries using the OpenAI API and save them in the 'summaries' directory.
  - If creating flashcards, call generate_flashcards to generate flashcards using the OpenAI API and save them as CSV files in the 'flashcards' directory.
  - If doing both, program first summarize the text, and then generates the flashcards from the summaries.
6. Win!!!

```

