# python-ai-examples

A collection of standalone AI/ML learning projects, one concept per subfolder.

## Project Structure

Each subfolder is fully independent — separate venv, requirements.txt, and .env. Do not share dependencies across subfolders.

| Folder | Concept |
|--------|---------|
| agent-example | Autonomous AI agent with tool use |
| gen-ai-example | Text generation with an LLM |
| integrate-custom-llm | Self-hosted / local LLM via Ollama |
| multi-agent-example | Orchestrating multiple agents |
| prompt-example | Prompt engineering techniques |
| rag-model-example | RAG pipeline basics |
| rag-model-library-book | RAG applied to books/PDFs |
| fine-tuning-example | Fine-tuning a model |

## Python Toolchain

- Python version: **3.12.4** (pinned via `.python-version` at repo root, read by pyenv)
- Virtual env: `python -m venv .venv` inside each subfolder
- Dependencies: `pip install -r requirements.txt`

## Environment Variables

- Each subfolder has a `.env.example` — copy to `.env` and fill in keys
- `.env` is gitignored; never commit it

## Linting & Formatting

Uses [ruff](https://docs.astral.sh/ruff/) for both linting and formatting. Config is at `ruff.toml` in the repo root and applies to all subfolders automatically.

Dev dependencies (install once from repo root via a root-level venv):
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install   # sets up the git hook
```

Run manually:
```bash
ruff check .         # lint
ruff check --fix .   # lint + auto-fix
ruff format .        # format
```

Pre-commit hook runs `ruff check --fix` and `ruff format` automatically on every commit.

## Testing

Uses [pytest](https://docs.pytest.org/). Each subfolder has a `tests/` directory. Run from any subfolder or the repo root:

```bash
pytest
```


## Conventions

- No co-author lines in commit messages
- Keep each subfolder self-contained; no cross-subfolder imports
- Each example is a single file — all logic in `main.py`, no additional modules or subfolders
- Entry points are `main.py` (and `ingest.py` for RAG projects)
- Test files go in `tests/` within each subfolder, named `test_*.py`

## Implementation Status

All examples are single-file — logic lives in `main.py` only, no additional modules. Placeholder projects have an empty `main.py` (`# main.py`) — no need to read them.

- **Implemented:** `rag-model-example`, `rag-model-library-book`, `chat-streaming-example`, `agent-example`
- **Placeholders (empty `main.py`):** `gen-ai-example`, `multi-agent-example`, `prompt-example`, `fine-tuning-example`, `integrate-custom-llm`

## Code Style Patterns

Observed across all implemented projects — follow these when implementing placeholders:

- `load_dotenv()` at module top, before any client init
- Required env vars via `os.environ["KEY"]` — raises `KeyError` if missing (intentional, no defaults)
- Module-level constants in `UPPERCASE`
- Print-based status logging (no `logging` module)
- Private helpers prefixed with `_`
- No tests written yet — `tests/` dirs exist with only `__init__.py`
