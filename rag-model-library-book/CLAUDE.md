# rag-model-library-book

Book recommender using Open Library metadata + semantic similarity + Claude explanations.

## Entry Points
- `main.py` — indexes reading history, fetches candidates from Open Library, ranks by vector similarity, explains recommendations via Claude with NYPL catalog links. Handles ingestion inline on first run; delete `./chroma_db` to re-index.

## Stack
- LLM: `ChatAnthropic` (model from env)
- Embeddings: `HuggingFaceEmbeddings` — runs locally, no API key needed
- Vector store: ChromaDB collection `reading_history`, persisted to `./chroma_db/`
- Candidate source: Open Library subjects API (no key needed)

## Env Vars
- `ANTHROPIC_API_KEY`
- `ANTHROPIC_MODEL` (e.g. `claude-sonnet-4-6`)
- `HF_EMBEDDING_MODEL` (e.g. `all-MiniLM-L6-v2`)

## Customization
Edit `READING_HISTORY` at the top of `main.py` — list of `{title, author}` dicts.

## Run
```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Gotchas
- `numpy<2` pinned — torch 2.2.x was compiled against NumPy 1.x
- `sentence-transformers<3.0` — 3.x requires PyTorch >= 2.4
- ChromaDB collection name is `reading_history` — if you have a stale `chroma_db/` from the old PDF Q&A version of this project, delete it before running
