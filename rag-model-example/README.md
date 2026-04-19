# RAG Model Example

A basic Retrieval-Augmented Generation (RAG) pipeline: ingest documents, embed them, store in a vector DB, and answer questions grounded in the retrieved context.

## Concepts Covered

- Document loading and chunking
- Generating and storing embeddings
- Similarity search / retrieval
- Grounded generation with retrieved context

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
# edit .env and set OPENAI_API_KEY (used for embeddings)
```

## Run

```bash
# Step 1: ingest documents into the vector store
python ingest.py

# Step 2: query the RAG pipeline
python main.py
```

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.
