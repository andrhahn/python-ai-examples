# RAG Model Example

A basic Retrieval-Augmented Generation (RAG) pipeline: load documents, embed them, store in a vector DB, and answer questions grounded in the retrieved context.

## Concepts Covered

- Document loading and chunking
- Generating and storing embeddings
- Similarity search / retrieval
- Grounded generation with retrieved context

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

## Run

```bash
python main.py
```

On first run, `main.py` automatically ingests documents from `./docs/` into ChromaDB. Subsequent runs detect the populated store and skip ingestion.

To re-ingest (e.g. after adding new docs):

```bash
rm -rf chroma_db/
python main.py
```

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.