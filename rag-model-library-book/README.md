# RAG Model — Library Book Recommender

A personalized book recommender that uses your reading history to find new books you'll love. It embeds your past reads into a vector store, pulls candidates from the Open Library API by subject, re-ranks them by semantic similarity, and uses Claude to write a short explanation for each recommendation.

## Concepts Covered

- Semantic similarity search with ChromaDB + HuggingFace embeddings (runs locally, no API key)
- Candidate sourcing from a public API (Open Library)
- Two-stage ranking: vector similarity then LLM re-rank
- Parallel API calls with `ThreadPoolExecutor`

## Stack

| Role | Library |
|------|---------|
| LLM | Claude via `langchain-anthropic` |
| Embeddings | `all-MiniLM-L6-v2` via `langchain-huggingface` (local) |
| Vector store | ChromaDB (persisted to `./chroma_db/`) |
| Candidate source | Open Library Subjects API (no key needed) |

## Setup

> Requires [pyenv](https://github.com/pyenv/pyenv). See the root [README](../README.md) for installation instructions.

```bash
pyenv version          # should show 3.12.4
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY, ANTHROPIC_MODEL, HF_EMBEDDING_MODEL
```

Copy `reading_history.example.json` to `reading_history.json` and replace the entries with books you've actually read:

```bash
cp reading_history.example.json reading_history.json
# edit reading_history.json with your own books
```

Each entry requires `title`, `author`, `description`, and `subjects`. Set `description` to `null` to have Open Library fetch it automatically.

## Run

```bash
python main.py
```

On first run, `main.py` indexes your reading history into ChromaDB, then fetches candidates from Open Library, ranks them, and prints the top recommendations with NYPL links. Subsequent runs skip books already in the index — just add new entries to `reading_history.json` and re-run.

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.

## TODO

- **Candidate caching** — cache the fully-fetched candidate list (title, description, subjects) in Redis with a configurable TTL so repeat runs skip the slow Open Library fetches. Cache key = hash of top subjects.
- **UI — reading history input** — web UI where user enters a book title, Sonnet returns a list of authors to select from, then auto-populates the full reading history entry (description, subjects) via Claude.
- **Google Books API key** — add a key to improve the fallback hit rate for books Open Library doesn't have.
