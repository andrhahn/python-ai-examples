# rag-model-library-book

RAG pipeline scoped to books/PDFs — ingest long-form text, chunk it, and answer questions about the content.

## Entry Points
- `ingest.py` — loads books from `data/`, chunks, embeds, stores in ChromaDB. Skips if store already populated; delete `chroma_db/` to re-ingest.
- `main.py` — conversational Q&A over the ingested books. Exits early with a message if store is empty.

## Stack
- LLM: `ChatAnthropic` (claude-sonnet-4-6)
- Embeddings: `HuggingFaceEmbeddings` with `all-MiniLM-L6-v2` — runs locally, no API key needed
- Vector store: ChromaDB persisted to `./chroma_db/`
- Chain: `RetrievalQA` from `langchain-classic` (moved out of core `langchain` in 1.x)

## Env Vars
- `ANTHROPIC_API_KEY`

## Source Data
Place `.txt` or `.pdf` files in `data/` before running `ingest.py`. A sample excerpt from Pride and Prejudice is included.

## Run
```bash
source .venv/bin/activate
pip install -r requirements.txt
python ingest.py   # run once per new book
python main.py
```

## Gotchas
- `numpy<2` pinned — torch 2.2.x was compiled against NumPy 1.x
- `sentence-transformers<3.0` — 3.x requires PyTorch >= 2.4
- Use `langchain_classic.chains` not `langchain.chains` — RetrievalQA moved in langchain 1.x
