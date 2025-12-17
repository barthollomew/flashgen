## FlashGen

FlashGen is a command-line tool that turns PDF slide decks into concise summaries and flashcards using the latest ChatGPT API (gpt-4o-mini by default). It is built for students who need quick study material from large batches of slides.

### Features
- **Bulk PDF Processing**: Process multiple PDFs in a single directory to generate summaries and flashcards.
- **Customizable Output**: Choose between generating summaries, flashcards, or both.
- **Intelligent Chunking**: Automatically splits PDF content into manageable chunks for more effective summarization and flashcard generation.
- **Token-aware chunking**: Uses `tiktoken` to keep requests within model limits with configurable overlap.
- **Structured Flashcards**: Uses JSON-mode Chat Completions with a text fallback for reliable `Front`/`Back` cards.
- **Per-PDF and combined outputs**: Chunk-level files plus per-PDF rollups and combined CSV/TXT across the entire batch.
- **Easy CLI Interface**: Simple command-line interface powered by Click with model/temperature/chunk-size knobs.

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
- `--directory`: Path to the directory containing the PDF files (required).
- `--choice`: Operation mode (1: Summaries, 2: Flashcards, 3: Both).
- `--model`: OpenAI model name (defaults to `OPENAI_MODEL` env var or `gpt-4o-mini`).
- `--temperature`: Sampling temperature for both summaries and flashcards.
- `--flashcard-limit`: Max cards per chunk.
- `--chunk-tokens`: Approximate tokens per chunk for splitting.
- `--chunk-overlap`: Token overlap between consecutive chunks.

### Example
```bash
python main.py --directory /path/to/pdf/files --choice 3
```
This command will generate both summaries and flashcards for all PDF files in the specified directory.

### Outputs
- Chunk-level files are stored beside your PDFs under `chunks/`.
- Per-PDF rollups live in `output/<pdf_name>_summary.txt` and `output/<pdf_name>_flashcards.csv`.
- Combined batch outputs are `output/combined_summary.txt` and `output/combined_flashcards.csv`.
