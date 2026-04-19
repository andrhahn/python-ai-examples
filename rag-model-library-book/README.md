# RAG Model — Library Book

A RAG example scoped to a library/book use case: load one or more books (or a catalog), embed them, and answer natural-language questions about their content.

## Concepts Covered

- Ingesting long-form text (books, PDFs)
- Chunking strategies for long documents
- Metadata filtering (author, title, chapter)
- Conversational Q&A over a book corpus

## Stack

| Role | Library |
|------|---------|
| LLM | Claude (claude-sonnet-4-6) via `langchain-anthropic` |
| Embeddings | `all-MiniLM-L6-v2` via `langchain-huggingface` (runs locally) |
| Vector store | ChromaDB (persisted to `./chroma_db/`) |
| Orchestration | LangChain Classic (`RetrievalQA`) |

## Setup

> Requires [pyenv](https://github.com/pyenv/pyenv). See the root [README](../README.md) for installation instructions.

```bash
pyenv version          # should show 3.12.4
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY
```

Place your source book(s) (`.txt` or `.pdf`) in the `data/` directory. A sample excerpt is included to get started.

## Run

```bash
# Step 1: ingest books into the vector store (run once, or after adding new books)
python ingest.py

# Step 2: ask questions about the books
python main.py
```

To re-ingest after adding new books:

```bash
rm -rf chroma_db/
python ingest.py
```

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.
