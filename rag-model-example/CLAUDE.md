# rag-model-example

Demonstrates a basic RAG pipeline: ingest docs → embed → store in vector DB → retrieve → generate.

## Entry Points
- `main.py` — ingests docs on first run (if store empty), then retrieves and answers a hardcoded query
- `docs/` — source documents to ingest (plain `.txt` files)

## How ingestion works
`main.py` checks `vectorstore._collection.count() == 0` at startup. If empty, it loads all `.txt` files from `./docs/`, chunks them with `RecursiveCharacterTextSplitter`, and adds them to ChromaDB. To re-ingest, delete `chroma_db/` and rerun.

## Stack
- LLM: `ChatAnthropic` (claude-sonnet-4-6)
- Embeddings: `HuggingFaceEmbeddings` with `all-MiniLM-L6-v2` — runs locally, no API key needed. Requires `sentence-transformers<3.0` due to PyTorch 2.2.x compatibility on this machine.
- Vector store: ChromaDB persisted to `./chroma_db/`
- Chain: `RetrievalQA` from `langchain-classic` (moved out of core `langchain` in 1.x)

## Env Vars
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL` (e.g. `claude-sonnet-4-6`)
- `HF_EMBEDDING_MODEL` (e.g. `all-MiniLM-L6-v2`)

## Run
```bash
source .venv/bin/activate
python main.py
```

## Gotchas
- `numpy<2` is pinned — torch 2.2.x was compiled against NumPy 1.x
- Use `langchain_classic.chains` not `langchain.chains` — RetrievalQA moved in langchain 1.x