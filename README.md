## FlashGen

FlashGen is a command-line tool that turns PDF slide decks into concise summaries and flashcards using the latest ChatGPT API (gpt-4o-mini). It is built for students who need quick study material from large batches of slides.

### Features
- **Bulk PDF Processing**: Process multiple PDFs in a single directory to generate summaries and flashcards.
- **Customizable Output**: Choose between generating summaries, flashcards, or both.
- **Intelligent Chunking**: Automatically splits PDF content into manageable chunks for more effective summarization and flashcard generation.
- **Easy CLI Interface**: Simple command-line interface powered by Click for ease of use.
- **Structured Flashcards**: Uses JSON-mode Chat Completions for reliable `Front`/`Back` cards.

### Usage

#### Setup
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI key:
   ```bash
   setx OPENAI_API_KEY "sk-..."
   # Or export OPENAI_API_KEY=... on macOS/Linux
   ```

#### Running the Tool
Place your PDF files in a directory, then run:

```bash
python main.py --directory /path/to/pdf/files --choice 3
```

#### Command-line Options
- `--directory`: Path to the directory containing the PDF files.
- `--choice`: Operation mode (1: Summarize text, 2: Create flashcards, 3: Summarize text and create flashcards).

### Example
```bash
python main.py --directory /path/to/pdf/files --choice 3
```
This command will generate both summaries and flashcards for all PDF files in the specified directory.
