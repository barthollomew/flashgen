## FlashGen

FlashGen is a powerful, easy-to-use command-line tool designed to help university students generate summaries and flashcards from PDF slides in bulk using the ChatGPT API. Whether you're studying for exams or trying to quickly grasp the key points from lecture slides, Slide-Smart automates the tedious work, allowing you to focus on learning.

### Features
- **Bulk PDF Processing**: Process multiple PDFs in a single directory to generate summaries and flashcards.
- **Customizable Output**: Choose between generating summaries, flashcards, or both.
- **Intelligent Chunking**: Automatically splits PDF content into manageable chunks for more effective summarization and flashcard generation.
- **Easy CLI Interface**: Simple command-line interface powered by Click for ease of use.

### Usage

#### Preparing the PDF Files
Place your PDF files in a directory that you will specify when running the tool.

#### Running the Tool
You can run Slide-Smart from the command line with the following command:

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
