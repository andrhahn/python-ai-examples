# rag-model-library-book

Book recommender using Open Library metadata + semantic similarity + Claude explanations.

## Entry Points
- `main.py` — indexes reading history, fetches candidates from Open Library, ranks by vector similarity, re-ranks with Claude, and prints structured recommendations with NYPL links.

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
Edit `reading_history.json` (gitignored, copy from `reading_history.example.json`). Each entry: `{title, author, description, subjects}`. Set `description` to `null` to have Open Library fetch it.

## Run
```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Gotchas
- Indexing is incremental — `index_reading_history()` only adds books not already in ChromaDB. Do NOT tell the user to delete `./chroma_db` when adding books; just re-run.
- Open Library can be flaky. `fetch_work_details` retries up to 3 times with exponential backoff. `fetch_candidates` skips subjects that time out rather than crashing.
- Work detail fetches and `explain()` calls run in parallel via `ThreadPoolExecutor` (4 workers for OL, TOP_N workers for Claude). Don't reduce pool sizes (description_fetch_limit=40, rerank pool=20) to gain speed — user prefers quality over runtime.
- `numpy<2` pinned — torch 2.2.x was compiled against NumPy 1.x
- `sentence-transformers<3.0` — 3.x requires PyTorch >= 2.4
- ChromaDB collection name is `reading_history` — if you have a stale `chroma_db/` from the old PDF Q&A version of this project, delete it before running