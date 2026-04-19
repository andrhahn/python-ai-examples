# Agent Example

A simple example of building an autonomous AI agent that can use tools to complete multi-step tasks.

## Concepts Covered

- Tool/function calling with an LLM
- Agent loop (observe → think → act)
- Handling tool results and feeding them back to the model

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

```bash
python main.py
```

## Linting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. See the root [README](../README.md#linting--formatting) for setup and usage instructions.
