# rag-model-library-book

RAG pipeline scoped to books/PDFs — ingest long-form text, chunk it, and answer questions about the content.

## Entry Points
- `ingest.py` — loads books from `data/`, chunks, embeds, stores in ChromaDB
- `main.py` — conversational Q&A over the ingested books

## Env Vars
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY` (used for embeddings)

## Source Data
Place `.txt` or `.pdf` files in the `data/` directory before running `ingest.py`.

## Run
```bash
source .venv/bin/activate
python ingest.py   # run once per new book
python main.py
```
