# 📚 PDF PowerPoint Slides Summarizer 📝

This project extracts text from multiple PowerPoint slides saved as PDF files, formats the text, and then generates a summary using OpenAI's ChatGPT API. It helps you get a quick overview of the contents of the slides.

## 🚀 Getting Started

### 📋 Prerequisites

1. Python 3.6 or higher
2. `PyPDF2` library
3. `openai` library

You can install the required libraries using pip:

```bash
pip install PyPDF2 openai
```

### 🔑 API Key
IMPORTANT: To use ChatGPT, you'll need an API key from OpenAI. Sign up for an account at https://beta.openai.com/signup/ to obtain your API key. Replace YOUR_API_KEY in summarize_text.py with your actual API key.

### 📁 How to Use
1. Place your PDF files (PowerPoint slides) in a directory.
2. Run summarize_text.py
3. Enter the directory containing the PDF files when prompted.
4. The script will extract and format the text from the PDF files, save it to output.txt, generate a summary using ChatGPT, and save the summary to summary.txt.
