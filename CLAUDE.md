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
| training-example | Fine-tuning a model |

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
- Entry points are `main.py` (and `ingest.py` for RAG projects)
- Test files go in `tests/` within each subfolder, named `test_*.py`
