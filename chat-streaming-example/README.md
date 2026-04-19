# Chat Streaming Example

A demonstration of real-time streaming chat with an LLM, including a multi-turn conversation loop that prints tokens incrementally as they arrive.

## Concepts Covered

- Streaming API responses (server-sent events)
- Incremental token output as tokens are received
- Multi-turn conversation state (message history)
- Handling stream events and lifecycle

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

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Then open `index.html` in your browser. The page connects to `http://localhost:8000/chat` and streams responses token by token.

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.
