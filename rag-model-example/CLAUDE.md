# rag-model-example

Demonstrates a basic RAG pipeline: ingest docs → embed → store in vector DB → retrieve → generate.

## Entry Points
- `ingest.py` — loads documents, generates embeddings, stores in ChromaDB
- `main.py` — accepts a query, retrieves context, generates a grounded answer

## Env Vars
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY` (used for embeddings)

## Run
```bash
source .venv/bin/activate
python ingest.py   # run once to build the vector store
python main.py
```
